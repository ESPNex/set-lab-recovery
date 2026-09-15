from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,re,csv,hashlib,itertools,shutil
r=Path('/home/user');b=Path('/usr/set-lab');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.loads((b/'coordinates-v12.json').read_text());old=json.loads(json.dumps(d));man=json.loads((b/'asset-sha256-v12.json').read_text());slots={}
for line in (b/'uploads/ls.ts').read_text().splitlines():
 m=re.search(r'^  (\w+): \{ id: "\w+", name: "([^"]+)", pos: (\[[^]]+\]), size: (\[[^]]+\]), explode: ([-.\d]+)',line)
 if m:slots[m[1]]=dict(pos=json.loads(m[3]),size=json.loads(m[4]),explode=float(m[5]))
(r/'analysis/set10-original-records.json').write_text(json.dumps([i for i in d['items'] if i['set']==10],indent=2,ensure_ascii=False))
notes={'soc-8e2':'Qualcomm Snapdragon8 Elite Gen5 leggibile; slash decorativi stampati fra righe. Il nome SKU8e2 non significa Gen2.','soc-dim95':'MediaTek Dimensity9500 leggibile, distinto da9400.','soc-ten6':'Google TensorG6 leggibile, distinto daG4/G5.','ram-18':'SK hynix18GB LPDDR5X9600MHz leggibile.','ram-32':'SK hynix32GB LPDDR5X10667MHz leggibile.','sto-1tb41':'KIOXIA1TB UFS4.1 leggibile; non4.0.','sto-2tb':'SAMSUNG2TB UFS4.1 leggibile.','hap-dual':'Esattamente due involucri Leaderdrive, marcati LRA L e LRA R; nessun2x ripetuto. Restano separati, non assumere una sede unica per entrambi.','th-cu':'CoolCo/Cu/0.4mm leggibile; strip rame appiattita molto allungata. Spessore illustrativo non misurato.','th-gr2':'CoolCo Dual graphite0.2+0.2mm leggibile; contorni sovrapposti suggeriscono un terzo foglio. Geometria/conteggio ambiguo: inventario separato, correzione richiesta.'}
board=d['boards'][4];fits=[]
for i in d['items']:
 if i['set']!=10:continue
 p=r/'generated'/i['file'];im=Image.open(p);box=im.getbbox();w,h=box[2]-box[0],box[3]-box[1];s=slots[i['slot']];q=min(s['size'][0]/w,s['size'][2]/h);size=[w*q,s['size'][1],h*q]
 i.update(crop=list(box),sourceSize=list(im.size),supersedesSha256=man['generated/'+i['file']],assetRevision='recovery-r1',provenance='AI regenerated recovery-r1; global smooth chroma-key and despill',visualReview=notes[i['sku']],physicalCompatibilityVerified=False,boardLocal=None,boardReference=None,angle=0,pos=s['pos'],size=size,status='nominal graphical placement only')
 man['generated/'+i['file']]=sha(p)
 if i['slot'] in ['soc','ram','storage']:
  x,y,sw,sh=board['slots'][i['slot']];q=min(sw/w,sh/h);cx,cy=x+sw/2,y+sh/2;t=dict(center=[cx,cy],size=[w*q,h*q],slotRect=[x,y,sw,sh],angle=0,scale=q,reference=board['file'],physicalCompatibilityVerified=False)
  i.update(boardLocal=t,boardReference=board['file'],pos=[.05+(cx-board['raster'][0]/2)*board['scale'],s['pos'][1],-3.35+(cy-board['raster'][1]/2)*board['scale']],size=[w*q*board['scale'],s['size'][1],h*q*board['scale']],status='GRAPHIC FIT on RF recovery-r1, no verified pinout or electrical compatibility')
  assert w*q<=sw+1e-7 and h*q<=sh+1e-7;fits.append(dict(sku=i['sku'],**t))
 if i['sku'] in ['hap-dual','th-gr2']:i.update(pos=None,size=None,angle=None,status='INVENTORY ONLY; individual seats or layer geometry unverified')
 if i['sku']=='th-gr2':i['qualityStatus']='NEEDS_LAYER_COUNT_CORRECTION'
 assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
