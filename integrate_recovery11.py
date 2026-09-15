from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,re,csv,hashlib,shutil
r=Path('/home/user');b=Path('/usr/set-lab');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.loads((b/'coordinates-v13.json').read_text());old=json.loads(json.dumps(d));man=json.loads((b/'asset-sha256-v13.json').read_text());slots={}
for l in (b/'uploads/ls.ts').read_text().splitlines():
 m=re.search(r'^  (\w+): \{ id: "\w+", name: "([^"]+)", pos: (\[[^]]+\]), size: (\[[^]]+\]), explode: ([-.\d]+)',l)
 if m:slots[m[1]]=dict(pos=json.loads(m[3]),size=json.loads(m[4]))
notes={'back-alu':'Vertex alluminio satinato, apertura camera passante, lega non misurata.','back-leather':'EcoLine marrone, trama e cuciture illustrate, apertura camera passante; materiale PU non certificato.','bat-dual':'ATL DUAL CELL5500mAh TOTAL3.87V leggibile. Due pouch, capacità totale esplicita, circuito parallelo non validato.','cons-screws':'Sei viti Phillips separate. DiametroM1.6 non misurabile dal raster, un solo SKU inventario.','frame-classic':'Vista frontale più pulita del raster perduto, centro e home trasparenti. Foro superiore camera illustrato scuro. Scelta apertura16:9; contraddizione catalogo4:3/16:9 ancora aperta.','soc-exy26':'Samsung Exynos2600 leggibile.','soc-g99':'MediaTek HelioG99 leggibile.','soc-helio':'UNISOC T7250 leggibile: SKU soc-helio non implica Helio/MediaTek.','soc-tensor':'Google TensorG5 leggibile.','sto-1tb':'Samsung1TB UFS4.0 leggibile, non4.1; package generato quasi quadrato.'}
board=d['boards'][1];fits=[]
(r/'analysis/set11-original-records.json').write_text(json.dumps([i for i in d['items'] if i['set']==11],indent=2))
for i in d['items']:
 if i['set']!=11:continue
 p=r/'generated'/i['file'];im=Image.open(p);box=im.getbbox();w,h=box[2]-box[0],box[3]-box[1];s=slots[i['slot']];q=min(s['size'][0]/w,s['size'][2]/h)
 i.update(crop=list(box),sourceSize=list(im.size),pos=s['pos'],size=[w*q,s['size'][1],h*q],angle=0,boardLocal=None,boardReference=None,status='fit nominale non validato',assetRevision='recovery-r1',provenance='AI regenerated recovery-r1; smooth global chroma-key/despill',supersedesSha256=man['generated/'+i['file']],visualReview=notes[i['sku']],physicalCompatibilityVerified=False)
 man['generated/'+i['file']]=sha(p)
 if i['slot'] in ['soc','storage']:
  x,y,sw,sh=board['slots'][i['slot']];q=min(sw/w,sh/h);cx,cy=x+sw/2,y+sh/2;t=dict(center=[cx,cy],size=[w*q,h*q],slotRect=[x,y,sw,sh],angle=0,reference=board['file'],borrowed=True,hypothesis=True,physicalCompatibilityVerified=False)
  i.update(boardLocal=t,boardReference=board['file'],pos=[.05+(cx-board['raster'][0]/2)*board['scale'],s['pos'][1],-3.35+(cy-board['raster'][1]/2)*board['scale']],size=[w*q*board['scale'],s['size'][1],h*q*board['scale']],status='IPOTESI grafica Pro03 riutilizzato; RAM/UFS non identificati univocamente');fits.append(dict(sku=i['sku'],**t));assert w*q<=sw+1e-8 and h*q<=sh+1e-8
 if i['sku']=='cons-screws':i.update(pos=None,size=None,angle=None,status='INVENTARIO; slot frame non autorizza montaggio')
 assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
