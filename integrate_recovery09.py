from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,re,hashlib,shutil,itertools
r=Path('/home/user');b=Path('/usr/set-lab');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.loads((b/'coordinates-v11.json').read_text());man=json.loads((b/'asset-sha256-v11.json').read_text());src=(b/'uploads/ls.ts').read_text();slots={}
for l in src.splitlines():
 m=re.search(r'^  (\w+): \{ id: "\w+", name: "([^"]+)", pos: (\[[^]]+\]), size: (\[[^]]+\]), explode: ([-.\d]+)',l)
 if m:slots[m[1]]=dict(pos=json.loads(m[3]),size=json.loads(m[4]),explode=float(m[5]))
(r/'analysis/set09-original-records.json').write_text(json.dumps([i for i in d['items'] if i['set']==9],ensure_ascii=False,indent=2));(r/'analysis/set09-original-board.json').write_text(json.dumps(d['boards'][4],indent=2))
notes={'back-green':'LuxGuard verde salvia satinato, fori alpha. Disposizione non verificata rispetto al periscopio.', 'bat-7000':'BYD7000mAh3.95V Si-C leggibile; nessuna capacità alternativa visibile.', 'board-rf':'SOC,RAM,UFS ben distinti e liberi da passivi; array UFS concentrico illustrativo, non pinout reale. Nome scheda ripetuto due volte.', 'cam-peri2':'SONY200MP6xOIS leggibile; microtesto aggiuntivo decorativo non certificato. Ingresso quadrangolare, non validato rispetto ai fori cover.', 'camf-12':'SONY12MP leggibile; riflesso blu e lieve alone/bordo non fisico. Apertura display non validata come misura.', 'disp-oled63':'BOE OLED6.3,120Hz,1080x2400 leggibili, punch centrale e flex inferiore.', 'frame-mag':'Telaio Vertex Qi2 con anello inferiore e finestre alpha; nessuna misura N52/lega certificabile.', 'glass-zaf':'CrystalLux Synthetic Sapphire leggibile, punch superiore; lastra opaca illustrativa, non trasparenza ottica.', 'spk-stereo-bot':'Due driver, Goertek2x1.1W leggibile; nessuna misura acustica.', 'usb-dp':'Amphenol DP2.1 8K60 leggibile; residuo violaceo sul metallo e vista non strettamente ortografica.'}
for i in d['items']:
 if i['set']==9:
  im=Image.open(r/'generated'/i['file']);box=im.getbbox();w,h=box[2]-box[0],box[3]-box[1];s=slots[i['slot']];q=min(s['size'][0]/w,s['size'][2]/h);blocked=i['slot'] in ['cameraRear','cameraFront'];prev=man['generated/'+i['file']];man['generated/'+i['file']]=sha(r/'generated'/i['file'])
  i.update(crop=list(box),sourceSize=list(im.size),pos=None if blocked else s['pos'],size=None if blocked else [w*q,s['size'][1],h*q],angle=None if blocked else 0,boardLocal=None,boardReference=None,status='SEPARATO: allineamento ottico non verificato' if blocked else 'fit nominale, non ingombro fisico verificato',assetRevision='recovery-r1',supersedesSha256=prev,visualReview=notes[i['sku']],physicalCompatibilityVerified=False,provenance='AI regenerated recovery-r1; smooth alpha chroma-key and despill')
  assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
 if i['set']==10 and i['slot'] in ['soc','ram','storage']:
  i.update(pos=None,size=None,angle=None,boardLocal=None,boardReference=None,status='STALE: asset da rigenerare e coordinate da ricalcolare sul nuovo RF')
