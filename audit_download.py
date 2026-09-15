from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,re,hashlib,csv,collections,subprocess,os
base=Path('/usr/set-lab-review');repo=base/'repo';out=base/'analysis';out.mkdir(exist_ok=True);d=json.loads((repo/'coordinates-v16.json').read_text());man=json.loads((repo/'asset-sha256-v16.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip();src=(repo/'uploads/ls.ts').read_text();skuids=set(re.findall(r'^  p\("([^"]+)"',src,re.M));assert len(skuids)==149
rows=[];groups=collections.defaultdict(list);pairs=collections.defaultdict(list)
for item in d['items']:
 pth=('originals/' if item['set']<=6 else 'generated/')+item['file'];p=repo/pth;assert p.exists();assert sha(p)==man[pth];im=Image.open(p);im.load();c=item['crop'];assert 0<=c[0]<c[2]<=im.width and 0<=c[1]<c[3]<=im.height
 assert item['sku'] in skuids
 extrema=im.getchannel('A').getextrema() if im.mode=='RGBA' else None
 rows.append(dict(file=pth,sku=item['sku'],set=item['set'],slot=item['slot'],sha256=man[pth],sha256Match=True,mode=im.mode,width=im.width,height=im.height,crop=json.dumps(c),alphaMin=extrema[0] if extrema else '',alphaMax=extrema[1] if extrema else '',hasTransparency=extrema is not None and extrema[0]<255,mountAssigned=item.get('pos') is not None,reviewBasis='Downloaded-source contact sheet, registered crop; selected full-resolution details',visualStatus='PENDING_VISUAL_REVIEW'))
 groups[item['sku']].append(pth);pairs[item['set']].append(item)
assert len(rows)==152 and len(groups)==149 and set(groups)==skuids and len(set(x['sha256'] for x in rows))==152
allpics=[str(p.relative_to(repo)) for p in repo.rglob('*') if p.is_file() and p.suffix.lower() in ['.png','.jpg','.jpeg','.webp','.gif','.svg'] and '.git' not in p.parts];assert sorted(allpics)==sorted(x['file'] for x in rows)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for st,items in pairs.items():
 width=1600 if len(items)>2 else 800;height=840
 sheet=Image.new('RGB',(width,height),'#b9c5ce');dr=ImageDraw.Draw(sheet)
 for j,i in enumerate(sorted(items,key=lambda x:x['file'])):
  im=Image.open(repo/('originals' if st<=6 else 'generated')/i['file']).convert('RGBA');im=im.crop(tuple(i['crop']));im.thumbnail((290,355));x=(j%5)*320 if len(items)>2 else j*400;y=(j//5)*420;sheet.paste(im,(x+(320-im.width)//2,y+10),im);dr.text((x+8,y+375),i['file'],font=font,fill='#112532');dr.text((x+8,y+398),'SKU '+i['sku'],font=font,fill='#112532')
 sheet.save(out/f'downloaded-set{st:02}.jpg')
for board in d['boards']:
 item=next(i for i in d['items'] if i['file']==board['file']);im=Image.open(repo/('originals' if item['set']<=6 else 'generated')/item['file']);im.crop(tuple(item['crop'])).save(out/('board-detail-'+item['file']))
# Full resolution detail copies of critical data labels and geometries, not tracked in delivery.
for name in ['set03-camf-32.png','set06-ram-16.png','set07-bat-6000.png','set08-sim-hybrid.png','set10-th-gr2.png','set14-disp-fold.png','set12-soc-d8300.png','set16-cons-ipa.png','set16-cons-tweezers.png']:
 item=next(i for i in d['items'] if i['file']==name);im=Image.open(repo/('originals' if item['set']<=6 else 'generated')/name);im.crop(tuple(item['crop'])).save(out/('detail-'+name))
with (out/'asset-audit.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary=dict(reviewedCommit=head,sourceRepo='https://github.com/ESPNex/set-lab-recovery',downloadedTo=str(repo),independentFreshClone=True,catalogEntries=149,assetImages=152,uniqueAssetHashes=152,missingSku=[],extraImages=[],sets={str(k):len(v) for k,v in sorted(pairs.items())},multiAssetSku={k:v for k,v in groups.items() if len(v)>1},alphaModes=dict(collections.Counter(x['mode'] for x in rows)),withoutTransparency=[x['file'] for x in rows if not x['hasTransparency']],catalogRawSha256=sha(repo/'uploads/ls.ts'),catalogNormalizedSha256=hashlib.sha256(src.encode()).hexdigest(),catalogNormalizedMatchesRegistry=hashlib.sha256(src.encode()).hexdigest()==d['catalogSourceSha256'],allRegisteredCropsInBounds=True,allAssetHashesMatchManifest=True)
(out/'download-integrity.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