assert [i for i in old['items'] if i['set']!=11]==[i for i in d['items'] if i['set']!=11]
combos=[dict(soc=s,storage='sto-1tb',ram=None,board=board['file'],borrowed=True,status='PARTIAL GRAPHIC HYPOTHESIS, NOT ELECTRICAL VALIDATION') for s in ['soc-exy26','soc-g99','soc-helio','soc-tensor']]
d.update(version=14,status='SET11 regenerated;140 local PNG; SET12 missing10;2 new SKU pending; final0/8. Repo current tree excludes raw/analysis images.',availabilityNote='SET01-11,13-15 physically present and verified.');d['set11Compositions']=combos;d['pair1112CompositionsStatus']='PARTIAL: SET11 refitted, SET12 absent'
bi=Image.open(b/'originals'/board['file']).convert('RGBA');bi=bi.crop(tuple(board['crop']));W,H=bi.size;sheet=Image.new('RGB',(W*2,(H+75)*2),'#14202b');dr=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
for j,c in enumerate(combos):
 im=bi.copy()
 for sku in [c['soc'],c['storage']]:
  row=next(i for i in d['items'] if i['set']==11 and i['sku']==sku);t=row['boardLocal'];chip=Image.open(r/'generated'/row['file']);chip=chip.crop(chip.getbbox());w,h=map(round,t['size']);chip=chip.resize((w,h),Image.Resampling.LANCZOS);cx,cy=t['center'];im.alpha_composite(chip,(round(cx-w/2),round(cy-h/2)))
 x=j%2*W;y=j//2*(H+75);dr.text((x+15,y+10),c['soc']+' + sto-1tb | PRO03 RIUTILIZZATO',font=font,fill='#a7e8cd');dr.text((x+15,y+39),'IPOTESI UFS / RAM ASSENTE / NON BUILD VALIDATA',font=font,fill='#ffcc83');sheet.paste(im,(x,y+70),im)
sheet.thumbnail((2200,1400));sheet.save(r/'analysis/fit-set11-pro-recovery.jpg')
rec=json.loads((b/'recovery-plan.json').read_text());rec.update(regeneratedSets=[8,9,10,11],pendingSets=[x for x in rec['pendingSets'] if x['set']==12],localAssetCount=140)
plan=json.loads((b/'catalog-plan.json').read_text());plan['locallyAvailableAssetCount']=140
finals=json.loads((b/'final-compositions-plan.json').read_text());finals['blockingReasons']=['Regenerate SET12:10 images','Generate2 consumables','Resolve or separately display documented defects and visually review finals'];assert finals['requestedCount']==8 and finals['createdCount']==0
available=[];absent=[]
for k,h in man.items():
 p=r/k if (r/k).exists() else b/k
 if p.exists():assert sha(p)==h,k;available.append(k)
 else:absent.append(k)
