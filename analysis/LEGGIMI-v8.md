# SET Lab — LEGGIMI corrente, revisione 8

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
| set13-bat-3500.png | BYD3500mAh3.85V leggibile, singola pouch con due linguette. Capacità e tensione non misurate. |
| set13-bat-4000.png | ATL4000mAh3.87V leggibile, singola pouch e linguette. Nessuna capacità alternativa rilevata sul fronte. |
| set13-bat-5500.png | ATL5500mAh Si-C3.90V leggibile. Singola pouch, distinta dal precedente dual-cell5500mAh; lieve tinta violacea dell’etichetta conservata. |
| set13-ram-12lp4.png | Micron12GB LPDDR4X leggibile, non LPDDR5X. Compatibilità con i tre SoC non verificata; solo collocazione nella sede RAM grafica. |
| set13-soc-ex2500.png | SAMSUNG Exynos2500 leggibile, distinto dai2400/2600 precedenti. Nessuna verifica del package fisico o delle memorie supportate. |
| set13-soc-kirin.png | HiSilicon Kirin9010 leggibile. Package quasi quadrato e pin-one illustrativo, non pinout verificato. |
| set13-soc-tensor4.png | Google TensorG4 leggibile; distinto daG5/G6. Il fit grafico non indica compatibilità con la RAM illustrata. |
| set13-sto-256u4.png | KIOXIA256GB UFS4.0 leggibile, distinto dal256GB UFS3.1 del SET06. |
| set13-sto-32.png | Micron32GB eMMC5.1 leggibile. Interfaccia diversa da UFS: nessuna sede eMMC identificata sulle schede mostrate, montaggio non assegnato. |
| set13-sto-512u31.png | Micron512GB UFS3.1 leggibile, distinto da Samsung512GB UFS4.0 del SET08. |

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
| ram-12lp4 | 692.000, 311.000 | 207.695, 252.000 | 3.152 / 0.000 |
| soc-ex2500 | 339.500, 323.000 | 227.344, 228.000 | 0.828 / 0.000 |
| soc-kirin | 339.500, 323.000 | 227.674, 228.000 | 0.663 / 0.000 |
| soc-tensor4 | 339.500, 323.000 | 228.000, 228.000 | 0.500 / 0.000 |
| sto-256u4 | 1044.500, 243.500 | 205.798, 241.000 | 3.601 / 0.000 |
| sto-512u31 | 1044.500, 243.500 | 206.648, 241.000 | 3.176 / 0.000 |

### Sei composizioni diagnostiche

3SoC×2UFS, RAM `ram-12lp4` comune. Le immagini non costituiscono assemblaggi funzionanti certificati e non includono il montaggio delle tre batterie. L’eMMC è esclusa. I chip alternativi non vengono sovrapposti contemporaneamente.

| N. | SoC | RAM | UFS |
|---|---|---|---|
| 1 | soc-ex2500 | ram-12lp4 | sto-256u4 |
| 2 | soc-ex2500 | ram-12lp4 | sto-512u31 |
| 3 | soc-tensor4 | ram-12lp4 | sto-256u4 |
| 4 | soc-tensor4 | ram-12lp4 | sto-512u31 |
| 5 | soc-kirin | ram-12lp4 | sto-256u4 |
| 6 | soc-kirin | ram-12lp4 | sto-512u31 |

`analysis/fit-set13-game-reference.jpg` documenta questi test. La compatibilità elettrica, la dimensione reale dei package e le connessioni non sono state verificate.

### Crop e coordinate nominali SET13

Cm **nominali di simulazione**: X destra, Y spessore, Z verso il basso del telefono. Bbox dopo rotazione; angolo positivo orario2D, non yaw Three.js collaudato. Per il GAME: `s=min(6.55/1272,7.10/639)`, `X=0.05+(u−1272/2)*s`, `Z=−3.35+(v−639/2)*s`; Y dagli slot di `ls.ts`. Batterie: centro nominale dello slot e fit proporzionale, non vasca fisica riconosciuta.

