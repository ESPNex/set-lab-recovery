from pathlib import Path
from PIL import Image
import json,hashlib,shutil,csv
r=Path('/home/user');b=Path('/usr/set-lab');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.loads((b/'coordinates-v10.json').read_text());man=json.loads((b/'asset-sha256-v10.json').read_text());old=[i.copy() for i in d['items'] if i['set']==8];(r/'analysis/set08-original-records.json').write_text(json.dumps(old,ensure_ascii=False,indent=2))
notes={'ant-uwb':'NXP UWB+NFC leggibile; fori scontornati. Non Wi-Fi/5G; microtesto decorativo non validato.','sim-hybrid':'Luxshare HYBRID leggibile, ma sono raffigurati TRE vani anziché due: geometria da correggere; non simulare un carrello fisico valido.','hap-z':'Nidec Z-axis leggibile, un solo attuatore rotondo con flex.','mic-1':'Knowles MEMS leggibile, un microfono con foro acustico.','ram-24':'Samsung24GB LPDDR5X10667MHz leggibile; package quasi quadrato, non misura BGA.','ram-8x':'Micron8GB LPDDR5X8533MHz leggibile.','soc-8s':'Qualcomm Snapdragon8sGen4 leggibile, non Elite.','soc-d9400':'MediaTek Dimensity9400 leggibile.','sto-512':'Samsung512GB UFS4.0 leggibile.','th-coil':'CoolCo VC+Qi2 15W leggibile; bobina e piastra in vista top, materiali non certificati.'}
for i in d['items']:
 if i['set']!=8:continue
 f=r/'generated'/i['file'];im=Image.open(f);assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
 prior=man['generated/'+i['file']];man['generated/'+i['file']]=sha(f)
 i.update(crop=list(im.getbbox()),sourceSize=list(im.size),pos=None,size=None,angle=None,boardLocal=None,boardReference=None,status='REGENERATED: coordinate da ricalcolare dopo ripristino PCB SET07',provenance='AI regenerated recovery R1; original lost; global chroma-key and despill',visualReview=notes[i['sku']],assetRevision='recovery-r1',supersedesSha256=prior,physicalCompatibilityVerified=False)
