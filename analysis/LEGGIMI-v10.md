# SET Lab — revisione 10 / SET 15

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
| back-black | LuxGuard nero AG, riflessi ridotti. Tre fori grandi in colonna e due piccoli, alpha passante ai centri. Non corrisponde automaticamente al dual camera orizzontale. |
| back-white | LuxGuard bianco perla, bordo oro. Tre aperture scure verticali e apertura inferiore; superficie con iridescenza rosata. Geometria diversa dalle altre cover. |
| back-carbon | AeroForge carbonio a trama diagonale; tre aperture scure in colonna. Fibra e leggerezza non verificabili da immagine. |
| back-wood | EcoLine noce leggibile, venatura verticale. Tre aperture triangolari e due piccole: non stessa geometria delle cover nere/bianche. |
| cam-uw | Due moduli Sony50MP, uno OIS e uno UW, affiancati orizzontalmente. Non allineabili per semplice traslazione alle tre aperture verticali delle cover. |
| cam-peri10 | SONY64MP10xOIS leggibile. Package molto allungato, prisma quadrangolare; vista illustrativa parzialmente sezionata con ottica esposta. Non prova di ingombro fisico o compatibilità con aperture circolari. |
| spk-hires | AAC Technologies Hi-Res Audio192kHz leggibile, un singolo modulo con griglia e contatti. Etichetta non equivale a certificazione o banda acustica misurata. |
| usb-pd | Amphenol PD3.1,140W,USB2.0 leggibili. Porta e flex uniti, vista non strettamente ortografica. Nessuna prova di erogazione140W del telefono o del connettore. |
| cons-thermalp | Tre pad separati, SBS Parts Thermal Pad1mm leggibile. Liner illustrato e lieve tinta violacea ai bordi inferiori conservata. Non montare la tavola intera come se fosse un telaio. |
| cons-kapton | Un rotolo ambra, SBS Parts Kapton10mm leggibile, foro centrale trasparente. Prospettiva e materiale illustrativi, larghezza non misurata. |

### Risultato controllo incastri

Le quattro cover NON hanno aperture identiche: nere/carbonio/bianche principalmente verticali, noce triangolare. Il dual-camera è orizzontale, il periscopio allungato con ingresso quadrangolare. Non basta scalare un’immagine per renderla un ricambio compatibile: nessun montaggio camera-cover approvato. Le camere restano `pos,size,angle=null`, esposte separatamente nelle future tavole. Non si nascondono sotto la cover per simulare l’incastro.

Consumabili: tre pad in una singola immagine e un rotolo Kapton sono articoli di inventario. Lo slot `frame` in `ls.ts` non è una sede di montaggio: coordinate nulle. Pad non scomposti automaticamente in tre SKU. Spessore1mm e larghezza10mm sono etichette, non misure del raster.

## Coordinate nominali

Cm di simulazione da `ls.ts`: X destra, Y strati, Z lunghezza. Angolo0° per orientamento leggibile; nessuno yaw3D validato. Fit uniforme q=min(slotW/cropW,slotH/cropH), nessuna deformazione. Dimensioni reali, contatti, aperture e spessori non certificati.

`analysis/fit-set15-nominal.jpg` mostra10 confronti separati, con rettangolo nominale dello slot dove sensato. È una diagnostica inventario, NON un’immagine finale e NON una prova che i pezzi combacino. `inventoryPreview` delle camere non autorizza il montaggio.

| File | Crop L,T,R,B px | Centro X,Y,Z cm | Bbox X,Y,Z cm | ° |
|---|---|---|---|---|
| set15-back-black.png | [72, 124, 632, 1383] | 0.000, -0.360, 0.000 | 7.028, 0.120, 15.800 | 0 |
| set15-back-white.png | [59, 102, 641, 1419] | 0.000, -0.360, 0.000 | 6.982, 0.120, 15.800 | 0 |
| set15-back-carbon.png | [43, 92, 662, 1429] | 0.000, -0.360, 0.000 | 7.315, 0.120, 15.800 | 0 |
| set15-back-wood.png | [52, 123, 652, 1397] | 0.000, -0.360, 0.000 | 7.400, 0.120, 15.713 | 0 |
| set15-cam-uw.png | [396, 139, 1106, 662] | null | null | None |
| set15-cam-peri10.png | [158, 248, 1231, 524] | null | null | None |
| set15-spk-hires.png | [340, 168, 1068, 600] | 1.700, -0.230, 7.050 | 1.685, 0.340, 1.000 | 0 |
| set15-usb-pd.png | [494, 86, 914, 679] | 0.000, -0.230, 7.200 | 0.637, 0.300, 0.900 | 0 |
| set15-cons-thermalp.png | [97, 92, 1311, 676] | null | null | None |
| set15-cons-kapton.png | [333, 78, 1224, 716] | null | null | None |

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
