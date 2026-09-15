> Documento storico V15, superato da README e REVISIONE-FINALE V16; include segnalazioni successivamente rettificate.

# SET Lab — revisione15 / SET12 rigenerato

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
| cons-glue | SBS Parts B-7000 15ml leggibile; tubo orizzontale, microtesto aggiuntivo illustrativo, lieve riflesso magenta metallico. Inventario, non frame montato. |
| cons-tabs | Due adesivi chiari con tiranti arancio, SBS Parts; liner largo e bordo rosato conservato. Non misura fisica o traslucenza reale. |
| frame-mg | Vertex AZ91D: due grandi finestre alpha, traverse/rail illustrativi. Lega e138g non certificabili dal raster. |
| frame-ss | AeroForge316L: finestre alpha, geometria diversa dal magnesio, qualche riflesso violaceo. Massa198g non verificata. |
| soc-6g1 | Qualcomm Snapdragon6Gen1 leggibile. |
| soc-7g3 | Qualcomm Snapdragon7Gen3 leggibile, senza plus. |
| soc-8g2 | Qualcomm Snapdragon8Gen2 leggibile; scritta Pin1 extra, non certificazione pinout. |
| soc-d7300 | MediaTek Dimensity7300 leggibile. |
| soc-d8300 | MediaTek Dimensity8300 leggibile, con sigle CPU/GPU/MT6880V aggiuntive non richieste e non verificate: non usare come specifica tecnica. |
| soc-d9300 | MediaTek Dimensity9300+ leggibile con plus presente. |

In particolare, Dimensity8300 include sigle extra CPU/GPU non presenti nella richiesta grafica: registrate come non verificate, non elevate a specifiche ufficiali. I due adesivi sono un solo SKU; non si montano colla o liner nello slot frame.

## Coordinate e proporzioni

Riferimento preso dal SET03 Pro, nessuna motherboard inventata. SoC[520,203,226,239] nel crop1286×666; ipotesi UFS[786,342,119,121] con sto-1tb del SET11. Serigrafia SOC/RAM/UFS ambigua: RAM assente, collocazione UFS solo ipotesi grafica. Nessuna compatibilità dei sei SoC con quella memoria dichiarata.

Fit uniforme q=min(slotW/cropW,slotH/cropH), centro coincidente,0° raster. s=min(6.55/1286,7.10/666); X=0.05+(u−1286/2)s, Z=−3.35+(v−666/2)s; Y nominale da `ls.ts`. Cm di simulazione, non dimensioni reali. Telai fit proporzionale dello slot; consumabili pos/size/angle null.

| File SET12 | Crop L,T,R,B px | Centro X,Y,Z cm | Bbox X,Y,Z cm |
|---|---|---|---|
| set12-cons-glue.png | [280, 271, 1128, 502] | null | null |
| set12-cons-tabs.png | [436, 67, 973, 702] | null | null |
| set12-frame-mg.png | [546, 55, 862, 717] | 0.000, 0.120, 0.000 | 7.400, 0.900, 15.503 |
| set12-frame-ss.png | [57, 156, 647, 1364] | 0.000, 0.120, 0.000 | 7.400, 0.900, 15.151 |
| set12-soc-6g1.png | [456, 134, 952, 636] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.165 |
| set12-soc-7g3.png | [491, 166, 917, 602] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.178 |
| set12-soc-8g2.png | [459, 139, 949, 629] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.151 |
| set12-soc-d7300.png | [450, 130, 958, 642] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.160 |
| set12-soc-d8300.png | [262, 262, 762, 762] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.151 |
| set12-soc-d9300.png | [467, 148, 940, 621] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.151 |

Diagnostica locale `analysis/fit-set12-pro-recovery.jpg`:6 prove, un SoC per volta con memoria SET11. Insieme alle4 prove SET11 formano10 ipotesi parziali, non10 build funzionanti. L’immagine diagnostica non è caricata nel ramo corrente del repo.

## Pipeline e controlli

Raw AI preservati localmente; chroma-key globale graduato smoothstep e despill2px Pillow/NumPy. Nessun rembg/flood fill/ROI manuale aggiuntivo. Alpha postprodotto, non nativo. Tutti10 nuovi PNG RGBA con alpha0–255 e crop validi.

V15 conserva gli altri140 record e hash; sostituiti solo i10 file rigenerati SET12, con supersedesSha256 e record vecchi archiviati. Tutti150 hash verificati. Lista originale intatta. Restano documentati difetti precedenti: frontale03 etichetta errata, RAM06 marca discordante, batteria07 microtesto, SIM08 tre vani, grafite10 fogli ambigui, frame11 catalogo4:3/16:9, fold14 rapporto errato, aperture cover/fotocamere15 non automaticamente coincidenti. eMMC13 non è UFS. Non nascondere difetti nelle finali.

## Prossimo

Produrre IPA99%100ml e pinzette ESD (2 SKU), poi completare audit e8 tavole finali con PNG effettivi, esploso leggibile, alternative separate e riferimenti riutilizzati dichiarati. Nessuna generazione in background. ViewerV1 storico, non aggiornato a tutti i SET.