rfim=Image.open(r/'generated/set09-board-rf.png');box=rfim.getbbox();W,H=box[2]-box[0],box[3]-box[1];sc=min(6.55/W,7.10/H)
d['boards'][4]=dict(pair=5,file='set09-board-rf.png',crop=list(box),raster=[W,H],center=[.05,.145,-3.35],scale=sc,size=[W*sc,.14,H*sc],yaw=0,slots={'soc':[162,131,341,350],'ram':[601,127,206,356],'storage':[899,180,216,252]},slotPlacementAllowed={'soc':True,'ram':True,'storage':True},slotStatus={k:'BARE GRAPHIC SEAT; physical/electrical fit NOT verified' for k in ['soc','ram','storage']},assetRevision='recovery-r1',notes='Old occupied UFS defect absent in new raster. Gold dots only, pinout not validated.')
# Refit SET08 to original Game board restored and hash verified.
game=d['boards'][3];fits=[]
for i in d['items']:
 if i['set']!=8:continue
 im=Image.open(b/'generated'/i['file']);box=im.getbbox();w,h=box[2]-box[0],box[3]-box[1];s=slots[i['slot']]
 if i['slot'] in ['soc','ram','storage']:
  x,y,sw,sh=game['slots'][i['slot']];q=min(sw/w,sh/h);cx,cy=x+sw/2,y+sh/2;size=[w*q,h*q];t=dict(center=[cx,cy],size=size,slotRect=[x,y,sw,sh],angle=0,scale=q,reference=game['file'],physicalCompatibilityVerified=False)
  i.update(boardLocal=t,boardReference=game['file'],pos=[.05+(cx-game['raster'][0]/2)*game['scale'],s['pos'][1],-3.35+(cy-game['raster'][1]/2)*game['scale']],size=[size[0]*game['scale'],s['size'][1],size[1]*game['scale']],angle=0,status='REFIT R1: graphic containment only on recovered Game')
  assert size[0]<=sw+1e-7 and size[1]<=sh+1e-7;fits.append({'sku':i['sku'],**t})
 elif i['sku']!='sim-hybrid':
  q=min(s['size'][0]/w,s['size'][2]/h);i.update(pos=s['pos'],size=[w*q,s['size'][1],h*q],angle=0,status='nominal proportional fit, not verified physical mount')
