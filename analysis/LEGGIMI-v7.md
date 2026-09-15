# SET Lab — LEGGIMI corrente, revisione7

**SET01–12 ·120 immagini ·117/149 SKU rappresentati ·32 SKU mancanti**

## Requisito finale aggiornato:8 immagini

La richiesta corrente dell’utente è **8 immagini composite finali, NON20**. Il precedente piano20 è superato e archiviato in `analysis/final-plan-v6-superseded.json`. Il file attivo `final-compositions-plan.json` torna a otto tavole, una per coppia di SET; tutte sono ancora **DA PRODURRE** dopo il completamento del catalogo.

Le tavole riuniranno i PNG effettivi con vista esplosa e varianti separate: motherboard, antenne, camere, batteria, telaio, display, glass, back cover e altre parti. I pezzi mancanti nell’assortimento potranno essere richiamati da SET precedenti, etichettati come riferimenti, non contati come nuovi SKU. Le cinque motherboard del catalogo non diventano otto SKU: tre tavole riuseranno una scheda esistente. Nessuna compatibilità fisica/elettrica viene dedotta dal semplice montaggio grafico.

| Tavola finale | Coppia | Motherboard prevista | Stato |
|---|---|---|---|
| final-pair-01-02.png | 01–02 | set01-pcb-bare.png | NON PRODOTTA |
| final-pair-03-04.png | 03–04 | set03-board-pro.png | NON PRODOTTA |
| final-pair-05-06.png | 05–06 | set05-board-lite.png | NON PRODOTTA |
| final-pair-07-08.png | 07–08 | set07-board-game.png | NON PRODOTTA |
| final-pair-09-10.png | 09–10 | set09-board-rf.png | NON PRODOTTA |
| final-pair-11-12.png | 11–12 | set03-board-pro.png — riferimento riutilizzato | NON PRODOTTA |
| final-pair-13-14.png | 13–14 | set07-board-game.png — riferimento riutilizzato | NON PRODOTTA |
| final-pair-15-16.png | 15–16 | set01-pcb-bare.png — riferimento riutilizzato | NON PRODOTTA |

## Lavoro completato in questo turno

Creato il SET12 con10 asset: sei SoC, due telai, colla e linguette. Letto `ls.ts`, riesaminate tutte le tavole SET01–11 e tutti i nuovi asset; PCB Pro letto in dettaglio. Sei nuove prove grafiche SoC+storage, con riferimenti dichiarati. Il limite10 immagini per turno impedisce di produrre i restanti32 SKU in questa stessa risposta; non e in corso alcuna generazione in background. Prossimo lotto: SET13.

## Materiali spostati in /usr e consegna

Gli ZIP precedenti SET08–11 sono stati spostati dal workspace a **`/usr/set-lab/downloads/`**, verificando l’identità delle copie. Tutti i materiali di lavoro, inclusi i nuovi raw/PNG e le analisi, sono conservati in `/usr/set-lab`.

**Attenzione: /usr non è persistente tra le sessioni.** Conservare gli archivi scaricati. Nel workspace rimangono questo LEGGIMI e la copia del nuovo **`set12-update.zip`** per il download, come negli aggiornamenti precedenti.

Estrarre SET12 nella stessa cartella del primo `set-lab-session.zip` e degli aggiornamenti SET08,09,10,11, unendo le sottocartelle. L’archivio include:
- `new_raw/set12-*.png`, `generated/set12-*.png`:10 raw AI e10 PNG con alpha;
- tavola SET12, metadati, log, prove grafiche e controlli in `analysis/`;
- `coordinates-v7.json`:120 record e cinque schede, compresi riferimenti riutilizzati;
- `catalog-status.csv`, `catalog-missing.json`, `catalog-plan.json`;
- piano finale8, manifest `asset-sha256-v7.json`, script e `uploads/ls.ts` invariato;
- questo LEGGIMI e il precedente storico V6, che contiene il requisito20 ora superato.

Il viewer resta quello storico SET01–06. Nessun aggiornamento o test del renderer3D è dichiarato.

## Pipeline effettiva

Immagini generate singolarmente su magenta, poi **Pillow + NumPy**: chroma-key globale graduato, alpha e despill della fascia di2px vicino alla trasparenza. Nessun rembg, flood fill o segmentatore AI. Formula invariata: `e=min(R,B)-G`, candidato con R/B>100 ed e>35; smoothstep tra35 e110; alpha<3 azzerato. Nel SET12 non sono state necessarie maschere ROI manuali.

Le aperture dei nuovi telai mostrano lo sfondo di composizione. Il liner delle linguette viene mantenuto come parte dell’accessorio; la sua tinta rosata/traslucida non è un matting fisico della pellicola. Il tubetto conserva lievi riflessi violacei sui metalli. Trasparenza postprodotta, non nativa; dati commerciali e materiali non verificati dall’aspetto.

