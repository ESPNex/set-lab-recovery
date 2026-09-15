from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,re,math,hashlib,csv
r=Path('/home/user');b=Path('/usr/set-lab');src=(b/'uploads/ls.ts').read_text();parts={};slots={}
for line in src.splitlines():
 m=re.search(r'^  p\("([^"]+)",\s*("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'),\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"',line)
 if m:parts[m[1]]=dict(name=m[2][1:-1],brand=m[3],category=m[4],slot=m[5])
 m=re.search(r'^  (\w+): \{ id: "\w+", name: "([^"]+)", pos: (\[[^]]+\]), size: (\[[^]]+\]), explode: ([-.\d]+)',line)
 if m:slots[m[1]]=dict(name=m[2],pos=json.loads(m[3]),size=json.loads(m[4]),explode=float(m[5]))
d=json.loads((b/'coordinates-v7.json').read_text());d['version']=8;d['status']='SET01-13:130 images,127 represented SKU,22 missing. Final8 composites pending. eMMC not assigned to UFS.'
board=d['boards'][3];new=[];local={};notes={
'soc-ex2500':'SAMSUNG Exynos2500 leggibile, distinto dai2400/2600 precedenti. Nessuna verifica del package fisico o delle memorie supportate.',
'soc-tensor4':'Google TensorG4 leggibile; distinto daG5/G6. Il fit grafico non indica compatibilità con la RAM illustrata.',
'soc-kirin':'HiSilicon Kirin9010 leggibile. Package quasi quadrato e pin-one illustrativo, non pinout verificato.',
'ram-12lp4':'Micron12GB LPDDR4X leggibile, non LPDDR5X. Compatibilità con i tre SoC non verificata; solo collocazione nella sede RAM grafica.',
'sto-32':'Micron32GB eMMC5.1 leggibile. Interfaccia diversa da UFS: nessuna sede eMMC identificata sulle schede mostrate, montaggio non assegnato.',
'sto-256u4':'KIOXIA256GB UFS4.0 leggibile, distinto dal256GB UFS3.1 del SET06.',
'sto-512u31':'Micron512GB UFS3.1 leggibile, distinto da Samsung512GB UFS4.0 del SET08.',
'bat-3500':'BYD3500mAh3.85V leggibile, singola pouch con due linguette. Capacità e tensione non misurate.',
'bat-4000':'ATL4000mAh3.87V leggibile, singola pouch e linguette. Nessuna capacità alternativa rilevata sul fronte.',
'bat-5500':'ATL5500mAh Si-C3.90V leggibile. Singola pouch, distinta dal precedente dual-cell5500mAh; lieve tinta violacea dell’etichetta conservata.'}
for f in sorted((r/'generated').glob('set13-*.png')):
 sku=f.stem[6:];role=parts[sku]['slot'];s=slots[role];im=Image.open(f);box=im.getbbox();w,h=box[2]-box[0],box[3]-box[1];tw,th=s['size'][0],s['size'][2];a=0 if abs(math.log((w/h)/(tw/th)))<=abs(math.log((h/w)/(tw/th))) else 90
 ew,eh=(w,h) if a==0 else(h,w);k=min(tw/ew,th/eh);pos=s['pos'].copy();size=[ew*k,s['size'][1],eh*k];status='proposta grafica nominale; sede non verificata';target=None;ref=None
 if role in ['soc','ram','storage'] and sku!='sto-32':
  ref=board['file'];x,y,sw,sh=board['slots'][role];cx,cy=x+sw/2,y+sh/2;q=min(sw/w,sh/h);target=dict(center=[cx,cy],size=[w*q,h*q],slotRect=[x,y,sw,sh],angle=0,scale=q,reference=ref,referenceBorrowed=True,confidence='serigrafia visibile; pinout non verificato',physicalCompatibilityVerified=False);local[sku]=target
  pos=[.05+(cx-board['raster'][0]/2)*board['scale'],s['pos'][1],-3.35+(cy-board['raster'][1]/2)*board['scale']];size=[w*q*board['scale'],s['size'][1],h*q*board['scale']];a=0;status='fit grafico su PCB GAME riutilizzato; compatibilità non verificata'
 if sku=='sto-32':pos=None;size=None;a=None;status='NON ASSEGNATO: eMMC non è UFS; esporre separatamente'
 row=dict(file=f.name,sku=sku,slot=role,set=13,crop=list(box),sourceSize=list(im.size),pos=pos,size=size,angle=a,status=status,provenance='AI + chroma-key graduato e despill',visualReview=notes[sku],boardLocal=target,boardReference=ref)
 if role=='storage':row['interface']='eMMC5.1' if sku=='sto-32' else ('UFS4.0' if sku=='sto-256u4' else 'UFS3.1')
 new.append(row)
