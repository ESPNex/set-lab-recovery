from pathlib import Path
from PIL import Image,ImageDraw
import json,re,csv,hashlib
r=Path('/home/user');b=Path('/usr/set-lab');src=(b/'uploads/ls.ts').read_text();d=json.loads((b/'coordinates-v9.json').read_text());old=json.loads(json.dumps(d));plan=json.loads((b/'catalog-plan.json').read_text());lot=next(x for x in plan['pendingLots'] if x['set']==15);missing=json.loads((b/'catalog-missing.json').read_text());parts={x['id']:x for x in missing};slots={}
for l in src.splitlines():
 m=re.search(r'^  (\w+): \{ id: "\w+", name: "([^"]+)", pos: (\[[^]]+\]), size: (\[[^]]+\]), explode: ([-.\d]+)',l)
 if m:slots[m[1]]=dict(pos=json.loads(m[3]),size=json.loads(m[4]),explode=float(m[5]))
notes={
'back-black':'LuxGuard nero AG, riflessi ridotti. Tre fori grandi in colonna e due piccoli, alpha passante ai centri. Non corrisponde automaticamente al dual camera orizzontale.',
'back-white':'LuxGuard bianco perla, bordo oro. Tre aperture scure verticali e apertura inferiore; superficie con iridescenza rosata. Geometria diversa dalle altre cover.',
'back-carbon':'AeroForge carbonio a trama diagonale; tre aperture scure in colonna. Fibra e leggerezza non verificabili da immagine.',
'back-wood':'EcoLine noce leggibile, venatura verticale. Tre aperture triangolari e due piccole: non stessa geometria delle cover nere/bianche.',
'cam-uw':'Due moduli Sony50MP, uno OIS e uno UW, affiancati orizzontalmente. Non allineabili per semplice traslazione alle tre aperture verticali delle cover.',
'cam-peri10':'SONY64MP10xOIS leggibile. Package molto allungato, prisma quadrangolare; vista illustrativa parzialmente sezionata con ottica esposta. Non prova di ingombro fisico o compatibilità con aperture circolari.',
'spk-hires':'AAC Technologies Hi-Res Audio192kHz leggibile, un singolo modulo con griglia e contatti. Etichetta non equivale a certificazione o banda acustica misurata.',
'usb-pd':'Amphenol PD3.1,140W,USB2.0 leggibili. Porta e flex uniti, vista non strettamente ortografica. Nessuna prova di erogazione140W del telefono o del connettore.',
'cons-thermalp':'Tre pad separati, SBS Parts Thermal Pad1mm leggibile. Liner illustrato e lieve tinta violacea ai bordi inferiori conservata. Non montare la tavola intera come se fosse un telaio.',
'cons-kapton':'Un rotolo ambra, SBS Parts Kapton10mm leggibile, foro centrale trasparente. Prospettiva e materiale illustrativi, larghezza non misurata.'}
new=[]
for sku in lot['skus']:
 im=Image.open(r/f'generated/set15-{sku}.png');box=im.getbbox();w,h=box[2]-box[0],box[3]-box[1];slot=parts[sku]['slot'];s=slots[slot];q=min(s['size'][0]/w,s['size'][2]/h);size=[w*q,s['size'][1],h*q];cons=sku.startswith('cons-');blocked=cons or slot=='cameraRear'
 row=dict(file=f'set15-{sku}.png',sku=sku,set=15,slot=slot,crop=list(box),sourceSize=list(im.size),pos=None if blocked else s['pos'],size=None if blocked else size,angle=None if blocked else 0,boardLocal=None,boardReference=None,provenance='AI + global chroma-key graduato e despill',visualReview=notes[sku],status='INVENTARIO SEPARATO: sede non assegnata' if blocked else 'fit nominale proporzionale, sede NON verificata',physicalCompatibilityVerified=False,inventoryPreview={'size':None if cons else size,'angle':0},explodeOffset=None if cons else s['explode'],qualityStatus='ILLUSTRATIVE_NOT_TECHNICALLY_VALIDATED');new.append(row)
 assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
d['items']+=new;d.update(version=10,status='150 historical assets,147/149 represented SKU,2 missing. Locally30 assets SET13-15. Final8 blocked pending original archives and catalog completion.',availabilityNote='120 SET01-12 source PNG missing; metadata preserved.');assert d['items'][:140]==old['items']
missing=[x for x in missing if x['id'] not in lot['skus']];assert len(missing)==2 and len({i['sku'] for i in d['items']})==147
plan.update(availableAssets=150,representedSkuCount=147,missingSkuCount=2,locallyAvailableAssetCount=30);plan['pendingLots']=[x for x in plan['pendingLots'] if x['set']>15];plan['assemblyWarnings']=['SET15 cover hole patterns differ; neither dual horizontal camera nor periscope has a validated matching cover. Keep separated in exploded view.','SET01-12 files absent: recover before multimodal review and final compositing.']
finals=json.loads((b/'final-compositions-plan.json').read_text());assert finals['requestedCount']==8 and finals['createdCount']==0;finals['blockingReasons']=['Missing120 source images SET01-12','Remaining SKU cons-ipa and cons-tweezers','Open geometry/label defects require review and declared exclusions'];finals['status']='BLOCKED_PENDING_SOURCE_RECOVERY_AND_CATALOG_COMPLETION'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();manifest=json.loads((b/'asset-sha256-v9.json').read_text());verified=[];absent=[]
for key,val in manifest.items():
 p=b/key
 if p.exists():assert sha(p)==val;verified.append(key)
 else:absent.append(key)
