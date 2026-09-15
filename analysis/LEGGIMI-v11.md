# SET Lab — recupero R1 / revisione 11

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
| ant-uwb | NXP UWB+NFC leggibile; fori scontornati. Non Wi-Fi/5G; microtesto decorativo non validato. |
| sim-hybrid | Luxshare HYBRID leggibile, ma sono raffigurati TRE vani anziché due: geometria da correggere; non simulare un carrello fisico valido. |
| hap-z | Nidec Z-axis leggibile, un solo attuatore rotondo con flex. |
| mic-1 | Knowles MEMS leggibile, un microfono con foro acustico. |
| ram-24 | Samsung24GB LPDDR5X10667MHz leggibile; package quasi quadrato, non misura BGA. |
| ram-8x | Micron8GB LPDDR5X8533MHz leggibile. |
| soc-8s | Qualcomm Snapdragon8sGen4 leggibile, non Elite. |
| soc-d9400 | MediaTek Dimensity9400 leggibile. |
| sto-512 | Samsung512GB UFS4.0 leggibile. |
| th-coil | CoolCo VC+Qi2 15W leggibile; bobina e piastra in vista top, materiali non certificati. |

Il carrello SIM ha un difetto geometrico nuovo documentato: tre vani. Rimane da correggere o isolare come illustrazione, non si nasconde il problema per accelerare l’assemblaggio.

## Coordinate e pipeline

Chroma-key globale graduato e despill Pillow/NumPy, stesso processore dei lotti recenti: nessun rembg/flood fill, nessuna trasparenza nativa dichiarata, raw intatti. Tutti10 alpha0–255 e bbox validi.

Le vecchie coordinate SET08 non si applicano automaticamente ai nuovi raster. Per tutti10 `pos,size,angle,boardLocal,boardReference=null` in V11, in attesa del PCB originale SET07 e della nuova verifica. I vecchi record sono archiviati in `analysis/set08-original-records.json`; le composizioni07–08 precedenti sono STALE, non valide per questi nuovi file. Le dimensioni vengono ricalcolate dai crop, senza stirare le immagini né inventare pinout.

| File | Source W,H px | Crop L,T,R,B px |
|---|---|---|
| set08-ant-uwb.png | [1408, 768] | [68, 275, 1340, 500] |
| set08-hap-z.png | [1408, 768] | [479, 60, 929, 708] |
| set08-mic-1.png | [1408, 768] | [488, 191, 920, 572] |
| set08-ram-24.png | [944, 1120] | [210, 292, 734, 828] |
| set08-ram-8x.png | [1024, 1024] | [212, 170, 812, 853] |
| set08-sim-hybrid.png | [1408, 768] | [151, 126, 1256, 642] |
| set08-soc-8s.png | [1408, 768] | [386, 59, 1020, 706] |
| set08-soc-d9400.png | [1024, 1024] | [93, 93, 931, 931] |
| set08-sto-512.png | [1408, 768] | [454, 100, 953, 676] |
| set08-th-coil.png | [1408, 768] | [194, 77, 1334, 692] |

## Prossimi lotti di recupero

- SET09: back-green, bat-7000, board-rf, cam-peri2, camf-12, disp-oled63, frame-mag, glass-zaf, spk-stereo-bot, usb-dp.
- SET10: hap-dual, ram-18, ram-32, soc-8e2, soc-dim95, soc-ten6, sto-1tb41, sto-2tb, th-cu, th-gr2.
- SET11: back-alu, back-leather, bat-dual, cons-screws, frame-classic, soc-exy26, soc-g99, soc-helio, soc-tensor, sto-1tb.
- SET12: cons-glue, cons-tabs, frame-mg, frame-ss, soc-6g1, soc-7g3, soc-8g2, soc-d7300, soc-d8300, soc-d9300.

## Finali

Richiesta8 tavole conservata, zero create. Prima: ripristinare01–07, rigenerare09–12, produrre2 consumabili, rivedere difetti e coordinate, analizzare le immagini reali disponibili. Le tavole useranno PNG effettivi con esploso, alternative separate e riferimenti presi da altri SET dichiarati. Allineamento visivo non equivale a incastro fisico o compatibilità elettrica.
