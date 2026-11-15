"""Check local drama skill names, routing paths, UI invocation names and references."""
import argparse
from pathlib import Path
import re

EXPECTED=('drama-creator','ad-novel-to-screenplay','ad-asset-engine','ad-seedance25-shot-prompts','ad-combat-engine','ad-xuanhuan-engine')

def validate(bundle):
    errors=[]
    for name in EXPECTED:
        root=bundle/name; entry=root/'SKILL.md'
        if not entry.is_file():errors.append('缺少入口：'+name);continue
        text=entry.read_text(encoding='utf-8')
        found=re.search(r'^name:\s*(\S+)\s*$',text,re.M)
        if not found or found[1]!=name:errors.append(name+'：文件夹与name不一致')
        ui=root/'agents/openai.yaml'
        if not ui.exists():errors.append(name+'：缺少UI入口')
        else:
            content=ui.read_text(encoding='utf-8')
            if '$'+name+' ' not in content:errors.append(name+'：UI默认调用名不一致')
        for p in root.rglob('*.md'):
            s=p.read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',s):
                if '://' in target:continue
                dest=(p.parent/target).resolve()
                if not dest.exists():errors.append(str(p.relative_to(bundle))+'：缺少引用 '+target)
                elif not dest.is_relative_to(bundle.resolve()):errors.append(str(p.relative_to(bundle))+'：依赖包外文件 '+target)
            # A root bundle uses sibling skill links; specialized skills stay independently portable.
            if name!='drama-creator' and re.search(r'\]\(\.\./(?:ad-[\w-]+|drama-creator)/',s):
                errors.append(str(p.relative_to(bundle))+'：专业技能引入必需的同级工作流依赖')
    extra=[p.name for p in bundle.iterdir() if p.is_dir() and (p/'SKILL.md').exists() and p.name not in EXPECTED]
    if extra:errors.append('存在未规范的技能入口：'+', '.join(extra))
    controller=bundle/'drama-creator/SKILL.md'
    if controller.exists():
        s=controller.read_text(encoding='utf-8')
        for name in EXPECTED[1:]:
            if '../'+name+'/SKILL.md' not in s:errors.append('总控缺少路由：'+name)
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    a=p.parse_args();errors=validate(a.root)
    for e in errors:print('FAIL:',e)
    if not errors:print('PASS: 六个技能的命名、总控路由、UI调用与本地链接有效。创作语义仍需按实际材料核对。')
    return int(bool(errors))

if __name__=='__main__':raise SystemExit(main())
