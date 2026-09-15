from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,re,csv,hashlib,shutil,subprocess
r=Path('/home/user');b=Path('/usr/set-lab');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.loads((b/'coordinates-v14.json').read_text());old=json.loads(json.dumps(d));man=json.loads((b/'asset-sha256-v14.json').read_text());src=(b/'uploads/ls.ts').read_text();assert len(set(re.findall(r'^  p\("([^"]+)"',src,re.M)))==149
assert hashlib.sha256(src.encode()).hexdigest()==d['catalogSourceSha256'];assert subprocess.check_output(['git','-C',str(b),'show','HEAD:uploads/ls.ts'])==(b/'uploads/ls.ts').read_bytes()
slots={}
for l in src.splitlines():
 m=re.search(r'^  (\w+): \{ id: "\w+", name: "([^"]+)", pos: (\[[^]]+\]), size: (\[[^]]+\]), explode: ([-.\d]+)',l)
 if m:slots[m[1]]=dict(pos=json.loads(m[3]),size=json.loads(m[4]))
notes={'cons-glue':'SBS Parts B-7000 15ml leggibile; tubo orizzontale, microtesto aggiuntivo illustrativo, lieve riflesso magenta metallico. Inventario, non frame montato.','cons-tabs':'Due adesivi chiari con tiranti arancio, SBS Parts; liner largo e bordo rosato conservato. Non misura fisica o traslucenza reale.','frame-mg':'Vertex AZ91D: due grandi finestre alpha, traverse/rail illustrativi. Lega e138g non certificabili dal raster.','frame-ss':'AeroForge316L: finestre alpha, geometria diversa dal magnesio, qualche riflesso violaceo. Massa198g non verificata.','soc-6g1':'Qualcomm Snapdragon6Gen1 leggibile.','soc-7g3':'Qualcomm Snapdragon7Gen3 leggibile, senza plus.','soc-8g2':'Qualcomm Snapdragon8Gen2 leggibile; scritta Pin1 extra, non certificazione pinout.','soc-d7300':'MediaTek Dimensity7300 leggibile.','soc-d8300':'MediaTek Dimensity8300 leggibile, con sigle CPU/GPU/MT6880V aggiuntive non richieste e non verificate: non usare come specifica tecnica.','soc-d9300':'MediaTek Dimensity9300+ leggibile con plus presente.'}
board=d['boards'][1];fits=[]
(r/'analysis/set12-original-records.json').write_text(json.dumps([i for i in d['items'] if i['set']==12],indent=2))
for i in d['items']:
 if i['set']!=12:continue
 p=r/'generated'/i['file'];im=Image.open(p);box=im.getbbox();w,h=box[2]-box[0],box[3]-box[1];s=slots[i['slot']];q=min(s['size'][0]/w,s['size'][2]/h)
 i.update(crop=list(box),sourceSize=list(im.size),pos=s['pos'],size=[w*q,s['size'][1],h*q],angle=0,boardLocal=None,boardReference=None,status='fit nominale non validato',assetRevision='recovery-r1',supersedesSha256=man['generated/'+i['file']],provenance='AI regenerated R1; global smooth chroma-key/despill',visualReview=notes[i['sku']],physicalCompatibilityVerified=False);man['generated/'+i['file']]=sha(p)
 if i['slot']=='soc':
  x,y,sw,sh=board['slots']['soc'];q=min(sw/w,sh/h);cx,cy=x+sw/2,y+sh/2;t=dict(center=[cx,cy],size=[w*q,h*q],slotRect=[x,y,sw,sh],angle=0,reference=board['file'],borrowed=True,hypothesis=True,physicalCompatibilityVerified=False);i.update(boardLocal=t,boardReference=board['file'],pos=[.05+(cx-board['raster'][0]/2)*board['scale'],s['pos'][1],-3.35+(cy-board['raster'][1]/2)*board['scale']],size=[w*q*board['scale'],s['size'][1],h*q*board['scale']],status='IPOTESI grafica Pro03 riutilizzato; nessun pinout validato');fits.append(dict(sku=i['sku'],**t));assert w*q<=sw+1e-8 and h*q<=sh+1e-8
 if i['sku'].startswith('cons-'):i.update(pos=None,size=None,angle=None,status='INVENTARIO; slot frame non è una sede')
 assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
