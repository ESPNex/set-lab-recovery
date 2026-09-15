from pathlib import Path
from PIL import Image
import json,re,math,hashlib
root=Path('/home/user');src=(root/'uploads/ls.ts').read_text()
slots={}
for line in src.splitlines():
 m=re.search(r'^  (\w+): \{ id: "\w+", name: "([^"]+)", pos: (\[[^]]+\]), size: (\[[^]]+\]), explode: ([-.\d]+)',line)
 if m:slots[m[1]]=dict(name=m[2],pos=json.loads(m[3]),size=json.loads(m[4]),explode=float(m[5]))
assert len(slots)==18
parts={}
for line in src.splitlines():
 m=re.search(r'^  p\("([^"]+)",\s*("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'),\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"',line)
 if m:parts[m[1]]=dict(name=m[2][1:-1],brand=m[3],slot=m[5])
# Explicit file aliases, not inferred ID_FILE fallback photographs.
alias={'pcb-bare':'board-std','soc-snap':'soc-x90','battery-pouch':'bat-3000','cam-front':'camf-8','speaker':'spk-mono','usb-flex':'usb-20','mic':'mic-1','sim-tray':'sim-nano','antenna-flex':'ant-wifi5','vapor-chamber':'th-vc'}
boardfiles=['set01-pcb-bare.png','set03-board-pro.png','set05-board-lite.png','set07-board-game.png']
rects=[{'soc':[139,244,158,157],'ram':[129,449,174,114],'storage':[356,350,132,157]},{'soc':[520,203,226,239],'ram':[786,184,119,123],'storage':[786,342,119,121]},{'soc':[470,158,327,328]},{'soc':[225,209,229,228],'ram':[585,185,214,252],'storage':[938,123,213,241]}]
boardrows=[];boarddata=[]
for p,name in enumerate(boardfiles):
 folder='generated' if p==3 else 'originals';im=Image.open(root/folder/name);bb=im.getbbox();W,H=bb[2]-bb[0],bb[3]-bb[1];scale=min(6.55/W,7.1/H)
 boarddata.append(dict(pair=p+1,file=name,crop=bb,raster=[W,H],center=[.05,.145,-3.35],scale=scale,size=[W*scale,.14,H*scale],yaw=0,slots=rects[p]))
 for role,(x,y,w,h) in rects[p].items():
  cx,cy=x+w/2,y+h/2;pos=[.05+(cx-W/2)*scale,slots[role]['pos'][1],-3.35+(cy-H/2)*scale]
  boardrows.append([p+1,role,x,y,w,h,cx,cy,*pos,w*scale,h*scale])
