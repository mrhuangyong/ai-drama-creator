"""Build a deterministic distributable ZIP and a SHA-256 checksum."""
from pathlib import Path
import hashlib
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def main():
    version=(ROOT/'VERSION').read_text().strip()
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+',version):raise ValueError('Invalid VERSION')
    prefix='ai-drama-creator-v'+version
    files=[ROOT/n for n in ('README.md','THIRD_PARTY_NOTICES.md','VERSION')]
    files+=list((ROOT/'skills').rglob('*'))+list((ROOT/'scripts').rglob('*.py'))
    files=sorted({p for p in files if p.is_file() and not any(part in ('__pycache__','.git') for part in p.parts) and p.name!='.DS_Store' and p.suffix!='.pyc'})
    dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    archive=dist/(prefix+'.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            entry=zipfile.ZipInfo(prefix+'/'+p.relative_to(ROOT).as_posix(),date_time=(2026,1,1,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            entry.external_attr=0o100644<<16
            z.writestr(entry,p.read_bytes())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(files)
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    (dist/'SHA256SUMS').write_text(digest+'  '+archive.name+'\n')
    print(str(archive)+': '+str(len(files))+' files, '+str(archive.stat().st_size)+' bytes')
    print('SHA256: '+digest)

if __name__=='__main__':main()