## Revisione multimodale SET12

| Asset | Osservazione |
|---|---|
| set12-cons-glue.png | Tubetto chiuso B-7000 /15ml /SBS PARTS leggibile. Solo accessorio: non dimostra volume reale o formulazione. |
| set12-cons-tabs.png | Tre strisce bianche con estremita arancioni su supporto chiaro rosato. Il supporto e conservato: la sua trasmissione ottica non e un matting fisico. Un solo SKU. |
| set12-frame-mg.png | Telaio chiaro opaco verticale con traversa e cavita visibili. LegaAZ91D e peso138g sono specifiche di catalogo, non misure del raster. |
| set12-frame-ss.png | Telaio scuro lucido in verticale, due grandi aperture e dettagli inferiori. Aspetto metallico, lega316L e peso198g non verificabili. |
| set12-soc-6g1.png | Qualcomm Snapdragon 6 Gen1 leggibile. Simbolo grafico aggiuntivo accanto al marchio illustrativo. |
| set12-soc-7g3.png | Qualcomm Snapdragon 7 Gen3 leggibile, senza segno piu; distinto da soc-7g2 (7+ Gen3). |
| set12-soc-8g2.png | Qualcomm Snapdragon 8 Gen2 leggibile. Non confondere con gli Elite dei SET precedenti. |
| set12-soc-d7300.png | MediaTek Dimensity7300 leggibile. Package quasi quadrato, pinout non verificato. |
| set12-soc-d8300.png | MediaTek Dimensity8300 leggibile, senza Ultra; distinto dal Dimensity8300-Ultra del SET06. |
| set12-soc-d9300.png | MediaTek Dimensity 9300+ leggibile, segno + presente. |

Colla e linguette sono **accessori d’inventario**: nel JSON hanno coordinate di montaggio nulle, anche se il catalogo usa `slot=frame`. Il pack di tre strisce è un unico SKU. I telai sono entrambi verticali e distinti per forma/finitura; non dimostrano che lega, peso o quote siano quelli di catalogo.

## Coordinate dei nuovi SoC: PCB Pro riutilizzato

Il SET12 non crea una nuova motherboard. Si usa `set03-board-pro.png` come riferimento grafico, coerentemente con il SET11. Piazzola maggiore SoC: `[520,203,226,239]` nel raster Pro ritagliato, centro `[633.0,322.5]` px. Fit uniforme `q=min(slot_w/crop_w,slot_h/crop_h)`, centro coincidente, angolo0°. Pinout non verificato.

| SKU | Centro u,v px | W×H disegno px | Margine X/Y per lato px |
|---|---|---|---|
| soc-6g1 | 633.000, 322.500 | 226.000, 226.350 | 0.000 / 6.325 |
| soc-7g3 | 633.000, 322.500 | 226.000, 225.339 | 0.000 / 6.830 |
| soc-8g2 | 633.000, 322.500 | 226.000, 225.670 | 0.000 / 6.665 |
| soc-d7300 | 633.000, 322.500 | 226.000, 225.418 | 0.000 / 6.791 |
| soc-d8300 | 633.000, 322.500 | 226.000, 226.000 | 0.000 / 6.500 |
| soc-d9300 | 633.000, 322.500 | 226.000, 226.652 | 0.000 / 6.174 |

### Sei nuove prove parziali

Ogni nuovo SoC è mostrato sul PCB SET03 con `set11-sto-1tb.png`. L’assegnazione storage sul Pro resta **ipotetica**, evidenziata in ambra; non è la sede RF bloccata. Nessuna RAM è montata e non si tratta di dispositivi completi. Sommando le quattro prove SET11 alle sei SET12, il registro della coppia11–12 comprende10 varianti SoC+storage illustrate.

Questa tavola diagnostica non è una delle otto immagini finali. Non si sovrappongono più SoC sulla stessa sede e non si dichiarano compatibilità Qualcomm/MediaTek/Google/Samsung/Unisoc.

### Registro nuovo: crop e cm nominali

Centro X,Y,Z di simulazione: X destra, Y spessore, Z verso il basso. Bbox dopo rotazione; angolo positivo orario in2D, non yaw Three.js verificato. Per il Pro `s=min(6.55/Wpcb,7.10/Hpcb)`, X=0.05+(u−Wpcb/2)*s, Z=−3.35+(v−Hpcb/2)*s. Y e centri dei telai derivano dalla baseline `ls.ts`. Queste sono coordinate grafiche riproducibili, non misure di incastri reali.

