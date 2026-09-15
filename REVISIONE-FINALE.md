# Revisione finale del catalogo — V16

Revisione del 16 settembre 2026. **Catalogo completo; revisione conclusa con correzioni aperte. Non è un collaudo ingegneristico e non è la consegna delle 8 composizioni finali.**

## Provenienza indipendente

Repository privato: https://github.com/ESPNex/set-lab-recovery

Nuovo clone scaricato da GitHub in `/usr/set-lab-review/repo`. Commit degli asset esaminati: `32f7d6cea73af18ccb45c0699d4c5fafc8126e67`. Il successivo commit documentale non modifica le immagini. Analisi e tavole diagnostiche restano in `/usr/set-lab-review/analysis`, fuori dal clone e dal ramo Git.

## Risultati verificati

- **149/149 SKU rappresentati, 0 mancanti; 152 PNG con 152 hash distinti.**
- SET01–15: 10 immagini ciascuno. SET16: 2 residui, senza inventare altri articoli.
- Tutti i 152 hash coincidono con `asset-sha256-v16.json`; tutti i PNG sono RGBA con trasparenza e crop registrati entro i limiti.
- Nessuna immagine raw/diagnostica nel tree corrente; i vecchi file nella storia Git non sono stati cancellati retroattivamente.
- Lista originale `uploads/ls.ts`: 149 SKU; hash normalizzato LF coincidente con il registro. La differenza CRLF/LF non è corruzione.
- 29/29 posizionamenti `boardLocal` contenuti nelle rispettive sedi registrate; nessuna discrepanza di rapporto oltre l'1% nel test size/crop/angolo. Sono controlli matematici sui metadati, **non prova che le sedi o le misure fisiche siano corrette**.
- 20 record senza posizione: non forzati dentro un telefono.

152 immagini anziché 149 perché sono conservate alternative storiche per `ant-wifi5`, `mic-1` e `th-vc`; non sono duplicati byte per byte.

## Revisione multimodale realmente eseguita

Lette tutte le **16 tavole del clone scaricato**, comprendenti i 152 asset. Approfonditi a risoluzione del crop: 5 motherboard e 9 dettagli (frontale32, RAM16, batteria6000, SIM ibrida, grafite dual, fold, Dimensity8300, IPA e pinzette). I restanti asset sono stati riesaminati alla scala delle tavole: questo non permette di certificare ogni microcarattere. Esito per file in `analysis/asset-audit.csv`.

### Ultimi due articoli

- **IPA:** bottiglia SBS Parts, scritte IPA 99% e 100 ml leggibili, pittogramma infiammabilità. Rappresentazione di inventario, non contenuto chimico certificato.
- **Pinzette ESD:** un paio nero, punte metalliche e scritta SBS Parts / ESD; orientamento raster orizzontale. Inventario, non componente montato.

Entrambi hanno coordinate di montaggio nulle. Alpha ottenuto in postproduzione con chroma key globale e despill, non nativo.

## Correzioni e limiti aperti

| Asset/gruppo | Riscontro e azione |
|---|---|
| SET03 frontale 32 MP | Marcatura S2/52 MP ambigua, non 32 MP chiaramente leggibile. Correggere rispetto al catalogo Sony IMX615 32 MP AF. |
| SET06 RAM 16 GB | Raster Samsung, catalogo **SK Hynix**: correggere marca. Capacità e 9600 non risolvono la discordanza. |
| SET08 SIM ibrida | Tre vani visibili; geometria e accoppiamento non validati, mantenere fuori montaggio automatico. |
| SET10 grafite dual | Tre sagome/fogli visibili nonostante “Dual / 0.2 + 0.2 mm”: chiarire o correggere il numero. |
| SET12 Dimensity 8300 | Nome principale corretto; sigle MT6880V, CPU/GPU aggiuntive non verificate nel catalogo. Rimuovere o verificare prima di usarle come specifica. |
| SET14 fold / UTG | Rapporto dell'area attiva, frame e vetro non validati; il raster largo non dimostra corrispondenza alla risoluzione scritta. |
| Cover/camere SET09 e SET15 | Aperture e geometrie non dimostrate coincidenti; non nascondere le incongruenze nelle finali. |
| Frame classico SET11 | Indicazioni catalogo 4:3/16:9 ambigue: non trattare il disegno come misura autorevole. |
| Vetri, superfici e alpha | Trasparenza ottica/materiali non certificati. SET07 hard key con rischio frange; recuperi successivi smooth key. Nessun rembg/flood fill. |

**Rettifica batteria SET07:** il dettaglio scaricato mostra 6000 mAh / 23.52 Wh, coerenti con 3.92 V e con 23.5 Wh arrotondati. La precedente segnalazione di capacità contraddittoria è ritirata; l'immagine non è stata modificata. RGB magenta nascosto a alpha=0 non va confuso con contaminazione visibile: nei cinque file campionati non risultano pixel magenta opachi secondo la soglia testata.

## Coordinate motherboard

Coordinate in pixel del raster ritagliato: rettangoli `[x,y,larghezza,altezza]`. Posizione globale, dimensioni e rotazione di ciascun asset rimangono in `coordinates-v16.json`, senza inventare nuove misure durante l'audit.

| Scheda / raster | SoC | RAM | Storage |
|---|---|---|---|
| Std01 / 508×660 | 139,244,158,157 | 129,449,174,114 | 356,350,132,157 |
| Pro03 / 1286×666 | 520,203,226,239 | 786,184,119,123 | 786,342,119,121 |
| Lite05 / 1265×646 | 470,158,327,328 | Non individuata | Non individuato |
| Game07 / 1272×639 | 225,209,229,228 | 585,185,214,252 | 938,123,213,241 |
| RF09 / 1249×613 | 162,131,341,350 | 601,127,206,356 | 899,180,216,252 |

Pro03: assegnazione RAM/UFS ipotetica, etichette condivise/ambigue, raster largo rispetto alle dimensioni nominali. Lite05: il solo SoC evidente non autorizza sedi RAM/UFS inventate. RF09: RAM rettangolare alta; nessuna validazione package/pinout. Gli angoli raster non sono automaticamente gli yaw Three.js del catalogo.

## Stato finale e seguito

**Catalogo: completo. Audit del download: completato. Prontezza tecnica: non certificata, correzioni aperte. Composizioni finali: 0/8.** Le tavole di controllo e i fit parziali non contano come finali. Viewer storico ancora limitato ai 60 asset originali.

Prima delle finali: correggere etichette/conteggi oppure esplicitare le limitazioni, risolvere le sedi ambigue e produrre 8 esplosi leggibili con alternative separate e riferimenti presi da altri SET dichiarati. Non avviata alcuna generazione in background.

File di prova: `analysis/download-integrity.json`, `analysis/coordinate-checks.json`, `analysis/asset-audit.csv`, `analysis/review-readiness.json`. `/usr` resta non persistente; il backup aggiornato è il repository GitHub verificato. Il bundle nel workspace è storico e non contiene V16.
