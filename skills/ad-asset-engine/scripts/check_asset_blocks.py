"""Validate text structure of standalone image-prompt blocks, not generated images."""
import argparse
from pathlib import Path
import re


def validate(text):
    errors = []
    blocks = list(re.finditer(r'```(?:text|markdown)?\n(.*?)\n```', text, re.S))
    if not blocks:
        return ['未找到独立提示词代码块']
    for index, match in enumerate(blocks, 1):
        body = match.group(1)
        prefix = f'第{index}块：'
        start = text.rfind('\n## ', 0, match.start())
        section = text[max(0, start):match.start()]
        def require(condition, message):
            if not condition:
                errors.append(prefix + message)
        require(bool(re.search(r'(?<!\d)\d+\s*:\s*\d+(?!\d)', body)), '缺少整板比例')
        require(not re.search(r'同上|同规格|见母版|同图\s*\d|同前|按上述|参见第|按外部技能', body), '提示词不是自包含')
        require(not re.search(r'图\s*\d+|图〔|图\[', body), '图号应移到标题或接线单')
        require(not re.search(r'〔[^〕]+〕', body), '仍有未填占位符')
        if '【角色四格设定图】' in body:
            require(bool(re.search(r'全图共\s*4\s*格', body)), '角色必须显式四格')
            for token in ('面部特写', '正面全身', '90°侧面', '背面全身', '无脸', '头顶至鞋', '五官10项', '声纹波形', 'fifth panel', 'different face'):
                require(token in body, '角色缺少：' + token)
            require(bool(re.search(r'Voice Description(?! Label)', section)), '缺少代码块外完整英文音色文本')
            title = re.search(r'画面正上方居中写着唯一文字[：:]\s*[“"]([^”"\n]+)[”"]', body)
            require(bool(title), '缺少顶部居中且为唯一文字的角色名')
            if title:
                require(title.group(1).strip() not in ('角色名称', '实际角色名称', '角色名', '姓名'), '角色名仍是占位符')
            require('绝对禁止输出任何其他英文字母、乱码或多余文字' in body, '缺少角色名以外的文字禁令')
            require('图底音色速览标签' not in body, '英文音色短标签须留在图外')
            require(not re.search(r'character names|禁止(?:出现|输出|标注|渲染)?(?:人物名|角色名)|不标人物名', body, re.I), '存在禁止角色名称入图的冲突约束')
        elif '【道具设定图】' in body:
            require(bool(re.search(r'全图共\s*4\s*格', body)), '道具必须显式四格')
            for token in ('正面视图', '45°侧视图', '顶部俯视图', '关键细节特写', '左上角标注'):
                require(token in body, '道具缺少：' + token)
            require(bool(re.search(r'无人物|禁止.*人物', body)), '缺少禁止人物约束')
            require(bool(re.search(r'无手|禁止.*手持', body)), '缺少禁止手或手持约束')
        elif '【场景母版】' in body:
            for token in ('【空间坐标】', '【主光源】'):
                require(token in body, '母版缺少：' + token)
            require('无人' in body or '禁止人物' in body, '母版须说明无人')
        elif '【场景定位】' in body:
            require(bool(re.search(r'全图共\s*9\s*格', body)), '九宫格必须显式九格')
            for token in ('【场景画面描写】', '【九宫格内容分配】', '【参考场景锁定模式】', '【摄影机矩阵】', '【摄影机参数】', '【光照曝光】', '【标注要求】'):
                require(token in body, '九宫格缺少：' + token)
            require('数字' in body and '对照表' in body, '缺少标注失败的数字对照降级方案')
            require('无人' in body or '禁止人物' in body, '九宫格须说明无人')
        elif '【群像参考图】' in body:
            require(bool(re.search(r'全图共\s*3\s*格', body)), '群像须显式三格')
        elif '【场景调度图】' in body:
            require('轴' in body and ('朝向' in body or '起点' in body), '调度图缺少轴线或朝向／起点')
        else:
            errors.append(prefix + '缺少可识别的资产模板类型')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    args = parser.parse_args()
    errors = validate(args.file.read_text(encoding='utf-8'))
    for error in errors:
        print('FAIL:', error)
    if errors:
        return 1
    print('PASS: 文本结构检查通过；仍需核对原文、编号交接、空间语义和实际图像。')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