assert [i for i in d['items'] if i['set']!=10]==[i for i in old['items'] if i['set']!=10]
combos=[dict(soc=a,ram=c,storage=e,board=board['file'],assetRevision='recovery-r1',status='GRAPHIC ONLY') for a,c,e in itertools.product(['soc-8e2','soc-dim95','soc-ten6'],['ram-18','ram-32'],['sto-1tb41','sto-2tb'])]
d['pair0910Compositions']=combos;d['pair0910CompositionsStatus']='RECOVERY_R1:12 graphical fits on bare RF footprint, not complete physical builds';d.update(version=13,status='SET10 regenerated;130 local PNG. SET11-12 missing20;2 catalog SKU ungenerated. Final0/8.',availabilityNote='SET01-10 and13-15 present and verified; SET11-12 pending regeneration.')
boardim=Image.open(b/'generated'/board['file']).convert('RGBA');boardim=boardim.crop(boardim.getbbox());W,H=boardim.size;font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
for page in range(2):
 sheet=Image.new('RGB',(3*W,2*(H+80)),'#14202b');dr=ImageDraw.Draw(sheet)
 for j,c in enumerate(combos[page*6:page*6+6]):
  im=boardim.copy()
  for sku in [c['soc'],c['ram'],c['storage']]:
   row=next(i for i in d['items'] if i['set']==10 and i['sku']==sku);t=row['boardLocal'];chip=Image.open(r/'generated'/row['file']);chip=chip.crop(chip.getbbox());w,h=map(round,t['size']);chip=chip.resize((w,h),Image.Resampling.LANCZOS);cx,cy=t['center'];im.alpha_composite(chip,(round(cx-w/2),round(cy-h/2)))
  x=(j%3)*W;y=(j//3)*(H+80);dr.text((x+12,y+8),f'{page*6+j+1:02} '+c['soc']+' + '+c['ram']+' + '+c['storage'],fill='#a6e9cf',font=font);dr.text((x+12,y+37),'RF09-R1 | SOLO FIT GRAFICO | NON VALIDAZIONE ELETTRONICA',fill='#ffd082',font=font);sheet.paste(im,(x,y+75),im)
 sheet.thumbnail((2400,1500));sheet.save(r/f'analysis/fit-set10-rf-recovery-{page+1}.jpg')
rec=json.loads((b/'recovery-plan.json').read_text());rec.update(regeneratedSets=[8,9,10],pendingSets=[x for x in rec['pendingSets'] if x['set']>10],localAssetCount=130)
plan=json.loads((b/'catalog-plan.json').read_text());plan['locallyAvailableAssetCount']=130;plan['qualityCorrections'].append({'file':'set10-th-gr2.png','issue':'Ambiguous outlines suggest third sheet instead of two','status':'NEEDS_CORRECTION','blocks':'validated layer count'})
finals=json.loads((b/'final-compositions-plan.json').read_text());finals['blockingReasons']=['Regenerate SET11-12:20 images','Generate2 consumables','Resolve or separately display documented defects; final visual review'];assert finals['requestedCount']==8 and finals['createdCount']==0
available=[];absent=[]
for k,h in man.items():
 p=r/k if (r/k).exists() else b/k
 if p.exists():assert sha(p)==h,k;available.append(k)
 else:absent.append(k)
assert len(available)==130 and len(absent)==20
for name,obj in [('coordinates-v13.json',d),('asset-sha256-v13.json',man),('catalog-plan.json',plan),('recovery-plan.json',rec),('final-compositions-plan.json',finals),('analysis/current-availability.json',{'availableCount':130,'missingCount':20,'missing':absent})]: (r/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
with (b/'catalog-status.csv').open(newline='') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['files'].startswith('set10-'):row['status']='REGENERATED_REVIEW_REQUIRED' if row['sku']=='th-gr2' else 'REGENERATED'
with (r/'catalog-status.csv').open('w',newline='') as f:wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
checks=dict(localHashesVerified=130,old120AvailableHashesUnchanged=True,other140MetadataRowsUnchanged=True,regenerated10AlphaValidated=True,contactSheetsReviewed=list(range(1,11))+[13,14,15],fullResolutionReviewed=['RF09-R1','th-gr2-R1'],fits=fits,compositionsCount=12,finalImagesCreated=0)
(r/'analysis/recovery-set10-checks.json').write_text(json.dumps(checks,indent=2));(r/'analysis/LEGGIMI-v12.md').write_text((b/'LEGGIMI.md').read_text())
text='''# SET Lab — revisione13 / recupero SET10

## Stato verificato

**SET13–15 presenti e integri:30 PNG. SET10 rigenerato:10 nuovi PNG.** Disponibili ora130 asset (SET01–10,13–15), tutti verificati contro il manifest corrente. Restano SET11–12:20 immagini da rigenerare e2 SKU mai prodotti (IPA e pinzette). Registro storico150 file/147 SKU su149, NON150 file disponibili.

**8 tavole finali confermate, zero prodotte.** Le12 diagnostiche RF di questo turno non sono le finali.

## GitHub

In questo turno `gh auth status` sia standard sia con configurazione dedicata ha restituito NON AUTENTICATO, nonostante la conferma dell’utente. Rilanciata autorizzazione device nel browser; codice temporaneo in chat, mai nel repository. Nessun push remoto dichiarato riuscito senza verifica. Nessuna password/token richiesto in chat.

Git locale e file in `/usr/set-lab`; `/usr` non persistente. Checkpoint Git nel workspace: `set-lab-recovery.bundle`. Contiene direttamente60 PNG generati SET08–10,13–15 e i relativi raw/metadati; i70 originali SET01–07 sono collegati al loro archivio esterno verificato, non inclusi nel bundle. Conservare anche lo ZIP originale: https://files.catbox.moe/ujc2ul.zip. `restore_originals.py` ripristina e verifica70 hash senza sovrascrivere i registri recenti.

## Analisi multimodale

Riesaminate13 tavole: SET01–10,13–15,130 asset. PCB RF09-R1 e grafite10 letti anche a piena risoluzione. SET11–12 assenti non riesaminati.

| SKU SET10 | Esito |
|---|---|
'''
for sku,note in notes.items():text+=f'| {sku} | {note} |\n'
text+='''
La grafite ha un problema di conteggio/contorni: non correggerlo attribuendo automaticamente i margini a spessori reali. Inventario separato con segnalazione di correzione. Doppio LRA: un file inventario con due motori L/R, non due motori nella stessa sede singola. Entrambi gli asset hanno montaggio nullo.

## Coordinate nuove sul RF09-R1

PCB originale del SET09 precedente perduto; qui si usa ESCLUSIVAMENTE RF09 rigenerato: crop[82,79,1331,692], raster1249×613. Sedi libere: SoC[162,131,341,350],RAM[601,127,206,356],UFS[899,180,216,252]. Scala nominale s=min(6.55/1249,7.10/613), X=0.05+(u−1249/2)s, Z=−3.35+(v−613/2)s, Y da `ls.ts`. Nessun pinout ingegneristico.

Fit uniforme q=min(sedeW/cropW,sedeH/cropH), centro coincidente,0° di rotazione raster. Nessuno stiramento. Le UFS sono incluse perché la nuova sede è libera, non perché sia stata provata compatibilità elettronica.

| SKU | Centro u,v px | Disegno W,H px |
|---|---|---|
'''
fmt=lambda v:'null' if v is None else ', '.join(f'{x:.3f}' for x in v)
for f in fits:text+=f'| {f["sku"]} | {fmt(f["center"])} | {fmt(f["size"])} |\n'
text+='''
### Dodici prove

3SoC×2RAM×2UFS, una sola variante per ruolo in ogni prova. `analysis/fit-set10-rf-recovery-1.jpg` e `-2.jpg`:6 combinazioni ciascuna. Nessuna asserzione di motherboard reale compatibile con tutti i SoC/RAM, nessun circuito funzionante certificato. Periferiche e strati termici non inclusi sotto i chip per nascondere difetti.

| File SET10 | Crop L,T,R,B px | Centro X,Y,Z cm | Bbox X,Y,Z cm |
|---|---|---|---|
'''
for i in d['items']:
 if i['set']==10:text+=f'| {i["file"]} | {i["crop"]} | {fmt(i["pos"])} | {fmt(i["size"])} |\n'
text+='''
Heatpipe con collocazione nominale dello slot thermal, non forma misurata della vasca. Spessore0.4mm stampato non sostituisce il valore nominale del catalogo. Haptics/grafite isolati senza coordinate assegnate.

## Pipeline e integrità

Raw AI preservati,10 generazioni del turno. Alpha postprodotto: Pillow/NumPy global chroma-key smoothstep e despill2px. Nessun rembg/flood fill, nessuna ROI manuale nuova. Etichette illustrate non sono specifiche fisiche verificate.

Manifest V13:150 hash storici,130 file locali verificati; i120 asset già disponibili sono invariati. Solo i10 hash SET10 sostituiti, precedenti hash riportati nei record come supersedesSha256. Vecchi record SET10 archiviati; tutti gli altri140 record restano invariati.

Rilievi storici ancora validi: USB01 bande bianche, frontale03 stampa52MP, RAM06 marchio non conforme, Lite senza RAM/UFS identificabili, batteria07 microtesto contraddittorio, SIM08 tre vani, fold14 rapporto errato, aperture cover15 non coincidenti automaticamente con le camere. eMMC13 separata da UFS. Non nascondere questi problemi nelle finali.

## Prossimo lotto

SET11: back-alu,back-leather,bat-dual,cons-screws,frame-classic,soc-exy26,soc-g99,soc-helio,soc-tensor,sto-1tb. Poi SET12 e2 consumabili. Infine8 tavole da PNG effettivi, esploso leggibile, alternative separate e riferimenti motherboard riutilizzati dichiarati. Viewer V1 non aggiornato in questo turno; niente generazione in background.
'''
(r/'LEGGIMI.md').write_text(text)
for p in [p for p in r.rglob('*') if p.is_file() and p.suffix not in ['.zip','.bundle']]:
 dst=b/p.relative_to(r);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
print('130 verified;12 diagnostics;20 regeneration pending;2 new SKU pending')