| File | Crop [L,T,R,B] px | Centro X,Y,Z cm | Bbox X,Y,Z cm | ° | Stato |
|---|---|---|---|---:|---|
| set12-cons-glue.png | [620, 87, 788, 681] | — | — | — | SOLO INVENTARIO ACCESSORI; non montare nel frame |
| set12-cons-tabs.png | [508, 64, 900, 715] | — | — | — | SOLO INVENTARIO ACCESSORI; non montare nel frame |
| set12-frame-mg.png | [40, 52, 665, 1454] | 0.000, 0.120, 0.000 | 7.044, 0.900, 15.800 | 0 | proposta grafica nominale; sede non verificata |
| set12-frame-ss.png | [90, 101, 677, 1276] | 0.000, 0.120, 0.000 | 7.400, 0.900, 14.813 | 0 | proposta grafica nominale; sede non verificata |
| set12-soc-6g1.png | [189, 189, 834, 835] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.153 | 0 | fit grafico SoC su PCB Pro riutilizzato |
| set12-soc-7g3.png | [170, 171, 854, 853] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.148 | 0 | fit grafico SoC su PCB Pro riutilizzato |
| set12-soc-8g2.png | [170, 170, 854, 853] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.149 | 0 | fit grafico SoC su PCB Pro riutilizzato |
| set12-soc-d7300.png | [124, 125, 900, 899] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.148 | 0 | fit grafico SoC su PCB Pro riutilizzato |
| set12-soc-d8300.png | [102, 102, 922, 922] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.151 | 0 | fit grafico SoC su PCB Pro riutilizzato |
| set12-soc-d9300.png | [165, 165, 858, 860] | -0.001, 0.285, -3.403 | 1.151, 0.100, 1.154 | 0 | fit grafico SoC su PCB Pro riutilizzato |

I precedenti110 record restano invariati nel JSONV7. Non convertire null in zero: i consumabili non hanno coordinate di montaggio; restano bloccati RAM/UFS del Lite e storage del SET10 sul RF.

## Stato delle revisioni precedenti

Confermati nel riesame: ritaglio USB SET01 per bande bianche; RAM LPDDR con rapporto differente dalla sede; camera32MP SET03 con stampa52MP; marca RAM16 SET06 incoerente con catalogo; PCB Lite senza sede RAM/UFS; microtesto batteria6000 SET07 contraddittorio; antenna UWB/NFC non automaticamente Wi-Fi; PCB RF con componenti nella piazzola UFS, ancora bloccata; LRA SET10 con marcatura2x duplicata; telaio classico SET11 con vista composita e cavità ripulita via alpha manuale. I rispettivi raw restano invariati e i difetti non vengono nascosti da sovrapposizioni.

## Catalogo residuo

**117 SKU rappresentati su149;32 mancanti.** I120 file includono i tre alias/duplicati di rappresentazione già registrati. “Rappresentato” non significa verificato tecnicamente. I consumabili futuri rimarranno accessori separati.

| Lotto | SKU | Stato |
|---|---|---|
| 13 | `soc-ex2500`, `soc-tensor4`, `soc-kirin`, `ram-12lp4`, `sto-32`, `sto-256u4`, `sto-512u31`, `bat-3500`, `bat-4000`, `bat-5500` | NON GENERATO |
| 14 | `bat-8000`, `bat-stacked`, `disp-lcd67`, `disp-oled61`, `disp-fold`, `disp-eco`, `glass-gg3`, `glass-gg7`, `glass-utg`, `back-red` | NON GENERATO |
| 15 | `back-black`, `back-white`, `back-carbon`, `back-wood`, `cam-uw`, `cam-peri10`, `spk-hires`, `usb-pd`, `cons-thermalp`, `cons-kapton` | NON GENERATO |
| 16 (2/10, residuo) | `cons-ipa`, `cons-tweezers` | NON GENERATO |

Tre lotti completi da10 e residuo finale2. Non si inventano8 SKU per chiamare il lotto16 un SET completo. L’ultima tavola finale potrà includere il residuo e riferimenti dichiarati ad altri SET senza modificare il conteggio del catalogo. Qualsiasi vista complementare va etichettata come vista, non come SKU nuovo.

## Controlli

- 12 SET da10 immagini:120 file e120 hash distinti; vecchi110 invariati.
- 10 nuovi PNG con alpha0–255, crop validi, proporzioni conservate.
- Sei nuovi SoC contenuti nella piazzola Pro con scala uniforme; due accessori esclusi dal montaggio.
- Sei prove parziali prodotte per lettura visiva;10 prove cumulate nella coppia11–12, con ipotesi UFS dichiarata.
- Piano residuo di32 SKU senza duplicati; piano finale attivo8 output, zero prodotti.
- ZIP precedenti spostati in /usr con verifica hash; nuovo aggiornamento disponibile nel workspace per il recupero.
