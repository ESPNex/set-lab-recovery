from pathlib import Path
from PIL import Image,ImageDraw
import json,re,hashlib,csv,shutil,zipfile
r=Path('/home/user');b=Path('/usr/set-lab');src=(b/'uploads/ls.ts').read_text();d=json.loads((b/'coordinates-v8.json').read_text());old=json.loads(json.dumps(d));plan=json.loads((b/'catalog-plan.json').read_text());lot=next(x for x in plan['pendingLots'] if x['set']==14);missing=json.loads((b/'catalog-missing.json').read_text());parts={x['id']:x for x in missing};slots={}
for l in src.splitlines():
 m=re.search(r'^  (\w+): \{ id: "\w+", name: "([^"]+)", pos: (\[[^]]+\]), size: (\[[^]]+\]), explode: ([-.\d]+)',l)
 if m:slots[m[1]]=dict(pos=json.loads(m[3]),size=json.loads(m[4]),explode=float(m[5]))
notes={'back-red':'LuxGuard leggibile; rosso scuro lucido. I fori fotocamera sono raffigurati scuri, non aperture alpha; disposizione non verificata rispetto ai moduli.', 'bat-8000':'BYD8000mAh3.95V STACKED leggibile; due strati visibili. Capacità totale illustrata, non per pouch; collegamenti non verificati.', 'bat-stacked':'ATL6800mAh3.94V Si-C STACKED leggibile; due strati. Nessuna validazione di spessore, potenza o capacità.', 'disp-eco':'Tianma TFT6.5,60Hz,720x1600 leggibili; notch centrale e flex inferiore.', 'disp-lcd67':'BOE LCD IPS6.7,90Hz,1080x2400 leggibili; notch centrale.', 'disp-oled61':'LG Display OLED LTPO6.1,120Hz,1179x2556 leggibili; punch centrale scuro.', 'disp-fold':'Samsung Display OLED7.6,120Hz,1812x2176 leggibili. DIFETTO: raster largo, proporzioni non corrispondenti al formato portrait richiesto. Non montare su telaio rigido; correzione futura necessaria.', 'glass-gg3':'Corning Gorilla Glass3: lastra stretta con fessura superiore illustrata; interno opaco chiaro, non trasmissione ottica.', 'glass-gg7':'Corning Gorilla Glass7i: identificatore presente e punch superiore; interno opaco illustrativo.', 'glass-utg':'SCHOTT Ultra Thin Glass UTG presente; lastra quasi quadrata distinta dai vetri stretti. Non coincide con il display fold generato; nessun accoppiamento validato.'}
new=[]
for sku in lot['skus']:
 f=r/f'generated/set14-{sku}.png';im=Image.open(f);box=im.getbbox();w,h=box[2]-box[0],box[3]-box[1];slot=parts[sku]['slot'];s=slots[slot];q=min(s['size'][0]/w,s['size'][2]/h);size=[w*q,s['size'][1],h*q];blocked=sku in ['disp-fold','glass-utg'];row=dict(file=f.name,sku=sku,set=14,slot=slot,crop=list(box),sourceSize=list(im.size),pos=None if blocked else s['pos'],size=None if blocked else size,angle=None if blocked else 0,boardLocal=None,boardReference=None,provenance='AI + chroma-key graduato e despill',visualReview=notes[sku],status='INVENTARIO SEPARATO: montaggio non assegnato' if blocked else 'fit nominale proporzionale; montaggio non verificato',physicalCompatibilityVerified=False,inventoryPreview={'size':size,'angle':0},explodeOffset=s['explode'],qualityStatus='NEEDS_GEOMETRY_CORRECTION' if sku=='disp-fold' else 'ILLUSTRATIVE_NOT_TECHNICALLY_VALIDATED');new.append(row)
 assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