combos=[];boardim=Image.open(b/'generated'/game['file']).convert('RGBA');boardim=boardim.crop(boardim.getbbox());W,H=boardim.size;sheet=Image.new('RGB',(W*2,(H+65)*2),'#14202b');dr=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
for j,(soc,ram) in enumerate(itertools.product(['soc-8s','soc-d9400'],['ram-24','ram-8x'])):
 c={'soc':soc,'ram':ram,'storage':'sto-512','board':game['file'],'status':'R1 graphic fit; NOT electrical validation'};combos.append(c);im=boardim.copy()
 for sku in [soc,ram,'sto-512']:
  row=next(i for i in d['items'] if i['set']==8 and i['sku']==sku);t=row['boardLocal'];chip=Image.open(b/'generated'/row['file']).convert('RGBA');chip=chip.crop(chip.getbbox());w,h=map(round,t['size']);chip=chip.resize((w,h),Image.Resampling.LANCZOS);cx,cy=t['center'];im.alpha_composite(chip,(round(cx-w/2),round(cy-h/2)))
 x=(j%2)*W;y=(j//2)*(H+65);dr.text((x+15,y+10),soc+' + '+ram+' + sto-512 | SOLO FIT GRAFICO R1',fill='#97e7c7',font=font);sheet.paste(im,(x,y+60),im)
sheet.thumbnail((2100,1400));sheet.save(r/'analysis/fit-set08-recovery-game.jpg')
d['pair0708Compositions']=combos;d['pair0708CompositionsStatus']='REFIT_RECOVERY_R1: reviewed graphically, not technical compatibility';d['pair0910CompositionsStatus']='STALE_PENDING_SET10_REGENERATION';d.update(version=12,status='Original70 restored and hash verified; SET08-09 regenerated; locally120 assets. Pending regeneration SET10-12:30. Pending new SKU2. Final0/8.',availabilityNote='Available SET01-09,13-15; SET10-12 original assets lost, not yet regenerated.')
rec=json.loads((b/'recovery-plan.json').read_text());rec.update(regeneratedSets=[8,9],pendingSets=[x for x in rec['pendingSets'] if x['set']>9],awaitingUserArchives=[],localAssetCount=120,restoredOriginalAssets=70,originalArchiveSource='https://files.catbox.moe/ujc2ul.zip')
plan=json.loads((b/'catalog-plan.json').read_text());plan['locallyAvailableAssetCount']=120
for c in plan['qualityCorrections']:
 if c['file']=='set09-board-rf.png':c.update(status='RESOLVED_IN_RECOVERY_R1',resolution='Regenerated bare UFS array; no passives visible; no pinout verification')
finals=json.loads((b/'final-compositions-plan.json').read_text());finals['blockingReasons']=['Regenerate SET10-12 (30 images)','Generate remaining2 consumables','Resolve or separately display documented defects; review final graphics'];finals['status']='PENDING_REMAINING_CATALOG_AND_RECOVERY'
for name,obj in [('coordinates-v12.json',d),('asset-sha256-v12.json',man),('recovery-plan.json',rec),('catalog-plan.json',plan),('final-compositions-plan.json',finals)]: (r/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
available=[];absent=[]
for key,h in man.items():
 p=(r/key) if (r/key).exists() else b/key
 if p.exists():assert sha(p)==h,key;available.append(key)
 else:absent.append(key)
assert len(available)==120 and len(absent)==30
(r/'analysis/current-availability.json').write_text(json.dumps({'availableCount':120,'missingCount':30,'missing':absent},indent=2));(r/'analysis/recovery-set09-checks.json').write_text(json.dumps({'hashesVerified':120,'multimodalContactSheets':[1,2,3,4,5,6,7,8,9,13,14,15],'nativeBoardsReviewed':['Game07','RF09-R1'],'set08Fits':fits,'rf09BareSeats':True,'finalCreatedCount':0},indent=2));(r/'analysis/LEGGIMI-v11.md').write_text((b/'LEGGIMI.md').read_text())
text='''# SET Lab — revisione12 / recupero SET09

## Risultato

**Archivio originale SET01–07 recuperato:70 PNG, tutti con hash identici ai registri storici.** Fonte https://files.catbox.moe/ujc2ul.zip, copia in `/usr/set-lab/downloads/recovered-originals-01-07.zip`. Metadati sovrapposti dell’archivio messi da parte, non sovrascritti ai registri attuali.

**SET09 rigenerato:10 immagini nuove. SET08–09 completati come recupero; restano SET10–12,30 immagini.** Restano anche2 SKU mai generati: IPA e pinzette. Limite10 generazioni del turno raggiunto.

Disponibili fisicamente120 immagini (SET01–09,13–15), tutte verificate contro il manifest corrente. Registro storico150 file/147 SKU, non150 file disponibili. Otto tavole finali confermate, zero prodotte.

## Analisi multimodale

Riesaminate le12 tavole disponibili: SET01–09 e13–15,120 immagini complessive. Game07 e nuovo RF09 anche in dettaglio. Non dichiarato riesame dei30 asset SET10–12 mancanti.

Rilievi storici confermati: USB01 pannelli bianchi nel raw; frontale03 stampa52MP anziché32MP; RAM16 del06 marchio Samsung rispetto a catalogo SK hynix; Lite05 senza sedi RAM/UFS chiare; batteria07 microtesto contraddittorio. Recupero08 SIM con tre vani; fold14 rapporto geometrico errato; cover15 e fotocamere non corrispondono automaticamente. Questi difetti non vengono nascosti sotto altri pezzi.

## Nuovo SET09

| SKU | Esito |
|---|---|
'''
for sku,note in notes.items():text+=f'| {sku} | {note} |\n'
text+='''
La piazzola UFS del nuovo RF è libera, a differenza del raster perduto: il precedente blocco per passivi è risolto SOLO per questa rigenerazione. Le griglie sono illustrative, non pinout. I chip SET10 saranno collocati dopo rigenerazione, non usando coordinate vecchie.

## Coordinate RF09-R1

Raster ritagliato1249×613, crop[82,79,1331,692]. Centro nominale[0.05,0.145,-3.35]cm, scala=min(6.55/1249,7.10/613). X destra,Y strati,Z lunghezza. Non misure CAD.

| Sede | Rect u,v,w,h nel crop px |
|---|---|
| SoC | [162,131,341,350] |
| RAM | [601,127,206,356] |
| UFS | [899,180,216,252] |

`coordinates-v12.json`: board aggiornata; SoC/RAM/storage SET10 con montaggi nulli perché i raster mancano e la geometria RF è cambiata. Camere SET09 isolate per mancata verifica aperture. Altri pezzi fit uniforme nominale nei rispettivi slot, non prova fisica.

| File SET09 | Crop L,T,R,B | Centro X,Y,Z cm | Bbox X,Y,Z cm |
|---|---|---|---|
'''
fmt=lambda v:'null' if v is None else ', '.join(f'{x:.3f}' for x in v)
for i in d['items']:
 if i['set']==9:text+=f'| {i["file"]} | {i["crop"]} | {fmt(i["pos"])} | {fmt(i["size"])} |\n'
text+='''
## SET08 ricalcolato sul Game originale

Recuperato il PNG Game07 identico, rifatti5 fit:2SoC,2RAM,1UFS. q=min(sedeW/cropW,sedeH/cropH), centro coincidente, angolo0°, nessuna deformazione. Quattro prove2SoC×2RAM con sto-512 in `analysis/fit-set08-recovery-game.jpg`. Solo contenimento grafico, NON compatibilità dei bus o BGA. Accessori fit nominale; SIM resta null per geometria difettosa.

| SKU | Centro u,v px | Disegno W,H px |
|---|---|---|
'''
for f in fits:text+=f'| {f["sku"]} | {fmt(f["center"])} | {fmt(f["size"])} |\n'
text+='''
## Pipeline e backup

Raw AI intatti; PNG alpha postprodotto con chroma-key globale smoothstep e despill2px, nessun rembg/flood fill o nuova ROI manuale. Vetri opachi illustrativi: non trasparenza ottica reale.

Git locale in `/usr/set-lab`; GitHub NON autenticato e push NON eseguito. `/usr` non persistente: non è una garanzia di backup remoto.

Per mantenere il checkpoint del workspace entro la capacità disponibile, il bundle Git contiene direttamente i50 asset generati SET08–09,13–15 con raw e metadati; gli originali70 recuperati rimangono un archivio esterno collegato tramite URL e SHA256. `restore_originals.py` li ripristina senza sovrascrivere file differenti e controlla gli hash. **Il bundle da solo non contiene i70 PNG originali**: conservare anche lo ZIP Catbox originale. I file sono tutti presenti in `/usr` in questa sessione. Dopo autorizzazione GitHub si potrà caricare anche il materiale originale nel repository remoto.

`set-lab-recovery.bundle` aggiornato è il checkpoint Git locale scaricabile. Viewer V1 recuperato nell’archivio originale, non aggiornato ai nuovi SET. Nessuna attività di generazione in background.

## Prossimo

SET10: hap-dual,ram-18,ram-32,soc-8e2,soc-dim95,soc-ten6,sto-1tb41,sto-2tb,th-cu,th-gr2. Poi SET11–12 e2 consumabili; controlli finali ed8 tavole con PNG effettivi, alternative separate e riferimenti riutilizzati dichiarati.
'''
(r/'LEGGIMI.md').write_text(text)
for p in [p for p in r.rglob('*') if p.is_file() and p.suffix not in ['.zip','.bundle']]:
 dst=b/p.relative_to(r);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
print('120 files verified; SET09 regenerated; SET08 refit4 diagnostics')