d['items']+=new;d.setdefault('setBoardReferences',{})['13']=dict(file=board['file'],borrowed=True,notNewMotherboard=True,status='riferimento grafico, nessuna compatibilità di bus o BGA accertata')
socs=['soc-ex2500','soc-tensor4','soc-kirin'];ufs=['sto-256u4','sto-512u31'];combos=[dict(id=f'13__{soc}__ram-12lp4__{sto}',board=board['file'],boardBorrowed=True,soc=soc,ram='ram-12lp4',storage=sto,excludedStorage='sto-32',status='graphic composition only, electrical compatibility NOT VERIFIED') for soc in socs for sto in ufs]
d['set13Compositions']=combos;d['defaultSet13Selection']={'soc':'soc-ex2500','ram':'ram-12lp4','storage':'sto-256u4','battery':'bat-4000','status':'illustrative only'}
present={i['sku'] for i in d['items']};missing=[dict(id=k,**v) for k,v in parts.items() if k not in present];plan=json.loads((b/'catalog-plan.json').read_text());plan['pendingLots']=[x for x in plan['pendingLots'] if x['set']>13];plan.update(availableAssets=130,representedSkuCount=127,missingSkuCount=22,finalImagesRequested=8)
assert len(d['items'])==130 and len(present)==127 and len(missing)==22
assert {s for lot in plan['pendingLots'] for s in lot['skus']}=={x['id'] for x in missing}
finals=json.loads((b/'final-compositions-plan.json').read_text());assert finals['requestedCount']==8 and finals['createdCount']==0
for name,obj in [('coordinates-v8.json',d),('catalog-missing.json',missing),('catalog-plan.json',plan),('final-compositions-plan.json',finals)]: (r/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
with (r/'catalog-status.csv').open('w',newline='') as f:
 wr=csv.writer(f);wr.writerow(['sku','name','slot','status','files','planned_set'])
 for sku,v in parts.items():
  files=[i['file'] for i in d['items'] if i['sku']==sku];lot=next((l['set'] for l in plan['pendingLots'] if sku in l['skus']),'');wr.writerow([sku,v['name'],v['slot'],'GENERATED_REVIEW_REQUIRED' if sku=='board-rf' else ('REPRESENTED' if files else 'NOT_GENERATED'),';'.join(files),lot])
checks=[]
for sku,t in local.items():
 sw,sh=t['slotRect'][2:];w,h=t['size'];assert w<=sw+1e-8 and h<=sh+1e-8
 checks.append(dict(sku=sku,center=t['center'],drawSize=t['size'],marginX=max(0,(sw-w)/2),marginY=max(0,(sh-h)/2),contained=True,uniformScale=True))
boardim=Image.open(b/'generated'/board['file']).convert('RGBA');boardim=boardim.crop(boardim.getbbox());W,H=boardim.size;sheet=Image.new('RGB',(3*W,2*(H+95)),'#14202b');dr=ImageDraw.Draw(sheet)
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
except:font=None
for j,c in enumerate(combos):
 im=boardim.copy()
 for sku in [c['soc'],c['ram'],c['storage']]:
  ai=Image.open(r/f'generated/set13-{sku}.png').convert('RGBA');ai=ai.crop(ai.getbbox());t=local[sku];w,h=[round(v) for v in t['size']];ai=ai.resize((w,h),Image.Resampling.LANCZOS);cx,cy=t['center'];im.alpha_composite(ai,(round(cx-w/2),round(cy-h/2)))
 x=(j%3)*W;y=(j//3)*(H+95);sheet.paste(im,(x,y+72),im);dr.text((x+15,y+10),c['soc']+' + ram-12lp4 + '+c['storage'],fill='#9be6cb',font=font);dr.text((x+15,y+39),'PCB SET07 riutilizzato | SOLO FIT GRAFICO | eMMC esclusa',fill='#ffc568',font=font)
sheet.thumbnail((2200,1250));sheet.save(r/'analysis/fit-set13-game-reference.jpg')
manifest={}
for row in d['items']:
 p=(r/'generated'/row['file']) if row['set']==13 else((b/'generated'/row['file']) if row['set']>=7 else(b/'originals'/row['file']));assert p.exists();manifest[('generated/' if row['set']>=7 else 'originals/')+row['file']]=hashlib.sha256(p.read_bytes()).hexdigest()
assert len(set(manifest.values()))==130
previous=json.loads((b/'asset-sha256-v7.json').read_text());assert all(manifest[k]==v for k,v in previous.items())
(r/'asset-sha256-v8.json').write_text(json.dumps(manifest,indent=2));(r/'analysis/revision8-checks.json').write_text(json.dumps(dict(counts={st:sum(i['set']==st for i in d['items']) for st in range(1,14)},represented=127,missing=22,old120HashesUnchanged=True,fits=checks,newCompositions=combos,finalRequiredCount=8,finalCreatedCount=0,emmcNotMounted=True,rawPreserved=True),ensure_ascii=False,indent=2))
old=(b/'LEGGIMI.md').read_text();(r/'analysis/LEGGIMI-v7.md').write_text(old);fmt=lambda v:'—' if v is None else ', '.join(f'{x:.3f}' for x in v)
text='''# SET Lab — LEGGIMI corrente, revisione 8

**SET 01–13 · 130 immagini · 127/149 SKU rappresentati · 22 SKU ancora mancanti**

## Stato reale e consegna finale

Creato il **SET 13 completo di 10 immagini**: tre SoC, RAM12GB LPDDR4X, tre memorie (due UFS e una eMMC) e tre batterie. Riesaminate tutte le tavole SET01–12, i10 nuovi asset e il PCB GAME in dettaglio. Le etichette principali corrispondono al catalogo; non si dichiarano verificate le specifiche elettroniche o meccaniche.

La consegna finale resta **8 immagini composite**, non20: una per coppia di SET, usando immagini effettive, viste esplose, varianti separate e riferimenti riutilizzati dichiarati. Tutte le otto tavole finali sono ancora DA PRODURRE dopo il completamento del catalogo. I test di fit di questa revisione non sono le immagini finali.

Il catalogo resta incompleto:22 SKU da generare, prossimo lotto SET14. Il limite dello strumento è10 generazioni per turno e non c’è produzione in background.

## ZIP incrementale e posizione dei file

Scaricare **`set13-update.zip` dal workspace** ed estrarlo nella cartella del primo `set-lab-session.zip` e degli aggiornamenti SET08–12, unendo le sottocartelle.

La copia di lavoro è in `/usr/set-lab`; gli ZIP precedenti sono in `/usr/set-lab/downloads`. **/usr non è persistente tra le sessioni**: conservare gli archivi scaricati. Nel workspace restano il LEGGIMI e il nuovo ZIP per il recupero.

Contenuto dell’aggiornamento:
- `new_raw/set13-*.png`:10 output AI intatti; `generated/set13-*.png`:10 PNG con alpha elaborato;
- `analysis/set13.jpg`, metadati, log e `fit-set13-game-reference.jpg`;
- `coordinates-v8.json`:130 record, cinque schede e riferimenti a schede riutilizzate;
- `catalog-status.csv`, `catalog-missing.json`, `catalog-plan.json`, piano finale8 invariato;
- `asset-sha256-v8.json`, script e `uploads/ls.ts` invariato;
- questo LEGGIMI e `analysis/LEGGIMI-v7.md` storico.

Il viewer resta quello storico SET01–06: in questo turno non viene aggiornato né testato il renderer3D.

## Pipeline realmente applicata

Generazione separata dei10 asset su magenta. Scontorno **Pillow + NumPy: chroma-key globale graduato e despill**. Nessun rembg, flood fill o segmentatore AI.

`e=min(R,B)-G`; candidato con R>100, B>100, e>35; `t=clamp((e−35)/75,0,1)`; `k=t²(3−2t)`; alpha finale=alpha originale×(1−k). Alpha<3 azzerato, riduzione della frangia magenta e despill entro2px dalla trasparenza. RGB azzerato dove alpha=0. Nel SET13 non sono state applicate maschere ROI manuali.

Alpha postprodotto, non nativo. Le tinte interne all’oggetto, per esempio l’etichetta leggermente violacea della batteria5500, non sono state cancellate per simulare un materiale diverso. I120 asset precedenti restano invariati nei loro hash.

## Analisi visuale SET13

| File | Esito |
|---|---|
'''
for row in new:text+=f'| {row["file"]} | {row["visualReview"]} |\n'
text+='''
Le batterie sono tre alternative singole, non celle da collegare automaticamente tra loro:3500mAh3.85V,4000mAh3.87V,5500mAhSi-C3.90V. Non si deducono capacità reali, soglie di ricarica, corrente o dimensioni dalle etichette illustrate. Le linguette incluse nel bbox possono ridurre la dimensione visiva del corpo quando il fit usa l’intero ritaglio.

## eMMC: non trattarla come UFS

`set13-sto-32.png` rappresenta **32GB eMMC5.1**, non UFS. L’interfaccia differisce; nessuna sede eMMC corrispondente è identificata nelle immagini delle motherboard. La voce usa lo slot generico `storage` in `ls.ts`, ma questo non basta per assegnarla a una piazzola serigrafata UFS.

Nel JSON V8: `interface=eMMC5.1`, `pos=null`, `size=null`, `angle=null`, `boardLocal=null`, `boardReference=null`. Resta nell’inventario/esploso. Non convertire null in zero e non farla diventare una terza alternativa montata nelle prove UFS.

## Riferimento motherboard e coordinate

Si riutilizza **`set07-board-game.png`**, senza creare una sesta scheda. Raster ritagliato1272×639px dal crop `[68,66,1340,705]` del PNG. Le sedi hanno etichette distinte, ma nessun pinout verificato.

| Sede | Rect u,v,w,h px | Centro u,v px |
|---|---|---|
| SoC | [225,209,229,228] | [339.5,323.0] |
| RAM | [585,185,214,252] | [692.0,311.0] |
| UFS | [938,123,213,241] | [1044.5,243.5] |

Fit uniforme: `q=min(slot_w/crop_w,slot_h/crop_h)`; centro coincidente, angolo2D0°. La collocazione di LPDDR4X accanto ai SoC illustrati è **soltanto una prova grafica**, non una configurazione supportata: il fatto che due rettangoli combacino non verifica controller RAM, generazione LPDDR o terminali BGA.

### Fit dei sei package assegnati graficamente

| SKU | Centro u,v px | Disegno W×H px | Margine X/Y per lato px |
|---|---|---|---|
'''
for c in checks:text+=f'| {c["sku"]} | {fmt(c["center"])} | {fmt(c["drawSize"])} | {c["marginX"]:.3f} / {c["marginY"]:.3f} |\n'
text+='''
### Sei composizioni diagnostiche

3SoC×2UFS, RAM `ram-12lp4` comune. Le immagini non costituiscono assemblaggi funzionanti certificati e non includono il montaggio delle tre batterie. L’eMMC è esclusa. I chip alternativi non vengono sovrapposti contemporaneamente.

| N. | SoC | RAM | UFS |
|---|---|---|---|
'''
for j,c in enumerate(combos,1):text+=f'| {j} | {c["soc"]} | {c["ram"]} | {c["storage"]} |\n'
text+='''
`analysis/fit-set13-game-reference.jpg` documenta questi test. La compatibilità elettrica, la dimensione reale dei package e le connessioni non sono state verificate.

### Crop e coordinate nominali SET13

Cm **nominali di simulazione**: X destra, Y spessore, Z verso il basso del telefono. Bbox dopo rotazione; angolo positivo orario2D, non yaw Three.js collaudato. Per il GAME: `s=min(6.55/1272,7.10/639)`, `X=0.05+(u−1272/2)*s`, `Z=−3.35+(v−639/2)*s`; Y dagli slot di `ls.ts`. Batterie: centro nominale dello slot e fit proporzionale, non vasca fisica riconosciuta.

| File | Crop [L,T,R,B] px | Centro X,Y,Z cm | Bbox X,Y,Z cm | ° | Stato |
|---|---|---|---|---:|---|
'''
for row in new:text+=f'| {row["file"]} | {row["crop"]} | {fmt(row["pos"])} | {fmt(row["size"])} | {row["angle"] if row["angle"] is not None else "—"} | {row["status"]} |\n'
text+='''
I precedenti120 record sono preservati nel JSON V8. Rimangono nulli i montaggi di accessori, RAM/UFS del Lite e storage del SET10 sul RF. L’ipotesi UFS sul Pro resta documentata come tale, non viene promossa a misura certa.

## Riesame e correzioni ancora pendenti

- SET01: bande bianche USB nel raw, ritaglio centrale già registrato; RAM con proporzioni diverse dalla sede.
- SET03: frontale32MP con stampa52MP e sedi RAM/UFS non univoche sul Pro.
- SET06: RAM16 Samsung nel raster, SK hynix nel catalogo; Lite privo di sedi RAM/UFS riconoscibili.
- SET07: microtesto contraddittorio batteria6000 e geometria PCB diversa dal prompt.
- SET08: UWB/NFC non equivale a Wi-Fi/5G.
- SET09: componenti all’interno della piazzola UFS RF, montaggio automatico tuttora bloccato.
- SET10: dicitura2xLRA ripetuta su due involucri, non quattro attuatori.
- SET11: telaio classico con vista composita e apertura ripulita via ROI alpha; contraddizione4:3/16:9 nel catalogo.
- SET12: supporto rosato delle linguette conservato, traslucenza non fisica; materiali dei telai non verificabili.

Questi difetti non sono stati nascosti mediante rigenerazione o sovrapposizione in questo turno. Le otto immagini finali useranno i componenti reali dell’inventario, con le limitazioni esplicite.

## Piano residuo e finale8

**127 SKU rappresentati su149;22 mancanti.** I130 file comprendono i tre alias/duplicati di rappresentazione già documentati. Nessuna tavola finale è stata prodotta ancora.

| Lotto | SKU | Stato |
|---|---|---|
'''
for lot in plan['pendingLots']:text+=f'| {lot["set"]:02}'+(' (2/10, residuo)' if not lot['completeTenAssetSet'] else '')+' | '+', '.join('`'+s+'`' for s in lot['skus'])+' | NON GENERATO |\n'
text+='''
Restano due lotti da10 e due SKU finali. Non si inventano otto SKU per completare artificialmente il lotto16. L’ultima tavola finale potrà mostrare i pezzi disponibili e i riferimenti presi da altri SET, distinti dai nuovi articoli.

La richiesta finale8, non20, resta nel piano attivo: coppie01–02,03–04,05–06,07–08,09–10,11–12,13–14,15–16. Cinque motherboard di catalogo; nelle ultime tre tavole riuso dichiarato. Vista esplosa leggibile con alternative e accessori separati, niente compatibilità inventate.

## Verifiche eseguite

-13SET da10:130 file con130 hash distinti; vecchi120 invariati.
-10 nuovi PNG con alpha0–255 e crop validi; proporzioni conservate.
-Sei package con fit uniforme nelle sedi serigrafate GAME; eMMC isolata e non assegnata.
-Sei prove raster prodotte per controllo visivo; nessuna certificazione elettronica.
-Piano residuo esattamente22 SKU, senza duplicati; finale8 pianificata, zero tavole finali prodotte.
'''
text=text.replace('\n-13SET','\n- 13 SET').replace('\n-10 nuovi','\n- 10 nuovi').replace('\n-Sei','\n- Sei').replace('\n-Piano','\n- Piano')
(r/'LEGGIMI.md').write_text(text)
print('130 assets /127 SKUs /22 pending; final8. README chars:',len(text))
