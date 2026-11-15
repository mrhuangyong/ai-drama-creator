"""Check local prompt structure and timing; no model/platform or combat-semantics guarantees."""
import argparse
from pathlib import Path
import re

def ordinal(s):
    if s.isdigit(): return int(s)
    d={c:i for i,c in enumerate('零一二三四五六七八九')}
    if s=='十': return 10
    if '十' in s:
        a,b=s.split('十'); return (d.get(a,1))*10+d.get(b,0)
    return d.get(s,-1)

def validate(text,duration):
    errors=[]
    blocks=re.findall(r'```(?:swift|text)?\n(.*?)\n```',text,re.S)
    if not blocks: blocks=[text.strip()]
    for i,body in enumerate(blocks,1):
        p=f'第{i}段：'
        for field in ('风格：','场景：','站位参考：','负面：'):
            if not re.search(r'^'+field,body,re.M):errors.append(p+'缺少'+field)
        if re.search(r'short-drama-director|sd-(?:feed|qc|asset|decision)-engine|<音效[:：]|★正面重击|模式\s*[A-K]|协议\s*[A-D]|\bS\d{2}\b',body):
            errors.append(p+'混入工作流或工程标记')
        negative=re.search(r'^负面：(.*)$',body,re.M)
        if negative and not ('字幕' in negative[1] and ('bgm' in negative[1].lower() or '背景音乐' in negative[1])):
            errors.append(p+'缺少字幕／背景音乐控制')
        shots=re.findall(r'^镜头([一二三四五六七八九十\d]+)：[（(]([^）)]+)[）)](.*)$',body,re.M)
        if shots:
            if [ordinal(s[0]) for s in shots]!=list(range(1,len(shots)+1)):
                errors.append(p+'镜号不连续或重复')
            values=[]
            for _,length,action in shots:
                if not re.fullmatch(r'[1-9]\d*秒',length):
                    errors.append(p+'镜头时长须为正整数秒');continue
                values.append(int(length[:-1]))
                if not action.strip():errors.append(p+'空镜头正文')
            # One-take: one shot spans the clip, with an internal timeline.
            if len(shots)==1 and re.search(r'\d+\s*-\s*\d+秒',shots[0][2]):
                errors+=check_timeline(shots[0][2],duration,p)
                if re.search(r'硬切|正反打|切至|切换机位',shots[0][2]):errors.append(p+'一镜到底包含切镜')
            elif re.search(r'\d+\s*-\s*\d+秒',body):
                errors.append(p+'混用镜头时长与时间区间')
            if sum(values)!=duration:errors.append(p+f'镜头合计{sum(values)}秒，应为{duration}秒')
        else:
            errors+=check_timeline(body,duration,p)
    return errors

def check_timeline(body,duration,p):
    out=[]
    raw=re.findall(r'(?<![\d.])(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)秒',body)
    if not raw:return [p+'未找到镜头时长或连续时间轴']
    if any('.' in a or '.' in b for a,b in raw):return [p+'时间轴须为整数秒']
    end=0
    for a,b in raw:
        a,b=int(a),int(b)
        if a!=end or b<=a:out.append(p+'时间轴有缺口、重叠或倒退')
        end=b
    if end!=duration:out.append(p+f'时间轴结束于{end}秒，应为{duration}秒')
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file',type=Path);p.add_argument('--duration',type=int,choices=(15,30),required=True)
    a=p.parse_args();errors=validate(a.file.read_text(encoding='utf-8'),a.duration)
    for e in errors:print('FAIL:',e)
    if not errors:print('PASS: 本地格式与时长检查通过；剧情、动作及连续性仍需人工核对。')
    return int(bool(errors))

if __name__=='__main__':raise SystemExit(main())
