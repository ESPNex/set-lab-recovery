# SET Lab — revisione13 / recupero SET10

## Stato verificato

**SET13–15 presenti e integri:30 PNG. SET10 rigenerato:10 nuovi PNG.** Disponibili ora130 asset (SET01–10,13–15), tutti verificati contro il manifest corrente. Restano SET11–12:20 immagini da rigenerare e2 SKU mai prodotti (IPA e pinzette). Registro storico150 file/147 SKU su149, NON150 file disponibili.

**8 tavole finali confermate, zero prodotte.** Le12 diagnostiche RF di questo turno non sono le finali.

## GitHub — backup remoto riuscito

**Repository privato: https://github.com/ESPNex/set-lab-recovery**

Autorizzazione riuscita come ESPNex, repository creato e push verificato: commit locale uguale a main remoto, inventario dell’albero GitHub con **130 PNG asset +70 raw**. Sono inclusi direttamente anche i70 originali recuperati SET01–07 e il viewer V1: il remoto non dipende dal solo collegamento Catbox.

L’errore precedente era il salvataggio delle credenziali in una directory /usr non scrivibile: l’utente aveva autorizzato correttamente. Directory creata, permessi corretti, nuova autorizzazione salvata fuori dal progetto, mai inclusa in Git. Accesso HTTPS; repository privato, nessun token/password in chat o nei file del progetto.

`analysis/github-backup-verification.json` registra il commit del caricamento degli asset, conteggio remoto e privacy. Recupero consigliato dopo un reset: autenticarsi e `git clone https://github.com/ESPNex/set-lab-recovery.git`. /usr resta non persistente, ma i file sono ora caricati su GitHub.

Il bundle nel workspace resta il checkpoint **precedente al caricamento degli originali su GitHub**, commit db10b994: contiene60 asset SET08–10,13–15 con raw, non i70 originali. Non va confuso con il repository remoto più completo. Conservare comunque lo ZIP originale https://files.catbox.moe/ujc2ul.zip. Nessun file viene eliminato da /usr durante questa verifica.

## Analisi multimodale

Riesaminate13 tavole: SET01–10,13–15,130 asset. PCB RF09-R1 e grafite10 letti anche a piena risoluzione. SET11–12 assenti non riesaminati.

| SKU SET10 | Esito |
|---|---|
| soc-8e2 | Qualcomm Snapdragon8 Elite Gen5 leggibile; slash decorativi stampati fra righe. Il nome SKU8e2 non significa Gen2. |
| soc-dim95 | MediaTek Dimensity9500 leggibile, distinto da9400. |
| soc-ten6 | Google TensorG6 leggibile, distinto daG4/G5. |
| ram-18 | SK hynix18GB LPDDR5X9600MHz leggibile. |
| ram-32 | SK hynix32GB LPDDR5X10667MHz leggibile. |
| sto-1tb41 | KIOXIA1TB UFS4.1 leggibile; non4.0. |
| sto-2tb | SAMSUNG2TB UFS4.1 leggibile. |
| hap-dual | Esattamente due involucri Leaderdrive, marcati LRA L e LRA R; nessun2x ripetuto. Restano separati, non assumere una sede unica per entrambi. |
| th-cu | CoolCo/Cu/0.4mm leggibile; strip rame appiattita molto allungata. Spessore illustrativo non misurato. |
| th-gr2 | CoolCo Dual graphite0.2+0.2mm leggibile; contorni sovrapposti suggeriscono un terzo foglio. Geometria/conteggio ambiguo: inventario separato, correzione richiesta. |

La grafite ha un problema di conteggio/contorni: non correggerlo attribuendo automaticamente i margini a spessori reali. Inventario separato con segnalazione di correzione. Doppio LRA: un file inventario con due motori L/R, non due motori nella stessa sede singola. Entrambi gli asset hanno montaggio nullo.

## Coordinate nuove sul RF09-R1

PCB originale del SET09 precedente perduto; qui si usa ESCLUSIVAMENTE RF09 rigenerato: crop[82,79,1331,692], raster1249×613. Sedi libere: SoC[162,131,341,350],RAM[601,127,206,356],UFS[899,180,216,252]. Scala nominale s=min(6.55/1249,7.10/613), X=0.05+(u−1249/2)s, Z=−3.35+(v−613/2)s, Y da `ls.ts`. Nessun pinout ingegneristico.