assert len(absent)==120 and len(verified)==20
for row in new:manifest['generated/'+row['file']]=sha(r/'generated'/row['file'])
assert len(manifest)==150 and len(set(manifest.values()))==150
for name,obj in [('coordinates-v10.json',d),('catalog-plan.json',plan),('catalog-missing.json',missing),('final-compositions-plan.json',finals),('asset-sha256-v10.json',manifest),('analysis/missing-source-files.json',{'count':120,'paths':absent,'neededArchives':['set-lab-session.zip (SET01-07)','SET08 update','SET09 update','SET10 update','SET11 update','SET12 update']})]: (r/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
with (b/'catalog-status.csv').open(newline='') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['sku'] in lot['skus']:row.update(status='REPRESENTED',files='set15-'+row['sku']+'.png',planned_set='')
with (r/'catalog-status.csv').open('w',newline='') as f:wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
checks={'historicalAssets':150,'locallyAvailableAssets':30,'representedSku':147,'missingSku':2,'old140RecordsUnchanged':True,'old140ManifestEntriesPreserved':True,'old120BinariesRehashed':False,'restoredSet13and14HashesVerified':True,'new10RGBAValidated':True,'multimodalReviewThisTurn':['SET13 contact sheet','SET14 contact sheet','SET15 contact sheet','SET15 periscope full resolution','SET15 thermal pads full resolution','SET15 black cover full resolution'],'previousSET01to12VisualReviewThisTurn':False,'consumablesAndCamerasMountNull':True,'finalImagesRequested':8,'finalImagesCreated':0}
# Diagnostic of alternatives: no claim that mismatched cameras seat in cover apertures.
sheet=Image.new('RGB',(1600,940),'#172330');dr=ImageDraw.Draw(sheet)
for j,row in enumerate(new):
 x=(j%5)*320;y=(j//5)*470;dr.text((x+10,y+10),row['sku'],fill='white');im=Image.open(r/'generated'/row['file']);im=im.crop(im.getbbox())
 if row['inventoryPreview']['size'] is not None:
  sw,_,sh=slots[row['slot']]['size'];k=min(280/sw,355/sh);rw,rh=round(sw*k),round(sh*k);left=x+(320-rw)//2;top=y+40;dr.rectangle((left,top,left+rw,top+rh),outline='#f4be65',width=2);im.thumbnail((rw,rh));sheet.paste(im,(left+(rw-im.width)//2,top+(rh-im.height)//2),im)
 else:
  im.thumbnail((280,355));sheet.paste(im,(x+(320-im.width)//2,y+40+(355-im.height)//2),im)
 dr.text((x+10,y+415),'SEPARATO / NON MONTATO' if row['pos'] is None else 'FIT NOMINALE NON VERIFICATO',fill='#f4be65')
sheet.save(r/'analysis/fit-set15-nominal.jpg');(r/'analysis/revision10-checks.json').write_text(json.dumps(checks,indent=2));(r/'analysis/LEGGIMI-v9.md').write_text((b/'LEGGIMI.md').read_text())
text='''# SET Lab — revisione 10 / SET 15

## Stato reale

**SET15 generato:10 PNG. Totale storico150 immagini,147/149 SKU rappresentati,2 SKU mancanti.**

Restano `cons-ipa` (IPA99%100ml) e `cons-tweezers` (pinzette ESD), residuo SET16 da2, non un lotto completo da10. Raggiunte le10 generazioni del turno; questi due asset NON sono ancora prodotti. Non viene dichiarato completato il catalogo.

**Consegna finale:8 immagini, ancora zero prodotte.** L’unione finale è bloccata dalla mancanza dei120 PNG SET01–12 (incluse le cinque motherboard), dai due SKU residui e dalla revisione dei difetti aperti. I metadati non sono immagini e non permettono un riesame multimodale.

### Recupero necessario

Verificato `/usr/set-lab`: disponibili fisicamente30 PNG elaborati SET13–15, non150. Mancano gli originali SET01–06 e i generati SET07–12. Elenco esatto in `analysis/missing-source-files.json`.

Ricaricare **`set-lab-session.zip` (SET01–07) e gli aggiornamenti SET08,09,10,11,12**. Non verranno sostituiti con immagini nuove spacciate per originali. Gli archivi SET13–15 sono inclusi come contenuti cumulativi nel nuovo ZIP.

Scaricare **`set15-update.zip`**, unire agli archivi precedenti. Include30 raw e30 PNG elaborati SET13–15, metadati storici e nuove verifiche; NON è un backup completo SET01–15. Materiali in `/usr/set-lab`, percorso non persistente; workspace con README e ZIP. Viewer V1 non disponibile in questa copia e non aggiornato.

## Pipeline

Generazioni separate su magenta, raw intatti. Pillow/NumPy chroma-key globale graduato: R>100,B>100,min(R,B)−G>35; t=clamp((e−35)/75), alpha×(1−t²(3−2t)). Alpha<3 azzerato, despill parziale e bordo2px. Nessun rembg/flood fill/ROI manuale nel SET15. Trasparenza postprodotta, NON nativa. Tutti i10 PNG nuovi hanno alpha0–255 e crop valido.

## Analisi multimodale effettiva

Riesaminate le tavole SET13,14 e15 (30 asset); letti a piena risoluzione periscopio, pad termici e cover nera. Nessun riesame dichiarato dei SET01–12 assenti. Rilievi storici nel LEGGIMI V9 allegato.

| SKU | Osservazione |
|---|---|
'''
for row in new:text+=f'| {row["sku"]} | {row["visualReview"]} |\n'
text+='''
### Risultato controllo incastri

Le quattro cover NON hanno aperture identiche: nere/carbonio/bianche principalmente verticali, noce triangolare. Il dual-camera è orizzontale, il periscopio allungato con ingresso quadrangolare. Non basta scalare un’immagine per renderla un ricambio compatibile: nessun montaggio camera-cover approvato. Le camere restano `pos,size,angle=null`, esposte separatamente nelle future tavole. Non si nascondono sotto la cover per simulare l’incastro.

Consumabili: tre pad in una singola immagine e un rotolo Kapton sono articoli di inventario. Lo slot `frame` in `ls.ts` non è una sede di montaggio: coordinate nulle. Pad non scomposti automaticamente in tre SKU. Spessore1mm e larghezza10mm sono etichette, non misure del raster.

## Coordinate nominali

Cm di simulazione da `ls.ts`: X destra, Y strati, Z lunghezza. Angolo0° per orientamento leggibile; nessuno yaw3D validato. Fit uniforme q=min(slotW/cropW,slotH/cropH), nessuna deformazione. Dimensioni reali, contatti, aperture e spessori non certificati.

`analysis/fit-set15-nominal.jpg` mostra10 confronti separati, con rettangolo nominale dello slot dove sensato. È una diagnostica inventario, NON un’immagine finale e NON una prova che i pezzi combacino. `inventoryPreview` delle camere non autorizza il montaggio.

| File | Crop L,T,R,B px | Centro X,Y,Z cm | Bbox X,Y,Z cm | ° |
|---|---|---|---|---|
'''
fmt=lambda v:'null' if v is None else ', '.join(f'{x:.3f}' for x in v)
for row in new:text+=f'| {row["file"]} | {row["crop"]} | {fmt(row["pos"])} | {fmt(row["size"])} | {row["angle"]} |\n'
text+='''
Tutti i nuovi `boardLocal` e `boardReference` null: nessuna piazzola PCB viene inventata. Cover, speaker e USB hanno solo collocazione nominale dello slot; connettori/mounting ears non verificati.

## Verifiche registrate

- `coordinates-v10.json`:150 record, precedenti140 invariati.
- `asset-sha256-v10.json`:150 hash distinti storici; verificati20 PNG recuperati SET13–14 e10 nuovi. I120 assenti NON ricalcolati.
- `catalog-status.csv`:149 SKU,147 rappresentati e2 non generati; stato difetto fold SET14 preservato.
- Piano finale8 preservato, stato bloccato e motivi espliciti; zero tavole finali.
- `analysis/revision10-checks.json`, log/crop/alpha e script inclusi.

## Sequenza per completare la richiesta

1. Generare i due SKU residui nel prossimo turno (SET16 parziale).
2. Ripristinare gli archivi SET01–12, verificarne gli hash contro il manifest.
3. Riesame multimodale completo: tavole e ingrandimenti delle sedi, aperture, orientamenti e proporzioni; risolvere o isolare i difetti. Fold SET14 con rapporto errato, RF con sede UFS occupata, etichette precedenti errate restano rilievi aperti. eMMC non è UFS; LPDDR4X non implica compatibilità con i SoC illustrati.
4. Comporre8 tavole da PNG effettivi: una per coppia di SET, esploso leggibile, alternative e accessori separati, riferimenti presi da altri SET dichiarati. Nessun pezzo nascosto per mascherare un conflitto.
5. Riesaminare tutte e8 le tavole, controllare copertura degli asset e consegnare archivio finale.

Nessuna elaborazione prosegue in background. Non si promettono incastri fisici da sole immagini AI: il controllo raggiungibile riguarda allineamento grafico, proporzioni, occlusioni e coerenza visiva.
'''
(r/'LEGGIMI.md').write_text(text)
print('V10:150 historical /147SKU /2pending; locally30; finals0/8')
