"""Validate this portable skill bundle and run the existing local test suites."""
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SKILLS=ROOT/'skills'
EXPECTED=('drama-creator','ad-novel-to-screenplay','ad-asset-engine','ad-seedance25-shot-prompts','ad-combat-engine','ad-xuanhuan-engine')

def main():
    subprocess.run([sys.executable,str(SKILLS/'drama-creator/scripts/check_skill_bundle.py')],check=True)
    for name in EXPECTED:
        text=(SKILLS/name/'SKILL.md').read_text(encoding='utf-8')
        assert text.startswith('---\n'),name+': missing frontmatter'
        assert re.search(r'^name: '+re.escape(name)+r'$',text,re.M),name+': mismatched name'
        assert re.search(r'^description: .+',text,re.M),name+': missing description'
    for name in EXPECTED:
        scripts=SKILLS/name/'scripts'
        if scripts.exists() and list(scripts.glob('test_*.py')):
            print('Testing '+name,flush=True)
            subprocess.run([sys.executable,'-m','unittest','discover','-s',str(scripts),'-p','test_*.py'],check=True)
    print('PASS: bundle configuration and all local test suites.')

if __name__=='__main__':main()