Fit uniforme q=min(sedeW/cropW,sedeH/cropH), centro coincidente,0° di rotazione raster. Nessuno stiramento. Le UFS sono incluse perché la nuova sede è libera, non perché sia stata provata compatibilità elettronica.

| SKU | Centro u,v px | Disegno W,H px |
|---|---|---|
| ram-18 | 704.000, 305.000 | 206.000, 295.958 |
| ram-32 | 704.000, 305.000 | 206.000, 306.834 |
| soc-8e2 | 332.500, 306.000 | 341.000, 339.769 |
| soc-dim95 | 332.500, 306.000 | 341.000, 344.123 |
| soc-ten6 | 332.500, 306.000 | 341.000, 342.464 |
| sto-1tb41 | 1007.000, 306.000 | 216.000, 237.192 |
| sto-2tb | 1007.000, 306.000 | 216.000, 251.337 |

### Dodici prove

3SoC×2RAM×2UFS, una sola variante per ruolo in ogni prova. `analysis/fit-set10-rf-recovery-1.jpg` e `-2.jpg`:6 combinazioni ciascuna. Nessuna asserzione di motherboard reale compatibile con tutti i SoC/RAM, nessun circuito funzionante certificato. Periferiche e strati termici non inclusi sotto i chip per nascondere difetti.

| File SET10 | Crop L,T,R,B px | Centro X,Y,Z cm | Bbox X,Y,Z cm |
|---|---|---|---|
| set10-hap-dual.png | [74, 229, 1335, 632] | null | null |
| set10-ram-18.png | [100, 214, 716, 1099] | 0.467, 0.275, -3.358 | 1.080, 0.080, 1.552 |
| set10-ram-32.png | [185, 211, 708, 990] | 0.467, 0.275, -3.358 | 1.080, 0.080, 1.609 |
| set10-soc-8e2.png | [427, 111, 981, 663] | -1.481, 0.285, -3.353 | 1.788, 0.100, 1.782 |
| set10-soc-dim95.png | [431, 110, 977, 661] | -1.481, 0.285, -3.353 | 1.788, 0.100, 1.805 |
| set10-soc-ten6.png | [471, 150, 937, 618] | -1.481, 0.285, -3.353 | 1.788, 0.100, 1.796 |
| set10-sto-1tb41.png | [439, 93, 969, 675] | 2.056, 0.275, -3.353 | 1.133, 0.080, 1.244 |
| set10-sto-2tb.png | [459, 101, 948, 670] | 2.056, 0.275, -3.353 | 1.133, 0.080, 1.318 |
| set10-th-cu.png | [83, 318, 1325, 450] | 0.200, 0.000, -3.500 | 5.600, 0.070, 0.595 |
| set10-th-gr2.png | [216, 110, 1192, 658] | null | null |

Heatpipe con collocazione nominale dello slot thermal, non forma misurata della vasca. Spessore0.4mm stampato non sostituisce il valore nominale del catalogo. Haptics/grafite isolati senza coordinate assegnate.

## Pipeline e integrità

Raw AI preservati,10 generazioni del turno. Alpha postprodotto: Pillow/NumPy global chroma-key smoothstep e despill2px. Nessun rembg/flood fill, nessuna ROI manuale nuova. Etichette illustrate non sono specifiche fisiche verificate.

Manifest V13:150 hash storici,130 file locali verificati; i120 asset già disponibili sono invariati. Solo i10 hash SET10 sostituiti, precedenti hash riportati nei record come supersedesSha256. Vecchi record SET10 archiviati; tutti gli altri140 record restano invariati.

Rilievi storici ancora validi: USB01 bande bianche, frontale03 stampa52MP, RAM06 marchio non conforme, Lite senza RAM/UFS identificabili, batteria07 microtesto contraddittorio, SIM08 tre vani, fold14 rapporto errato, aperture cover15 non coincidenti automaticamente con le camere. eMMC13 separata da UFS. Non nascondere questi problemi nelle finali.

## Prossimo lotto

SET11: back-alu,back-leather,bat-dual,cons-screws,frame-classic,soc-exy26,soc-g99,soc-helio,soc-tensor,sto-1tb. Poi SET12 e2 consumabili. Infine8 tavole da PNG effettivi, esploso leggibile, alternative separate e riferimenti motherboard riutilizzati dichiarati. Viewer V1 non aggiornato in questo turno; niente generazione in background.