d.update(version=11,status='Recovery SET08 regenerated10. SET09-12 need40 regenerations. SET01-07 await upload. 40 local PNG,150 historical records,2 catalog SKU still ungenerated.')
d['pair0708CompositionsStatus']='STALE_AFTER_SET08_REGENERATION: recalculate from new crops after SET07 recovery';d['availabilityNote']='Local SET08 recovery-r1 and SET13-15. Original SET08 artwork unavailable.'
recovery={'regeneratedSets':[8],'pendingSets':[{ 'set':s,'skus':[i['sku'] for i in d['items'] if i['set']==s]} for s in range(9,13)],'awaitingUserArchives':[{'sets':[1,2,3,4,5,6],'count':60},{'sets':[7],'count':10}],'pendingNewSku':['cons-ipa','cons-tweezers'],'localAssetCount':40,'historicalRecords':150,'newFinalImagesCreated':0,'allFinalImagesRequired':8}
for name,obj in [('coordinates-v11.json',d),('asset-sha256-v11.json',man),('recovery-plan.json',recovery)]: (r/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
finals=json.loads((b/'final-compositions-plan.json').read_text());finals['blockingReasons']=['Upload original SET01-07','Regenerate SET09-12 (40 PNG)','Generate final2 consumables','Recompute regenerated part coordinates; inspect all originals and assemblies'];(r/'final-compositions-plan.json').write_text(json.dumps(finals,ensure_ascii=False,indent=2))
plan=json.loads((b/'catalog-plan.json').read_text());plan['locallyAvailableAssetCount']=40;plan['recoveryPlan']='recovery-plan.json';plan['qualityCorrections'].append({'file':'set08-sim-hybrid.png','issue':'Recovery R1 depicts three bays rather than two hybrid bays','blocks':'validated tray geometry'});(r/'catalog-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2))
with (b/'catalog-status.csv').open(newline='') as f:rows=list(csv.DictReader(f))
for i in rows:
 if i['sku'] in notes:i['status']='REGENERATED_REVIEW_REQUIRED'
with (r/'catalog-status.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
(r/'analysis/recovery-set08-checks.json').write_text(json.dumps({'generated10':True,'sheetMultimodallyReviewed':True,'antennaFullResolutionReviewed':True,'newAlphaAndCropValidated':True,'oldFilesNotClaimedRecovered':True,'newCoordinatesPendingPCB':True,'regenerationCountRemaining':40,'old30AvailableHashesVerified':all(sha(b/k)==v for k,v in man.items() if (b/k).exists()),'finalsCreated':0},indent=2))
(r/'analysis/LEGGIMI-v10.md').write_text((b/'LEGGIMI.md').read_text())
text='''# SET Lab — recupero R1 / revisione 11

## Stato verificato

L’utente conserva SET01–06 e SET07, da ricaricare. Richiesta attiva: rigenerare SET08–12 (50 immagini), repository Git con login web, poi completare catalogo e8 tavole finali.

**Questo turno: SET08 rigenerato,10 immagini nuove. Restano SET09–12:40 immagini da rigenerare.** Le nuove immagini non sono gli originali perduti e hanno hash/provenienza distinti. Rimangono anche IPA e pinzette ESD,2 SKU mai generati. Limite della pipeline10 generazioni per turno; nessuna produzione in background.

Disponibilità effettiva:40 PNG elaborati e40 raw (SET08-R1,13,14,15). Registro storico150 immagini/147 SKU; catalogo149 SKU. Questi conteggi NON implicano che tutti i file siano presenti. `recovery-plan.json` separa rigenerazioni, archivi da ricaricare e SKU mai prodotti.

## Git e backup

Repository Git locale preparato in `/usr/set-lab`, con esclusione di downloads e credenziali. Autorizzazione GitHub CLI via https://github.com/login/device; nessun token/password richiesto in chat. Il codice temporaneo è mostrato in conversazione, non salvato nel repository. Il repository remoto privato `set-lab-recovery` sarà creato solo dopo autorizzazione riuscita: NON dichiarare un push completato senza verificarlo.

**Backup persistente: `set-lab-recovery.bundle` nel workspace**, contenente la storia Git e tutti i40 raw/PNG ora disponibili, metadati e script. Non è solo un aggiornamento incrementale. Recupero: `git clone set-lab-recovery.bundle set-lab-recovery`. `/usr` non è persistente: il bundle è essenziale finché il push remoto non è verificato.

Gli ZIP precedenti rimangono in `/usr/set-lab/downloads`, fuori da Git. Il bundle conserva i loro asset SET13–15, ma NON inventa i SET01–07 e09–12 mancanti. Non sono inclusi segreti di autenticazione.

## Riesame SET08 nuovo

Tavola dei10 asset letta multimodalmente; antenna letta anche a piena risoluzione. Etichette principali SoC, RAM, UFS, haptics, microfono, Qi2 corrette. Nessuna affermazione di capacità, prestazioni o conformità fisica misurata.

| SKU | Esito |
|---|---|
'''
for sku,note in notes.items():text+=f'| {sku} | {note} |\n'
text+='''
Il carrello SIM ha un difetto geometrico nuovo documentato: tre vani. Rimane da correggere o isolare come illustrazione, non si nasconde il problema per accelerare l’assemblaggio.

## Coordinate e pipeline

Chroma-key globale graduato e despill Pillow/NumPy, stesso processore dei lotti recenti: nessun rembg/flood fill, nessuna trasparenza nativa dichiarata, raw intatti. Tutti10 alpha0–255 e bbox validi.

Le vecchie coordinate SET08 non si applicano automaticamente ai nuovi raster. Per tutti10 `pos,size,angle,boardLocal,boardReference=null` in V11, in attesa del PCB originale SET07 e della nuova verifica. I vecchi record sono archiviati in `analysis/set08-original-records.json`; le composizioni07–08 precedenti sono STALE, non valide per questi nuovi file. Le dimensioni vengono ricalcolate dai crop, senza stirare le immagini né inventare pinout.

| File | Source W,H px | Crop L,T,R,B px |
|---|---|---|
'''
for i in d['items']:
 if i['set']==8:text+=f'| {i["file"]} | {i["sourceSize"]} | {i["crop"]} |\n'
text+='''
## Prossimi lotti di recupero

'''
for lot in recovery['pendingSets']:text+=f'- SET{lot["set"]:02}: '+', '.join(lot['skus'])+'.\n'
text+='''
## Finali

Richiesta8 tavole conservata, zero create. Prima: ripristinare01–07, rigenerare09–12, produrre2 consumabili, rivedere difetti e coordinate, analizzare le immagini reali disponibili. Le tavole useranno PNG effettivi con esploso, alternative separate e riferimenti presi da altri SET dichiarati. Allineamento visivo non equivale a incastro fisico o compatibilità elettrica.
'''
(r/'LEGGIMI.md').write_text(text)
for p in [p for p in r.rglob('*') if p.is_file() and p.suffix not in ['.zip','.bundle']]:
 dst=b/p.relative_to(r);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);assert sha(p)==sha(dst)
print('SET08 recovery integrated;40 local/40 regeneration remaining')
