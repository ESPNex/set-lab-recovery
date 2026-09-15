# SET Lab — revisione14 / SET11 rigenerato

## Repository ripulito

Repository privato: https://github.com/ESPNex/set-lab-recovery

Richiesta utente: eliminare immagini inutili o in più. Rimossi dalla versione corrente **70 raw e27 immagini diagnostiche** precedentemente tracciate. Non sono stati eliminati componenti di catalogo. I nuovi raw/diagnostici SET11 restano solo materiali di lavoro in `/usr`, esclusi dal push. Nel ramo corrente restano **140 immagini di componenti**, in `originals/` (60) e `generated/` (80), più dati, script e viewerV1 già richiesto. Nessun contatto-sheet, crop o mockup aggiuntivo nel ramo corrente.

Rimozione normale Git, non riscrittura della storia: raw/diagnostiche già caricate restano recuperabili nei vecchi commit. `/usr` non persistente; dopo un reset le tavole si ricostruiscono dai PNG, i raw nuovi non caricati non sono garantiti. Le immagini di lavoro non sono SKU aggiuntivi e non vengono conteggiate nel catalogo.

## Stato pipeline

SET11 rigenerato da `ls.ts`:10 nuovi PNG. Disponibili140 immagini effettive SET01–11,13–15, hash verificati. Rimane SET12 da rigenerare (10) e2 SKU mai prodotti (IPA/pinzette). Registro storico150 file/147 SKU su149, non150 file ora presenti. **8 finali previste, zero create.**

Il checkpoint nel workspace `set-lab-recovery.bundle` è storico, precedente alla pulizia e al SET11: non rappresenta lo stato corrente. Fonte corrente: repository GitHub. Non rigenerato il bundle completo perché contiene la storia e supererebbe lo spazio persistente disponibile.

## Analisi eseguita

Riesaminate le14 tavole disponibili (140 asset); Pro03, nuovo telaio classico e batteria dual letti in dettaglio. SET12 assente non riesaminato. Quattro composizioni parziali SoC+UFS generate per analisi locale, non aggiunte al repository e non considerate finali.

| SKU SET11 | Esito |
|---|---|
| back-alu | Vertex alluminio satinato, apertura camera passante, lega non misurata. |
| back-leather | EcoLine marrone, trama e cuciture illustrate, apertura camera passante; materiale PU non certificato. |
| bat-dual | ATL DUAL CELL5500mAh TOTAL3.87V leggibile. Due pouch, capacità totale esplicita, circuito parallelo non validato. |
| cons-screws | Sei viti Phillips separate. DiametroM1.6 non misurabile dal raster, un solo SKU inventario. |
| frame-classic | Vista frontale più pulita del raster perduto, centro e home trasparenti. Foro superiore camera illustrato scuro. Scelta apertura16:9; contraddizione catalogo4:3/16:9 ancora aperta. |
| soc-exy26 | Samsung Exynos2600 leggibile. |
| soc-g99 | MediaTek HelioG99 leggibile. |
| soc-helio | UNISOC T7250 leggibile: SKU soc-helio non implica Helio/MediaTek. |
| soc-tensor | Google TensorG5 leggibile. |
| sto-1tb | Samsung1TB UFS4.0 leggibile, non4.1; package generato quasi quadrato. |

Il telaio ora ha centro vuoto pulito e home passante, senza ritaglio ROI manuale. Apertura portrait16:9 circa, non prova di compatibilità: `ls.ts` contraddice4:3 e16:9. L’etichetta5500mAh TOTAL evita di attribuire5500 a ciascuna pouch; tensione/materiali restano illustrativi.

## Coordinate e ipotesi

Pro03 riutilizzato, nessuna nuova motherboard: SoC[520,203,226,239], ipotesi UFS[786,342,119,121] nel crop1286×666. Serigrafia SOC/RAM/UFS ambigua: queste assegnazioni non sono pinout. RAM assente nelle quattro prove. Anche Helio/Unisoc non sono dichiarati compatibili con UFS4.0: solo test raster.

Fit uniforme q=min(slotW/cropW,slotH/cropH); X=0.05+(u−1286/2)s, Z=−3.35+(v−666/2)s con s=min(6.55/1286,7.10/666). Y da `ls.ts`, rotazione0°. Unità cm nominali, nessuna deformazione. Cover e batteria fit nominale; viti pos/size/angle null perché inventario.

| File | Crop L,T,R,B px | Centro X,Y,Z cm | Bbox X,Y,Z cm |
|---|---|---|---|
| set11-back-alu.png | [22, 25, 682, 1497] | 0.000, -0.360, 0.000 | 7.084, 0.120, 15.800 |
| set11-back-leather.png | [28, 35, 676, 1486] | 0.000, -0.360, 0.000 | 7.056, 0.120, 15.800 |
| set11-bat-dual.png | [73, 72, 1335, 694] | 0.000, -0.020, 3.500 | 6.400, 0.440, 3.154 |
| set11-cons-screws.png | [95, 91, 1312, 684] | null | null |
| set11-frame-classic.png | [60, 62, 708, 1314] | 0.000, 0.120, 0.000 | 7.400, 0.900, 14.298 |
| set11-soc-exy26.png | [456, 136, 952, 632] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.151 |
| set11-soc-g99.png | [418, 92, 990, 676] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.175 |
| set11-soc-helio.png | [472, 152, 937, 618] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.154 |
| set11-soc-tensor.png | [434, 114, 974, 654] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.151 |
| set11-sto-1tb.png | [489, 178, 919, 590] | 1.081, 0.275, -2.996 | 0.606, 0.080, 0.581 |

## Pipeline, integrità e limiti

Alpha postprodotto con chroma-key globale graduato smoothstep e despill2px Pillow/NumPy. Nessun rembg, flood fill o nuova ROI manuale. I10 nuovi raw sono preservati localmente ma non aggiunti alla consegna Git. Script di analisi producono file ignorati da Git.

V14 conserva gli altri140 record. I130 PNG già presenti restano invariati;10 hash SET11 nuovi con riferimento ai precedenti in supersedesSha256. Viti sei per immagine ma un solo SKU. Diagnostiche escluse dal conteggio.

Persistono difetti storici: USB01 bande bianche, frontale03 etichetta52MP, RAM06 marca diversa, Lite senza sedi RAM/UFS certe, batteria07 microtesto, SIM08 tre vani, grafite10 conteggio ambiguo, fold14 rapporto errato, cover15 aperture non coincidenti automaticamente. eMMC13 non è UFS. Non nascondere difetti sotto altri pezzi nelle finali.

Prossimo: SET12, poi2 consumabili e8 tavole finali con componenti reali dell’inventario, alternative separate e riferimenti riutilizzati dichiarati. Nessuna generazione in background. Il viewer storico non è aggiornato a tutti i SET.
