# SET Lab — revisione 9 / SET 14

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
| bat-8000 | BYD8000mAh3.95V STACKED leggibile; due strati visibili. Capacità totale illustrata, non per pouch; collegamenti non verificati. |
| bat-stacked | ATL6800mAh3.94V Si-C STACKED leggibile; due strati. Nessuna validazione di spessore, potenza o capacità. |
| disp-lcd67 | BOE LCD IPS6.7,90Hz,1080x2400 leggibili; notch centrale. |
| disp-oled61 | LG Display OLED LTPO6.1,120Hz,1179x2556 leggibili; punch centrale scuro. |
| disp-fold | Samsung Display OLED7.6,120Hz,1812x2176 leggibili. DIFETTO: raster largo, proporzioni non corrispondenti al formato portrait richiesto. Non montare su telaio rigido; correzione futura necessaria. |
| disp-eco | Tianma TFT6.5,60Hz,720x1600 leggibili; notch centrale e flex inferiore. |
| glass-gg3 | Corning Gorilla Glass3: lastra stretta con fessura superiore illustrata; interno opaco chiaro, non trasmissione ottica. |
| glass-gg7 | Corning Gorilla Glass7i: identificatore presente e punch superiore; interno opaco illustrativo. |
| glass-utg | SCHOTT Ultra Thin Glass UTG presente; lastra quasi quadrata distinta dai vetri stretti. Non coincide con il display fold generato; nessun accoppiamento validato. |
| back-red | LuxGuard leggibile; rosso scuro lucido. I fori fotocamera sono raffigurati scuri, non aperture alpha; disposizione non verificata rispetto ai moduli. |

### Blocco fold / UTG

La risoluzione stampata è corretta, ma il display fold è largo anziché portrait. Non è stato stirato o ruotato per mascherare il difetto. `disp-fold` e `glass-utg` hanno `pos,size,angle=null`: inventario separato, nessun montaggio sul telaio standard. `inventoryPreview` serve solo al confronto grafico. Le loro sagome non sono una coppia fisicamente verificata. Correzione del fold registrata in `catalog-plan.json`; non sono state eseguite ulteriori generazioni oltre le10 del lotto.

## Coordinate e proporzioni

Unità cm NOMINALI da `ls.ts`, non misure di fabbrica. X destra, Y spessore/strati, Z lunghezza. Rotazione0° per preservare testo e orientamento raster. Per ogni bbox w×h, q=min(larghezzaSlot/w,lunghezzaSlot/h), dimensioni[wq,spessoreSlot,hq]. Nessuna deformazione. Le linguette dei display e batterie sono incluse nel bbox. Spessore stacked non misurato:0.44cm del catalogo è solo valore di simulazione.

Display e vetro occupano strati del telefono, non piazzole del PCB. `boardReference` e `boardLocal` sono null per tutti i nuovi asset. Nessun fit sul PCB GAME viene inventato in assenza del file. Diagnostica `analysis/fit-set14-nominal.jpg`: dieci viste separate contro il rettangolo nominale dello slot, NON assemblaggi completi né immagini finali.

| File | Crop L,T,R,B px | Centro X,Y,Z cm | Dimensioni X,Y,Z cm | ° |
|---|---|---|---|---|
| set14-bat-8000.png | [163, 190, 686, 1074] | 0.000, -0.020, 3.500 | 4.023, 0.440, 6.800 | 0 |
| set14-bat-stacked.png | [148, 118, 701, 1126] | 0.000, -0.020, 3.500 | 3.731, 0.440, 6.800 | 0 |
| set14-disp-lcd67.png | [180, 100, 667, 1223] | 0.000, 0.460, 0.000 | 6.592, 0.120, 15.200 | 0 |
| set14-disp-oled61.png | [566, 58, 842, 714] | 0.000, 0.460, 0.000 | 6.395, 0.120, 15.200 | 0 |
| set14-disp-fold.png | [325, 75, 1083, 736] | null | null | None |
| set14-disp-eco.png | [67, 102, 621, 1461] | 0.000, 0.460, 0.000 | 6.196, 0.120, 15.200 | 0 |
| set14-glass-gg3.png | [41, 43, 663, 1477] | 0.000, 0.560, 0.000 | 6.680, 0.060, 15.400 | 0 |
| set14-glass-gg7.png | [60, 114, 644, 1407] | 0.000, 0.560, 0.000 | 6.956, 0.060, 15.400 | 0 |
| set14-glass-utg.png | [410, 45, 998, 724] | null | null | None |
| set14-back-red.png | [74, 163, 630, 1358] | 0.000, -0.360, 0.000 | 7.351, 0.120, 15.800 | 0 |

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

- SET15: back-black, back-white, back-carbon, back-wood, cam-uw, cam-peri10, spk-hires, usb-pd, cons-thermalp, cons-kapton.
- SET16: cons-ipa, cons-tweezers.

Le otto tavole finali restano organizzate per coppie di SET; solo cinque SKU motherboard, con riuso dichiarato dei riferimenti nelle altre tavole. Servono gli archivi precedenti prima del compositing finale.