rows=[]
for f in sorted(list((root/'originals').glob('*.png'))+list((root/'generated').glob('*.png'))):
 st=int(f.name[3:5]);sku=f.stem[6:];sku=alias.get(sku,sku);role=parts[sku]['slot'];im=Image.open(f);bb=im.getbbox()
 if f.name=='set01-usb-flex.png':bb=(626,66,782,702)
 W,H=bb[2]-bb[0],bb[3]-bb[1];s=slots[role];a=W/H;tw,th=s['size'][0],s['size'][2];angle=0 if abs(math.log(a/(tw/th)))<=abs(math.log((1/a)/(tw/th))) else 90
 ew,eh=(W,H) if angle==0 else (H,W);scale=min(tw/ew,th/eh);pos=s['pos'].copy();status='proposta grafica, sede non verificata';size=[ew*scale,s['size'][1],eh*scale]
 b=boarddata[(st-1)//2]
 if role=='motherboard':pos=b['center'];size=b['size'];angle=0;status='riferimento raster in ingombro nominale'
 if role in ['soc','ram','storage']:
  br=next((r for r in boardrows if r[0]==(st+1)//2 and r[1]==role),None)
  if br:
   pos=br[8:11];tw,th=br[11:13];angle=0;scale=min(tw/W,th/H);size=[W*scale,s['size'][1],H*scale];status='piazzola visuale; non verifica BGA'
   if st==4 and role in ['ram','storage']:status='attribuzione ipotetica RAM/UFS'
  else:pos=None;size=None;angle=None;status='nessuna sede identificata, non montare automaticamente'
 rows.append(dict(file=f.name,sku=sku,slot=role,set=st,crop=list(bb),sourceSize=list(im.size),pos=pos,size=size,angle=angle,status=status,provenance='AI + chroma-key' if st==7 else 'PNG fornito'))
planned=['soc-d9400','ram-24','sto-512','th-coil','ant-uwb','hap-z','sim-hybrid','soc-8s','ram-8x','mic-1']
out=dict(version=2,units='cm nominali di simulazione, non dimensioni misurate',axes='x destra, y spessore, z basso del telefono',angle='rotazione 2D oraria rispetto al raster; non yaw del renderer non fornito',boards=boarddata,items=rows,set08Pending=planned)
(root/'coordinates-v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(root/'analysis/LEGGIMI-v1.md').write_text((root/'LEGGIMI.md').read_text())
fmt=lambda v:'—' if v is None else ', '.join(f'{x:.3f}' for x in v)
text='''# SET Lab — Revisione 2 e nuovi SET

Aggiornamento: 15 settembre 2026. Fonte catalogo: `uploads/ls.ts`.

## Stato effettivo e conservazione

- **SET 01–06:** 60 PNG precedenti riesaminati visivamente in sei tavole; le tre motherboard anche in dettaglio.
- **SET 07:** 10 nuove immagini sintetiche generate, elaborate con alpha e riesaminate visivamente; completato come inventario, non validato come kit meccanico.
- **SET 08:** 10 componenti pianificati, **0 immagini generate**. Limite dello strumento raggiunto dopo 10 generazioni nel turno; la coppia 07–08 è ancora incompleta.
- Totale immagini utilizzabili: **70**, non 80. Non sono state copiate immagini dei vecchi SET per fingere nuovi SKU.
- Come richiesto, tutti i materiali di progetto sono spostati in **`/usr/set-lab`**, lasciando nel workspace persistente soltanto questo LEGGIMI. Le directory di sistema non sono state spostate.
- **ATTENZIONE:** `/usr` non viene incluso nei salvataggi tra sessioni. Non è un archivio permanente e spostare sullo stesso filesystem non libera spazio disco complessivo: riduce solo i materiali soggetti al limite del workspace. Scaricare l’archivio dalla pagina live “Archivio SET Lab” mentre questa sessione è disponibile. Per riprendere da un ambiente nuovo, ricaricare quell’archivio insieme a questo LEGGIMI.
- Nessuna repository remota è stata creata; è stata scelta l’opzione `/usr`, non GitHub.

## File in `/usr/set-lab`

| Percorso | Contenuto |
|---|---|
| `originals/` | I 60 PNG precedenti, non modificati |
| `new_raw/` | Le 10 nuove immagini AI con sfondo magenta di lavorazione |
| `generated/` | I 10 PNG SET 07 con sfondo rimosso via chroma-key |
| `analysis/` | Tavole 01–07, ritagli delle motherboard, metadati, precedente LEGGIMI |
| `uploads/ls.ts` | Catalogo fornito, non modificato |
| `coordinates-v2.json` | Revisione corrente: 70 asset, 4 PCB e piano SET 08 |
| `coordinates.json` | Coordinate V1, storiche, in pixel tavola |
| `viewer.html`, `viewer_package.zip` | Viewer V1 storico, soltanto SET 01–06; NON aggiornato a 70 immagini |
| `update_readme.py` | Script di derivazione delle coordinate nominali V2 |
| `downloads/set-lab-session.zip` | Archivio scaricabile del progetto, esclusi duplicati storici compressi e file di servizio |

## Revisione multimodale SET 01–06

| SET | Esito della revisione delle 10 immagini |
|---|---|
| 01 | Telaio/cover/display verticali; cover con apertura camera molto più compatta del modulo dual completo di flex. Batteria e PCB non condividono una scala fisica dimostrabile. PCB con serigrafie SoC, LPDDR, UFS leggibili. Speaker comprende fili lunghi: il suo alpha-bbox non è l’ingombro della sola cassa. USB contiene due pannelli bianchi opachi: usare solo ritaglio centrale [626,66,782,702]. |
| 02 | SoC quadrato, RAM quasi quadrata mentre sede LPDDR è orizzontale: non deformare per riempirla. Due antenne e due materiali termici sono elementi distinti, non quattro sedi meccaniche nuove. Microfono raffigurato come capsula tonda: forma non rappresentativa con certezza del MEMS singolo di catalogo. ERM comprende cavi; SIM include linguetta di estrazione. |
| 03 | PCB largo e basso, pur recando la stampa 65×71 mm: la scritta non giustifica una scala anisotropa. Area comune SOC/RAM/UFS con più piazzole; RAM/UFS non etichettate singolarmente. Vetro orizzontale, display e telaio verticali: serve rotazione grafica, non stiramento. Batteria larga, camera tripla verticale. Camf-32 riporta 52MP sul raster, diverso dai 32MP del catalogo. |
| 04 | Due SoC e due RAM alternativi, non simultaneamente sulle stesse sedi. Le stampe 8 Gen 3 e 7+ Gen 3 coincidono con i nomi del catalogo: i suffissi ID non sono errori. Modulo SIM/eSIM è una composizione di due oggetti separati: un unico bbox non basta per un incastro. Antenna e attuatore orizzontali; termico quasi quadrato. |
| 05 | PCB Lite con sola sede U1 SoC identificabile; non assegnare RAM/UFS al rame libero. Camera quad, frontale e batteria hanno ingombri diversi dai vecchi asset. Frontale ha flex laterale; speaker contiene fili/annotazioni separati. Vetro orizzontale da ruotare per una tavola ritratto. Posizione del foro cover e del vano frame non costituisce allineamento meccanico provato. |
| 06 | Due SoC e due RAM alternativi; RAM/UFS prive di sede sul Lite mostrato. Exynos 2400 e Dimensity 8300-Ultra sono corretti rispetto al catalogo. **RAM 16 mostra Samsung mentre ls.ts indica SK Hynix**: conflitto reale di marca. Haptics è circolare, SIM dual verticale, antenna e array microfoni orizzontali. Non applicare uno yaw uguale a tutte le forme. |

### Correzioni al precedente LEGGIMI

`set04-soc-8e`, `set04-soc-7g2`, `set06-soc-vertv2` e `set06-soc-q6` non sono errori di denominazione confrontati con `ls.ts`: gli ID sono alias. Rimangono le discrepanze camf-32 e marca RAM16. `glass-victus3` è l’ID interno del **Victus 2** nel catalogo, non una prova di Victus 3.

Il mapping `ID_FILE` e il fallback `slotFiles` riusano fotografie fra SKU diversi: non permettono di dichiarare ciascuna immagine unica. Esempio: `soc-ten6 → soc-snap`, `soc-8e2 → soc-a19`. La mappa aggiornata usa file specifici; non certifica i prodotti o le specifiche commerciali scritte nel catalogo.

## SET 07 — creato e revisionato

La generazione non ha prodotto alpha nativo: si è richiesto uno sfondo magenta uniforme, poi rimosso con chroma-key. I PNG in `generated/` hanno canale alpha 0–255; non equivalgono a scontorni manuali certificati. Nel vetro il centro è trasparente: rifrazione e trasmissione fisica non sono modellate. Possibili residui cromatici sui bordi vanno verificati alla risoluzione finale.

| File | SKU / risultato visivo |
|---|---|
| set07-frame-flat.png | Telaio flat-edge metallico, vuoti interni e guide laterali; forma creata distinta dai tre telai precedenti. |
| set07-board-game.png | PCB blu SBS-G8 GAME con tre piazzole SOC/RAM/UFS distinte. **Il generatore non ha rispettato la geometria quasi quadrata né le posizioni richieste:** l’immagine effettiva è larga. Coordinate sottostanti misurate sul risultato, non copiate dal prompt. |
| set07-bat-6000.png | ATL 6000mAh nella stampa principale; il microtesto “Rated capacity” sembra indicare 8000mAh: etichetta non validata e da correggere in un successivo passaggio. Non usare come specifica elettrica. |
| set07-disp-2k.png | Display spento verticale, punch-hole centrale; risoluzione/refresh non deducibili dall’aspetto. |
| set07-glass-armor.png | Cornice di vetro verticale trasparente; materiale Armor 2 è una destinazione di catalogo, non identificazione ottica. |
| set07-back-blue.png | Cover blu distinta, foro vuoto in alto a sinistra. |
| set07-cam-1inch.png | Un singolo grande modulo lente con flex inferiore; scritta IMX989/50MP illustrativa. |
| set07-camf-50.png | Frontale singola con 50MP AF sul flex; autofocus non verificabile da raster. |
| set07-spk-dual.png | Due griglie in un’unica cassa Goertek 2×1.4W; proprietà audio non misurate. |
| set07-usb-40b.png | Flex verticale marcato USB4 40Gbps; velocità e PD non verificabili dalla foto. |

## SET 08 — da generare nel prossimo turno

| Nome file previsto | Slot | Stato |
|---|---|---|
'''
for sku in planned:text+=f'| set08-{sku}.png | {parts[sku]["slot"]} | NON GENERATO |\n'
text+='''
Il piano comprende 9 SKU non illustrati nei precedenti SET e `mic-1` come nuova rappresentazione correttiva del microfono singolo già associato al vecchio `set02-mic`. I due SoC e le due RAM sono alternative illustrative, non dichiarazioni di compatibilità BGA. Tutti i 18 slot funzionali saranno coperti nella coppia solo dopo il completamento del SET 08.

## Sistemi di coordinate: non confonderli

1. **V1 tavola:** 1800×1200 pixel, X/Y al centro del ritaglio, W/H prima della rotazione. Conservate nel JSON storico.
2. **Raster locale PCB:** origine nell’angolo alto-sinistro del ritaglio alpha; u destra, v basso. Rettangoli misurati visivamente, precisione di pochi pixel non certificata.
3. **V2 simulazione:** centimetri NOMINALI derivati da `ls.ts`: X destra, Y spessore, Z verso il basso del telefono. Non centimetri ricavati da una misura fisica.

La V2 colloca ciascun PCB al centro nominale (0.05, 0.145, −3.35), entro l’ingombro massimo 6.55×7.10 cm **senza deformare il raster**. Per raster ritagliato W×H:

```
s = min(6.55/W, 7.10/H)
x = 0.05 + (u - W/2) * s
z = -3.35 + (v - H/2) * s
```

Rotazione PCB 2D = 0°, come il raster ispezionato. Questa è una nuova convenzione di tavola, **non un override collaudato dello yaw Three.js**: il renderer e `types.ts` non sono stati forniti. In `ls.ts` lo yaw è 90° per PCB/SoC/RAM/UFS/SIM, −90° per batterie, 180° per haptics: applicarlo automaticamente ai raster eterogenei può disallinearli. Prima dell’integrazione, definire la trasformazione texture→mesh e ruotare insieme PCB e figli.

Per i componenti non saldati, la proposta usa centro e spessore dello slot del catalogo; sceglie 0° o 90° per contenere il bbox con scala uniforme. Sono **coordinate illustrative**, non alloggiamenti riconosciuti. W×Z descrive il bbox dopo rotazione. Cavi e flex inclusi nell’alpha-bbox possono rendere il corpo principale troppo piccolo: servono ancore corpo/connettore separate per perfezionare il montaggio.

### Baseline 18 slot da `ls.ts` (non modificata)

| Slot | Centro X,Y,Z cm | Ingombro X,Y,Z cm | Esplosione Y cm |
|---|---|---|---|
'''
for role,s in slots.items():text+=f'| {role} | {fmt(s["pos"])} | {fmt(s["size"])} | {s["explode"]:.2f} |\n'
text+='''
La baseline contiene sovrapposizioni da non scambiare per incastri risolti: ad esempio, con box centrati non ruotati, USB e speaker si intersecano lungo X di 0.6 cm sul bordo inferiore, con Y coincidente e intervalli Z sovrapposti. Display/glass e board/batteria richiedono controllo degli strati e delle tolleranze. Il commento “PRECISE SLOT MAP” è un’intenzione del codice, non validazione CAD.

### Motherboard: ritagli e nuove dimensioni nominali proporzionali

| SET | Raster W×H px | Ritaglio nel PNG [L,T,R,B] | Bbox X×Z cm | Scala cm/px |
|---|---|---|---|---|
'''
for b in boarddata:text+=f'| {b["file"]} | {b["raster"][0]}×{b["raster"][1]} | {b["crop"]} | {b["size"][0]:.4f}×{b["size"][2]:.4f} | {b["scale"]:.7f} |\n'
text+='''
### Piazzole riviste: pixel locali e proiezione nominale V2

| Coppia | Sede | Rect u,v,w,h px | Centro u,v px | Centro X,Y,Z cm | Limite X×Z cm |
|---|---|---|---|---|---|
'''
for r in boardrows:text+=f'| {r[0]*2-1:02}–{r[0]*2:02} | {r[1]} | {r[2:6]} | {r[6]:.1f}, {r[7]:.1f} | {fmt(r[8:11])} | {r[11]:.3f}×{r[12]:.3f} |\n'
text+='''
Le sedi 01–02 sono confermate solo per la serigrafia. Nel 03–04 RAM/UFS restano ipotesi, senza escludere le altre piazzole visibili. Nel 05–06 RAM e storage **non hanno coordinate di montaggio V2**. Le sedi 07–08 sono misurate sull’immagine AI effettiva, ma attendono i chip SET 08; non sono state provate combinazioni assenti.

## Registro coordinate V2 — tutti i 70 asset disponibili

Valori arrotondati a 3 decimali per leggibilità; i decimali NON esprimono accuratezza fisica. Angolo 2D orario; dimensioni X,Y,Z del bbox orientato. “—” indica mancata assegnazione, non zero. Gli asset alternativi condividono lo slot: non installarli contemporaneamente. Per ritagli, precisione numerica completa e provenienza usare `coordinates-v2.json`.

| File | Slot | Centro X,Y,Z cm | Bbox X,Y,Z cm | ° | Stato |
|---|---|---|---|---:|---|
'''
for r in rows:text+=f'| {r["file"]} | {r["slot"]} | {fmt(r["pos"])} | {fmt(r["size"])} | {r["angle"] if r["angle"] is not None else "—"} | {r["status"]} |\n'
text+='''
## Prossimo passo e criteri di accettazione

1. Recuperare l’archivio da questa sessione prima che `/usr` venga eliminato.
2. Generare i 10 asset SET 08, uno per file, senza fallback o copie dei vecchi SKU.
3. Scontornare e riesaminare tutti i nuovi asset; verificare la RAM/UFS sul raster effettivo della motherboard GAME, mantenendo le proporzioni.
4. Correggere il microtesto batteria e rifinire eventuali bordi cromatici; distinguere area corpo da flex e cavi.
5. Solo dopo, aggiornare il viewer a SET 01–08 e verificare le trasformazioni nel renderer reale. Il viewer V1 non rappresenta questa revisione V2.
6. Per incastri fisici esatti occorrono disegni quotati, pinout, verso dei connettori e ancore comuni. Le immagini AI non sono sostituti di questi dati.
'''
(root/'LEGGIMI.md').write_text(text)
print('parts',len(parts),'slots',len(slots),'rows',len(rows),'readme chars',len(text))
