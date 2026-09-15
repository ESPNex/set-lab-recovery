from pathlib import Path
from PIL import Image
import json,hashlib,csv,shutil
r=Path('/home/user');b=Path('/usr/set-lab');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.loads((b/'coordinates-v15.json').read_text());m=json.loads((b/'asset-sha256-v15.json').read_text());missing=json.loads((b/'catalog-missing.json').read_text());assert {x['id'] for x in missing}=={'cons-ipa','cons-tweezers'}
for sku in ['cons-ipa','cons-tweezers']:
 p=r/f'generated/set16-{sku}.png';im=Image.open(p);assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
 d['items'].append(dict(file=p.name,sku=sku,slot='frame',set=16,crop=list(im.getbbox()),sourceSize=list(im.size),pos=None,size=None,angle=None,boardLocal=None,boardReference=None,status='INVENTARIO: consumabile/utensile non montato',provenance='AI + global smooth chroma-key/despill',visualReview='SBS Parts IPA99%100ml, etichetta leggibile e pictogramma fiamma; contenuto non verificato.' if sku=='cons-ipa' else 'Un paio di pinzette SBS Parts/ESD, due bracci con punte allineate. Raster orizzontale, proprietà ESD non misurata.',physicalCompatibilityVerified=False))
 m['generated/'+p.name]=sha(p)
assert len(d['items'])==152 and len({i['sku'] for i in d['items']})==149
d.update(version=16,status='Catalog representation complete:152 assets,149 unique SKU. SET16 residual2. Independent repository review pending; final0/8.',availabilityNote='All catalog SKU have PNG; no technical certification implied.')
plan=json.loads((b/'catalog-plan.json').read_text());plan.update(availableAssets=152,representedSkuCount=149,missingSkuCount=0,locallyAvailableAssetCount=152,pendingLots=[],status='CATALOG_REPRESENTATION_COMPLETE_REVIEW_PENDING')
rec=json.loads((b/'recovery-plan.json').read_text());rec.update(localAssetCount=152,historicalRecords=152,pendingNewSku=[],status='RECOVERY_AND_CATALOG_REPRESENTATION_COMPLETE')
finals=json.loads((b/'final-compositions-plan.json').read_text());finals['blockingReasons']=['Independent downloaded-repository review and documented geometry/label defects'];finals['status']='CATALOG_COMPLETE_REVIEW_PENDING';assert finals['createdCount']==0
for name,obj in [('coordinates-v16.json',d),('asset-sha256-v16.json',m),('catalog-missing.json',[]),('catalog-plan.json',plan),('recovery-plan.json',rec),('final-compositions-plan.json',finals),('analysis/current-availability.json',{'availableCount':152,'missingCount':0,'missing':[]})]: (b/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
with (b/'catalog-status.csv').open(newline='') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['sku'] in ['cons-ipa','cons-tweezers']:row.update(status='REPRESENTED_INVENTORY_ONLY',files='set16-'+row['sku']+'.png',planned_set='')
with (b/'catalog-status.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
for folder in ['generated','new_raw','analysis']:
 for p in (r/folder).glob('*'):
  if p.is_file():shutil.copy2(p,b/folder/p.name)
for name in ['complete_catalog.py','process_set16.py']:shutil.copy2(r/name,b/name)
(b/'analysis/set16-checks.json').write_text(json.dumps({'skuCount':2,'completeTenAssetSet':False,'visualReview':'IPA and tweezers inspected','nullMounts':True,'alphaVerified':True,'finalCreatedCount':0},indent=2))
print('152 assets,149 SKU,0 missing')