assert [i for i in old['items'] if i['set']!=12]==[i for i in d['items'] if i['set']!=12]
combos=[dict(soc=f['sku'],storage='sto-1tb',storageSet=11,ram=None,board=board['file'],borrowed=True,status='PARTIAL GRAPHIC HYPOTHESIS ONLY') for f in fits];d['set12Compositions']=combos;d['pair1112Compositions']=d['set11Compositions']+combos;d['pair1112CompositionsStatus']='10 partial graphical hypotheses R1;RAM absent; not electrical configurations';d.update(version=15,status='SET08-12 recovery complete;150 asset files available;147/149 SKU represented;2 new consumables pending;final0/8.',availabilityNote='All150 historical assets now physically present; SET01-15 complete10 each.')
bi=Image.open(b/'originals'/board['file']).convert('RGBA').crop(tuple(board['crop']));W,H=bi.size;sheet=Image.new('RGB',(W*3,(H+75)*2),'#14202b');dr=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
for j,c in enumerate(combos):
 im=bi.copy()
 for st,sku in [(12,c['soc']),(11,c['storage'])]:
  row=next(i for i in d['items'] if i['set']==st and i['sku']==sku);t=row['boardLocal'];p=(r if st==12 else b)/'generated'/row['file'];chip=Image.open(p);chip=chip.crop(chip.getbbox());w,h=map(round,t['size']);chip=chip.resize((w,h),Image.Resampling.LANCZOS);cx,cy=t['center'];im.alpha_composite(chip,(round(cx-w/2),round(cy-h/2)))
 x=j%3*W;y=j//3*(H+75);dr.text((x+12,y+8),c['soc']+' + sto-1tb SET11 | PRO03 RIUTILIZZATO',font=font,fill='#a7e8cd');dr.text((x+12,y+37),'IPOTESI UFS / RAM ASSENTE / NON VALIDAZIONE ELETTRONICA',font=font,fill='#ffce83');sheet.paste(im,(x,y+70),im)
sheet.thumbnail((2400,1500));sheet.save(r/'analysis/fit-set12-pro-recovery.jpg')
rec=json.loads((b/'recovery-plan.json').read_text());rec.update(regeneratedSets=[8,9,10,11,12],pendingSets=[],localAssetCount=150,status='RECOVERY_COMPLETE;2 new catalog SKU pending')
plan=json.loads((b/'catalog-plan.json').read_text());plan['locallyAvailableAssetCount']=150
finals=json.loads((b/'final-compositions-plan.json').read_text());finals['blockingReasons']=['Generate2 consumables','Resolve or separately display documented defects and visually review8 final composites'];assert finals['requestedCount']==8 and finals['createdCount']==0
for k,h in man.items():
 p=r/k if (r/k).exists() else b/k;assert p.exists() and sha(p)==h,k
