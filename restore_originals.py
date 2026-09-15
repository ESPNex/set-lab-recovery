"""Restore original SET01-07 from pinned user archive; never overwrite differing files."""
from pathlib import Path
import hashlib,json,urllib.request,zipfile,sys,shutil
root=Path(__file__).resolve().parent
report=json.loads((root/'analysis/recovery-originals-checks.json').read_text())
archive=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'downloads/recovered-originals-01-07.zip'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not archive.exists():
 archive.parent.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(report['source'],timeout=120) as response,archive.open('wb') as out:shutil.copyfileobj(response,out)
assert sha(archive)==report['archiveSha256'],'Archive hash mismatch: abort'
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for member in z.infolist():
  rel=Path(member.filename)
  if member.is_dir():continue
  assert not rel.is_absolute() and '..' not in rel.parts
  dest=root/rel;data=z.read(member)
  if dest.exists():
   if dest.read_bytes()==data:continue
   dest=root/'recovered-original-archive'/rel
   if dest.exists() and dest.read_bytes()==data:continue
   assert not dest.exists(),'Conflict: '+str(dest)
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
manifest=json.loads((root/'asset-sha256-v12.json').read_text())
for key in report['paths']:assert sha(root/key)==manifest[key],key
print('Verified70 original PNG; current metadata preserved.')