d['items']+=new;d.update(version=9,status='140 historical assets,137/149 represented SKU,12 missing. SET01-12 source images unavailable this session; fold geometry flagged. Final8 not created.');d['availabilityNote']='SET13 restored from ZIP, SET14 generated. SET01-12 metadata/hash only; binaries need earlier archives.'
assert d['items'][:130]==old['items'];present={i['sku'] for i in d['items']};missing=[x for x in missing if x['id'] not in lot['skus']];assert len(present)==137 and len(missing)==12
plan.update(availableAssets=140,representedSkuCount=137,missingSkuCount=12,locallyAvailableAssetCount=20);plan['pendingLots']=[x for x in plan['pendingLots'] if x['set']>14];plan['qualityCorrections'].append({'file':'set14-disp-fold.png','issue':'Landscape panel despite portrait1812x2176 specification','blocks':'validated fold assembly'})
finals=json.loads((b/'final-compositions-plan.json').read_text());assert finals['requestedCount']==8 and finals['createdCount']==0
manifest=json.loads((b/'asset-sha256-v8.json').read_text());historical=manifest.copy();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in (b/'generated').glob('set13-*.png'):assert sha(f)==manifest['generated/'+f.name]
for row in new:manifest['generated/'+row['file']]=sha(r/'generated'/row['file'])
assert len(manifest)==140 and len(set(manifest.values()))==140
for name,obj in [('coordinates-v9.json',d),('catalog-plan.json',plan),('catalog-missing.json',missing),('final-compositions-plan.json',finals),('asset-sha256-v9.json',manifest)]: (r/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
with (b/'catalog-status.csv').open(newline='') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['sku'] in lot['skus']:row.update(status='GENERATED_REVIEW_REQUIRED' if row['sku']=='disp-fold' else 'REPRESENTED',files='set14-'+row['sku']+'.png',planned_set='')
with (r/'catalog-status.csv').open('w',newline='') as f:wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
checks={'historicalAssets':140,'locallyAvailableAssets':20,'representedSku':137,'missingSku':12,'old130RecordsUnchanged':True,'old130ManifestEntriesPreserved':True,'old120BinariesRehashed':False,'restoredSet13HashesVerified':True,'new10RGBAValidated':True,'multimodalReviewThisTurn':['SET13 contact sheet','SET14 contact sheet','SET14 fold full resolution'],'previousSET01to12VisualReviewThisTurn':False,'foldAndUTGMountNull':True,'finalImagesRequested':8,'finalImagesCreated':0}
(r/'analysis/revision9-checks.json').write_text(json.dumps(checks,indent=2))
# Proportional inventory tests against nominal slot bounds, not assembled devices.
sheet=Image.new('RGB',(1600,860),'#172330');draw=ImageDraw.Draw(sheet)
for j,row in enumerate(new):
 x=(j%5)*320;y=(j//5)*430;sw,_,sh=slots[row['slot']]['size'];k=min(270/sw,335/sh);rw,rh=round(sw*k),round(sh*k);left=x+(320-rw)//2;top=y+35;draw.rectangle((left,top,left+rw,top+rh),outline='#f4be65',width=2)
 im=Image.open(r/'generated'/row['file']);im=im.crop(im.getbbox());im.thumbnail((rw,rh));sheet.paste(im,(left+(rw-im.width)//2,top+(rh-im.height)//2),im);draw.text((x+10,y+8),row['sku'],fill='white');draw.text((x+10,y+380),'SEPARATO / NON MONTARE' if row['pos'] is None else 'SCALA NOMINALE / NON VERIFICATA',fill='#f4be65')
sheet.save(r/'analysis/fit-set14-nominal.jpg')
(r/'analysis/LEGGIMI-v8.md').write_text((b/'LEGGIMI.md').read_text())
text='''# SET Lab — revisione 9 / SET 14

## Stato e archivio

**SET14:10 nuovi PNG. Totale storico140 immagini,137/149 SKU rappresentati,12 SKU mancanti.** Un asset nuovo, il display fold, richiede correzione geometrica: rappresentato non significa approvato tecnicamente.

**8 immagini composite finali confermate, zero prodotte.** Prossimo SET15 da10, poi residuo SET16 da2; nessun SKU inventato per riempire il lotto finale.

Scaricare `set14-update.zip` e conservare gli archivi precedenti. Questo ZIP contiene SET14 e una copia recuperata del SET13 con catalogo/coordinate: NON contiene i120 PNG SET01–12. Estrarre unendo alla cartella degli archivi precedenti.

La vecchia `/usr/set-lab` non era più disponibile nella nuova sessione. È stata ricreata recuperando `set13-update.zip`. Disponibili fisicamente ora20 PNG elaborati (SET13–14), non140. I120 file precedenti restano registrati nei metadati e nei manifest SHA256, ma non è stato possibile ricontrollarli né riesaminarli visivamente in questo turno. Per le tavole finali occorre ricaricare l’archivio iniziale e gli aggiornamenti SET08–12. Nessuna perdita è stata nascosta generando sostituti.

Materiali di lavoro in `/usr/set-lab`, percorso NON persistente. Nel workspace restano questo LEGGIMI e lo ZIP recuperabile; lo ZIP include anche i file recuperati del SET13 per conservarli tra sessioni.

## Pipeline e trasparenza

10 generazioni AI distinte, raw conservati. Chroma-key globale Pillow/NumPy: candidato R>100,B>100,min(R,B)−G>35; smoothstep su t=clamp((min(R,B)−G−35)/75); alpha originale×(1−smoothstep(t)). Alpha<3 azzerato; despill parziale e fascia2px ai bordi. Nessun rembg/flood fill; nessuna maschera manuale nuova. PNG con alpha postprodotto, NON nativo.

Vetri: superficie chiara opaca con riflessi illustrati, non trasparenza ottica. Fori cover rossa scuri, non aperture trasparenti: non sovrapporre le camere pretendendo un incastro validato. Rosso più scuro del concetto “lava”, identità mantenuta.

## Controllo multimodale

Riletti tutti i10 asset SET13 e i10 SET14 nelle tavole; display fold esaminato anche a piena risoluzione. SET01–12 non disponibili: i rilievi storici sono nel LEGGIMI V8 allegato, non nuove verifiche.

| SKU | Esito |
|---|---|
'''
for row in new:text+=f'| {row["sku"]} | {row["visualReview"]} |\n'
text+='''
### Blocco fold / UTG

La risoluzione stampata è corretta, ma il display fold è largo anziché portrait. Non è stato stirato o ruotato per mascherare il difetto. `disp-fold` e `glass-utg` hanno `pos,size,angle=null`: inventario separato, nessun montaggio sul telaio standard. `inventoryPreview` serve solo al confronto grafico. Le loro sagome non sono una coppia fisicamente verificata. Correzione del fold registrata in `catalog-plan.json`; non sono state eseguite ulteriori generazioni oltre le10 del lotto.

## Coordinate e proporzioni

Unità cm NOMINALI da `ls.ts`, non misure di fabbrica. X destra, Y spessore/strati, Z lunghezza. Rotazione0° per preservare testo e orientamento raster. Per ogni bbox w×h, q=min(larghezzaSlot/w,lunghezzaSlot/h), dimensioni[wq,spessoreSlot,hq]. Nessuna deformazione. Le linguette dei display e batterie sono incluse nel bbox. Spessore stacked non misurato:0.44cm del catalogo è solo valore di simulazione.

Display e vetro occupano strati del telefono, non piazzole del PCB. `boardReference` e `boardLocal` sono null per tutti i nuovi asset. Nessun fit sul PCB GAME viene inventato in assenza del file. Diagnostica `analysis/fit-set14-nominal.jpg`: dieci viste separate contro il rettangolo nominale dello slot, NON assemblaggi completi né immagini finali.

| File | Crop L,T,R,B px | Centro X,Y,Z cm | Dimensioni X,Y,Z cm | ° |
|---|---|---|---|---|
'''
fmt=lambda v:'null' if v is None else ', '.join(f'{x:.3f}' for x in v)
for row in new:text+=f'| {row["file"]} | {row["crop"]} | {fmt(row["pos"])} | {fmt(row["size"])} | {row["angle"]} |\n'
text+='''
Le varianti non si montano tutte contemporaneamente. Dimensioni e fori dei vetri non provano corrispondenza con i display, e cover/fotocamere richiedono verifica. Rimane valido il blocco eMMC SET13: non sostituisce UFS. LPDDR4X/SoC del SET13 restano prove grafiche non configurazioni elettriche supportate.

## File e controlli

- `coordinates-v9.json`:140 record; precedenti130 invariati.
- `asset-sha256-v9.json`:140 hash distinti storici; verificati i10 recuperati SET13 e i10 nuovi. I120 assenti NON sono stati ricalcolati.
- `catalog-status.csv`:149 SKU, fold marcato GENERATED_REVIEW_REQUIRED.
- `analysis/revision9-checks.json`: distingue disponibilità locale, storico e controlli effettivi.
- `new_raw`, `generated`, tavole e log SET13–14; script di elaborazione e catalogo `uploads/ls.ts`.
- `analysis/LEGGIMI-v8.md`: coordinate/limitazioni storiche precedenti; non sostituisce questa nota sulla disponibilità.

Il viewer V1 non è stato recuperato né aggiornato in questa sessione. Nessun processo continua la generazione in background.

## Restanti SKU

'''
for l in plan['pendingLots']:text+=f'- SET{l["set"]}: '+', '.join(l['skus'])+'.\n'
text+='\nLe otto tavole finali restano organizzate per coppie di SET; solo cinque SKU motherboard, con riuso dichiarato dei riferimenti nelle altre tavole. Servono gli archivi precedenti prima del compositing finale.\n'
(r/'LEGGIMI.md').write_text(text)
print('V9 ready',len(d['items']),len(present),len(missing))