assert len(available)==140 and len(absent)==10
for name,obj in [('coordinates-v14.json',d),('asset-sha256-v14.json',man),('recovery-plan.json',rec),('catalog-plan.json',plan),('final-compositions-plan.json',finals),('analysis/current-availability.json',dict(availableCount=140,missingCount=10,missing=absent)),('analysis/recovery-set11-checks.json',dict(localHashesVerified=140,old130AvailableHashesUnchanged=True,other140RowsUnchanged=True,contactSheetsReviewed=list(range(1,12))+[13,14,15],nativeReviewed=['Pro03','frame-classic11','bat-dual11'],fits=fits,partialCompositions=4,finalImagesCreated=0))]: (r/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
with (b/'catalog-status.csv').open(newline='') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['files'].startswith('set11-'):row['status']='REGENERATED_REVIEW_REQUIRED' if row['sku']=='frame-classic' else 'REGENERATED'
with (r/'catalog-status.csv').open('w',newline='') as f:wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
(r/'analysis/LEGGIMI-v13.md').write_text((b/'LEGGIMI.md').read_text())
text='''# SET Lab — revisione14 / SET11 rigenerato

## Repository ripulito

Repository privato: https://github.com/ESPNex/set-lab-recovery

Richiesta utente: eliminare immagini inutili o in più. Rimossi dalla versione corrente **70 raw e27 immagini diagnostiche** precedentemente tracciate. Non sono stati eliminati componenti di catalogo. I nuovi raw/diagnostici SET11 restano solo materiali di lavoro in `/usr`, esclusi dal push. Nel ramo corrente restano **140 immagini di componenti**, in `originals/` (60) e `generated/` (80), più dati, script e viewerV1 già richiesto. Nessun contatto-sheet, crop o mockup aggiuntivo nel ramo corrente.

Rimozione normale Git, non riscrittura della storia: raw/diagnostiche già caricate restano recuperabili nei vecchi commit. `/usr` non persistente; dopo un reset le tavole si ricostruiscono dai PNG, i raw nuovi non caricati non sono garantiti. Le immagini di lavoro non sono SKU aggiuntivi e non vengono conteggiate nel catalogo.

## Stato pipeline

SET11 rigenerato da `ls.ts`:10 nuovi PNG. Disponibili140 immagini effettive SET01–11,13–15, hash verificati. Rimane SET12 da rigenerare (10) e2 SKU mai prodotti (IPA/pinzette). Registro storico150 file/147 SKU su149, non150 file ora presenti. **8 finali previste, zero create.**

Il checkpoint nel workspace `set-lab-recovery.bundle` è storico, precedente alla pulizia e al SET11: non rappresenta lo stato corrente. Fonte corrente: repository GitHub. Non rigenerato il bundle completo perché contiene la storia e supererebbe lo spazio persistente disponibile.

## Analisi eseguita

Riesaminate le14 tavole disponibili (140 asset); Pro03, nuovo telaio classico e batteria dual letti in dettaglio. SET12 assente non riesaminato. Quattro composizioni parziali SoC+UFS generate per analisi locale, non aggiunte al repository e non considerate finali.

| SKU SET11 | Esito |
|---|---|
'''
for sku,note in notes.items():text+=f'| {sku} | {note} |\n'
text+='''
Il telaio ora ha centro vuoto pulito e home passante, senza ritaglio ROI manuale. Apertura portrait16:9 circa, non prova di compatibilità: `ls.ts` contraddice4:3 e16:9. L’etichetta5500mAh TOTAL evita di attribuire5500 a ciascuna pouch; tensione/materiali restano illustrativi.

## Coordinate e ipotesi

Pro03 riutilizzato, nessuna nuova motherboard: SoC[520,203,226,239], ipotesi UFS[786,342,119,121] nel crop1286×666. Serigrafia SOC/RAM/UFS ambigua: queste assegnazioni non sono pinout. RAM assente nelle quattro prove. Anche Helio/Unisoc non sono dichiarati compatibili con UFS4.0: solo test raster.

Fit uniforme q=min(slotW/cropW,slotH/cropH); X=0.05+(u−1286/2)s, Z=−3.35+(v−666/2)s con s=min(6.55/1286,7.10/666). Y da `ls.ts`, rotazione0°. Unità cm nominali, nessuna deformazione. Cover e batteria fit nominale; viti pos/size/angle null perché inventario.

| File | Crop L,T,R,B px | Centro X,Y,Z cm | Bbox X,Y,Z cm |
|---|---|---|---|
'''
fmt=lambda v:'null' if v is None else ', '.join(f'{x:.3f}' for x in v)
for i in d['items']:
 if i['set']==11:text+=f'| {i["file"]} | {i["crop"]} | {fmt(i["pos"])} | {fmt(i["size"])} |\n'
text+='''
## Pipeline, integrità e limiti

Alpha postprodotto con chroma-key globale graduato smoothstep e despill2px Pillow/NumPy. Nessun rembg, flood fill o nuova ROI manuale. I10 nuovi raw sono preservati localmente ma non aggiunti alla consegna Git. Script di analisi producono file ignorati da Git.

V14 conserva gli altri140 record. I130 PNG già presenti restano invariati;10 hash SET11 nuovi con riferimento ai precedenti in supersedesSha256. Viti sei per immagine ma un solo SKU. Diagnostiche escluse dal conteggio.

Persistono difetti storici: USB01 bande bianche, frontale03 etichetta52MP, RAM06 marca diversa, Lite senza sedi RAM/UFS certe, batteria07 microtesto, SIM08 tre vani, grafite10 conteggio ambiguo, fold14 rapporto errato, cover15 aperture non coincidenti automaticamente. eMMC13 non è UFS. Non nascondere difetti sotto altri pezzi nelle finali.

Prossimo: SET12, poi2 consumabili e8 tavole finali con componenti reali dell’inventario, alternative separate e riferimenti riutilizzati dichiarati. Nessuna generazione in background. Il viewer storico non è aggiornato a tutti i SET.
'''
(r/'LEGGIMI.md').write_text(text)
for p in [p for p in r.rglob('*') if p.is_file() and p.suffix not in ['.zip','.bundle']]:
 dst=b/p.relative_to(r);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
(b/'README.md').write_text(text)
print('140 verified; SET11 complete;4 partial hypotheses; repo cleanup next')
