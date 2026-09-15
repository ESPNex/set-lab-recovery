# SET Lab — revisione12 / recupero SET09

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
| back-green | LuxGuard verde salvia satinato, fori alpha. Disposizione non verificata rispetto al periscopio. |
| bat-7000 | BYD7000mAh3.95V Si-C leggibile; nessuna capacità alternativa visibile. |
| board-rf | SOC,RAM,UFS ben distinti e liberi da passivi; array UFS concentrico illustrativo, non pinout reale. Nome scheda ripetuto due volte. |
| cam-peri2 | SONY200MP6xOIS leggibile; microtesto aggiuntivo decorativo non certificato. Ingresso quadrangolare, non validato rispetto ai fori cover. |
| camf-12 | SONY12MP leggibile; riflesso blu e lieve alone/bordo non fisico. Apertura display non validata come misura. |
| disp-oled63 | BOE OLED6.3,120Hz,1080x2400 leggibili, punch centrale e flex inferiore. |
| frame-mag | Telaio Vertex Qi2 con anello inferiore e finestre alpha; nessuna misura N52/lega certificabile. |
| glass-zaf | CrystalLux Synthetic Sapphire leggibile, punch superiore; lastra opaca illustrativa, non trasparenza ottica. |
| spk-stereo-bot | Due driver, Goertek2x1.1W leggibile; nessuna misura acustica. |
| usb-dp | Amphenol DP2.1 8K60 leggibile; residuo violaceo sul metallo e vista non strettamente ortografica. |

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
| set09-back-green.png | [539, 60, 837, 709] | 0.000, -0.360, 0.000 | 7.255, 0.120, 15.800 |
| set09-bat-7000.png | [100, 85, 667, 1292] | 0.000, -0.020, 3.500 | 3.194, 0.440, 6.800 |
| set09-board-rf.png | [82, 79, 1331, 692] | 0.050, 0.145, -3.350 | 6.550, 0.140, 3.215 |
| set09-cam-peri2.png | [93, 183, 1317, 587] | null | null |
| set09-camf-12.png | [523, 204, 1080, 618] | null | null |
| set09-disp-oled63.png | [547, 36, 861, 734] | 0.000, 0.460, 0.000 | 6.838, 0.120, 15.200 |
| set09-frame-mag.png | [70, 70, 633, 1426] | 0.000, 0.120, 0.000 | 6.560, 0.900, 15.800 |
| set09-glass-zaf.png | [67, 132, 637, 1387] | 0.000, 0.560, 0.000 | 6.994, 0.060, 15.400 |
| set09-spk-stereo-bot.png | [186, 262, 1222, 508] | 1.700, -0.230, 7.050 | 2.400, 0.340, 0.570 |
| set09-usb-dp.png | [519, 109, 889, 658] | 0.000, -0.230, 7.200 | 0.607, 0.300, 0.900 |

## SET08 ricalcolato sul Game originale

Recuperato il PNG Game07 identico, rifatti5 fit:2SoC,2RAM,1UFS. q=min(sedeW/cropW,sedeH/cropH), centro coincidente, angolo0°, nessuna deformazione. Quattro prove2SoC×2RAM con sto-512 in `analysis/fit-set08-recovery-game.jpg`. Solo contenimento grafico, NON compatibilità dei bus o BGA. Accessori fit nominale; SIM resta null per geometria difettosa.

| SKU | Centro u,v px | Disegno W,H px |
|---|---|---|
| ram-24 | 692.000, 311.000 | 214.000, 218.901 |
| ram-8x | 692.000, 311.000 | 214.000, 243.603 |
| soc-8s | 339.500, 323.000 | 223.419, 228.000 |
| soc-d9400 | 339.500, 323.000 | 228.000, 228.000 |
| sto-512 | 1044.500, 243.500 | 208.783, 241.000 |

## Pipeline e backup

Raw AI intatti; PNG alpha postprodotto con chroma-key globale smoothstep e despill2px, nessun rembg/flood fill o nuova ROI manuale. Vetri opachi illustrativi: non trasparenza ottica reale.

Git locale in `/usr/set-lab`; GitHub NON autenticato e push NON eseguito. `/usr` non persistente: non è una garanzia di backup remoto.

Per mantenere il checkpoint del workspace entro la capacità disponibile, il bundle Git contiene direttamente i50 asset generati SET08–09,13–15 con raw e metadati; gli originali70 recuperati rimangono un archivio esterno collegato tramite URL e SHA256. `restore_originals.py` li ripristina senza sovrascrivere file differenti e controlla gli hash. **Il bundle da solo non contiene i70 PNG originali**: conservare anche lo ZIP Catbox originale. I file sono tutti presenti in `/usr` in questa sessione. Dopo autorizzazione GitHub si potrà caricare anche il materiale originale nel repository remoto.

`set-lab-recovery.bundle` aggiornato è il checkpoint Git locale scaricabile. Viewer V1 recuperato nell’archivio originale, non aggiornato ai nuovi SET. Nessuna attività di generazione in background.

## Prossimo

SET10: hap-dual,ram-18,ram-32,soc-8e2,soc-dim95,soc-ten6,sto-1tb41,sto-2tb,th-cu,th-gr2. Poi SET11–12 e2 consumabili; controlli finali ed8 tavole con PNG effettivi, alternative separate e riferimenti riutilizzati dichiarati.