for name,obj in [('coordinates-v15.json',d),('asset-sha256-v15.json',man),('recovery-plan.json',rec),('catalog-plan.json',plan),('final-compositions-plan.json',finals),('analysis/current-availability.json',dict(availableCount=150,missingCount=0,missing=[])),('analysis/recovery-set12-checks.json',dict(localHashesVerified=150,old140AvailableHashesUnchanged=True,other140RowsUnchanged=True,contactSheetsReviewed=list(range(1,16)),fits=fits,partialCompositions=6,finalImagesCreated=0,catalogSku149=True,catalogBytesMatchGit=True,catalogNormalizedHashMatchesRegistry=True)),('analysis/catalog-integrity.json',dict(path='uploads/ls.ts',skuCount=149,uniqueSkuCount=149,rawSha256=sha(b/'uploads/ls.ts'),normalizedLfSha256=hashlib.sha256(src.encode()).hexdigest(),matchesGit=True,matchesUserArchive=True,note='Raw CRLF and LF-normalized hashes differ only by line endings; no catalog loss.'))]: (r/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
with (b/'catalog-status.csv').open(newline='') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['files'].startswith('set12-'):row['status']='REGENERATED_REVIEW_REQUIRED' if row['sku']=='soc-d8300' else 'REGENERATED'
with (r/'catalog-status.csv').open('w',newline='') as f:wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
(r/'analysis/LEGGIMI-v14.md').write_text((b/'LEGGIMI.md').read_text())
text='''# SET Lab — revisione15 / SET12 rigenerato

## Lista conservata, non ricostruita a memoria

`uploads/ls.ts` è presente:149 SKU unici, coincide byte per byte con il file Git e con l’archivio originale dell’utente. La SHA256 dei byte CRLF differisce da quella normalizzata LF nel registro, ma la normalizzazione restituisce esattamente l’hash storico. Nessuna perdita o sostituzione della lista. Verifica in `analysis/catalog-integrity.json`.

## Stato corrente

**SET12 rigenerato:10 PNG. Recupero SET08–12 completato.** Tutti i150 asset SET01–15 sono disponibili e verificati,147/149 SKU rappresentati. Rimangono solo2 nuovi SKU: `cons-ipa` e `cons-tweezers` (SET16 parziale). Dieci generazioni effettuate in questo turno.

**Consegna finale8 immagini, zero prodotte.** Completare2 consumabili e revisione dei difetti prima delle tavole finali. Le6 prove parziali di questo turno NON sono finali.

Repository privato: https://github.com/ESPNex/set-lab-recovery

La versione corrente mantiene soltanto immagini di catalogo:150 PNG in `originals/` e `generated/`, nessuna immagine raw o diagnostica aggiunta. Dati, script, README e viewerV1 restano. Raw e tavole di analisi locali in `/usr`, esclusi da Git; i vecchi materiali già caricati rimangono nella storia, non riscritta. `/usr` non persistente: fonte di recupero principale è GitHub dopo push verificato. Il bundle nel workspace è storico e non aggiornato.

## Riesame visuale

Riesaminate tutte le15 tavole disponibili,150 asset; riferimento Pro03 e tavola SET11 inclusi. Non equivale a validazione CAD/elettronica. Sei SoC coerenti nei nomi principali, materiali/spessori e microtesto non certificati.

| SKU | Esito |
|---|---|
'''
for sku,note in notes.items():text+=f'| {sku} | {note} |\n'
text+='''
In particolare, Dimensity8300 include sigle extra CPU/GPU non presenti nella richiesta grafica: registrate come non verificate, non elevate a specifiche ufficiali. I due adesivi sono un solo SKU; non si montano colla o liner nello slot frame.

## Coordinate e proporzioni

Riferimento preso dal SET03 Pro, nessuna motherboard inventata. SoC[520,203,226,239] nel crop1286×666; ipotesi UFS[786,342,119,121] con sto-1tb del SET11. Serigrafia SOC/RAM/UFS ambigua: RAM assente, collocazione UFS solo ipotesi grafica. Nessuna compatibilità dei sei SoC con quella memoria dichiarata.

Fit uniforme q=min(slotW/cropW,slotH/cropH), centro coincidente,0° raster. s=min(6.55/1286,7.10/666); X=0.05+(u−1286/2)s, Z=−3.35+(v−666/2)s; Y nominale da `ls.ts`. Cm di simulazione, non dimensioni reali. Telai fit proporzionale dello slot; consumabili pos/size/angle null.

| File SET12 | Crop L,T,R,B px | Centro X,Y,Z cm | Bbox X,Y,Z cm |
|---|---|---|---|
'''
fmt=lambda v:'null' if v is None else ', '.join(f'{x:.3f}' for x in v)
for i in d['items']:
 if i['set']==12:text+=f'| {i["file"]} | {i["crop"]} | {fmt(i["pos"])} | {fmt(i["size"])} |\n'
text+='''
Diagnostica locale `analysis/fit-set12-pro-recovery.jpg`:6 prove, un SoC per volta con memoria SET11. Insieme alle4 prove SET11 formano10 ipotesi parziali, non10 build funzionanti. L’immagine diagnostica non è caricata nel ramo corrente del repo.

## Pipeline e controlli

Raw AI preservati localmente; chroma-key globale graduato smoothstep e despill2px Pillow/NumPy. Nessun rembg/flood fill/ROI manuale aggiuntivo. Alpha postprodotto, non nativo. Tutti10 nuovi PNG RGBA con alpha0–255 e crop validi.

V15 conserva gli altri140 record e hash; sostituiti solo i10 file rigenerati SET12, con supersedesSha256 e record vecchi archiviati. Tutti150 hash verificati. Lista originale intatta. Restano documentati difetti precedenti: frontale03 etichetta errata, RAM06 marca discordante, batteria07 microtesto, SIM08 tre vani, grafite10 fogli ambigui, frame11 catalogo4:3/16:9, fold14 rapporto errato, aperture cover/fotocamere15 non automaticamente coincidenti. eMMC13 non è UFS. Non nascondere difetti nelle finali.

## Prossimo

Produrre IPA99%100ml e pinzette ESD (2 SKU), poi completare audit e8 tavole finali con PNG effettivi, esploso leggibile, alternative separate e riferimenti riutilizzati dichiarati. Nessuna generazione in background. ViewerV1 storico, non aggiornato a tutti i SET.
'''
(r/'LEGGIMI.md').write_text(text)
# Explicit allowlist: never copy dotfiles, credentials or Git configuration.
for folder in ['new_raw','generated','analysis']:
 for p in (r/folder).glob('*'):
  if p.is_file():dst=b/folder/p.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
for p in r.iterdir():
 if p.is_file() and not p.name.startswith('.') and p.suffix in ['.py','.json','.csv','.md']:shutil.copy2(p,b/p.name)
(b/'README.md').write_text(text)
print('All150 asset files verified;catalog149 intact;remaining new SKU2')