| File | Crop [L,T,R,B] px | Centro X,Y,Z cm | Bbox X,Y,Z cm | ° | Stato |
|---|---|---|---|---:|---|
| set13-bat-3500.png | [442, 78, 966, 677] | 0.000, -0.020, 3.500 | 5.949, 0.440, 6.800 | 0 | proposta grafica nominale; sede non verificata |
| set13-bat-4000.png | [444, 58, 965, 700] | 0.000, -0.020, 3.500 | 5.518, 0.440, 6.800 | 0 | proposta grafica nominale; sede non verificata |
| set13-bat-5500.png | [477, 70, 932, 680] | 0.000, -0.020, 3.500 | 5.072, 0.440, 6.800 | 0 | proposta grafica nominale; sede non verificata |
| set13-ram-12lp4.png | [67, 68, 878, 1052] | 0.338, 0.275, -3.394 | 1.069, 0.080, 1.298 | 0 | fit grafico su PCB GAME riutilizzato; compatibilità non verificata |
| set13-soc-ex2500.png | [165, 165, 858, 860] | -1.477, 0.285, -3.332 | 1.171, 0.100, 1.174 | 0 | fit grafico su PCB GAME riutilizzato; compatibilità non verificata |
| set13-soc-kirin.png | [163, 163, 861, 862] | -1.477, 0.285, -3.332 | 1.172, 0.100, 1.174 | 0 | fit grafico su PCB GAME riutilizzato; compatibilità non verificata |
| set13-soc-tensor4.png | [172, 172, 852, 852] | -1.477, 0.285, -3.332 | 1.174, 0.100, 1.174 | 0 | fit grafico su PCB GAME riutilizzato; compatibilità non verificata |
| set13-sto-256u4.png | [108, 108, 868, 998] | 2.154, 0.275, -3.741 | 1.060, 0.080, 1.241 | 0 | fit grafico su PCB GAME riutilizzato; compatibilità non verificata |
| set13-sto-32.png | [487, 126, 921, 642] | — | — | — | NON ASSEGNATO: eMMC non è UFS; esporre separatamente |
| set13-sto-512u31.png | [100, 100, 876, 1005] | 2.154, 0.275, -3.741 | 1.064, 0.080, 1.241 | 0 | fit grafico su PCB GAME riutilizzato; compatibilità non verificata |

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
| 14 | `bat-8000`, `bat-stacked`, `disp-lcd67`, `disp-oled61`, `disp-fold`, `disp-eco`, `glass-gg3`, `glass-gg7`, `glass-utg`, `back-red` | NON GENERATO |
| 15 | `back-black`, `back-white`, `back-carbon`, `back-wood`, `cam-uw`, `cam-peri10`, `spk-hires`, `usb-pd`, `cons-thermalp`, `cons-kapton` | NON GENERATO |
| 16 (2/10, residuo) | `cons-ipa`, `cons-tweezers` | NON GENERATO |

Restano due lotti da10 e due SKU finali. Non si inventano otto SKU per completare artificialmente il lotto16. L’ultima tavola finale potrà mostrare i pezzi disponibili e i riferimenti presi da altri SET, distinti dai nuovi articoli.

La richiesta finale8, non20, resta nel piano attivo: coppie01–02,03–04,05–06,07–08,09–10,11–12,13–14,15–16. Cinque motherboard di catalogo; nelle ultime tre tavole riuso dichiarato. Vista esplosa leggibile con alternative e accessori separati, niente compatibilità inventate.

## Verifiche eseguite

- 13 SET da10:130 file con130 hash distinti; vecchi120 invariati.
- 10 nuovi PNG con alpha0–255 e crop validi; proporzioni conservate.
- Sei package con fit uniforme nelle sedi serigrafate GAME; eMMC isolata e non assegnata.
- Sei prove raster prodotte per controllo visivo; nessuna certificazione elettronica.
- Piano residuo esattamente22 SKU, senza duplicati; finale8 pianificata, zero tavole finali prodotte.
