# SET Lab — Viewer dei componenti

Aprire **viewer.html** in un browser moderno. È autonomo: include tutte le 60 immagini come derivati WebP trasparenti, senza dipendenze di rete. Per scaricare le coordinate dal viewer, usare preferibilmente il file aperto nel browser fuori dall’anteprima incorporata.

## Contenuto
- Tre tavole distinte: SET 01–02, SET 03–04, SET 05–06, ciascuna con 20 asset nell’inventario.
- Motherboard con componenti centrati sulle piazzole riconoscibili; area esplosa per gli altri pezzi.
- Selezione, trascinamento, zoom, visibilità, dimensionamento proporzionale, rotazione, livello Z.
- Esportazione JSON/CSV e importazione delle trasformazioni JSON.
- `coordinates.json`: coordinate iniziali di tutti i 60 asset, ritagli nativi, note e piazzole locali.
- I PNG sorgente sono conservati separatamente in `originals/` nel workspace; non sono inclusi nel piccolo pacchetto del viewer.

## Convenzioni
Tavola 1800 × 1200 pixel logici; origine in alto a sinistra; X verso destra, Y verso il basso. X/Y sono il **centro del ritaglio**, W/H le dimensioni prima della rotazione, angolo positivo orario. Tutti i componenti iniziano a 0° perché sono mostrati nell’orientamento delle immagini, non in un orientamento di montaggio certificato.

Le piazzole `slot` sono rettangoli (x,y,w,h) nei pixel del raster motherboard ritagliato. `crop` è [sinistra, alto, destra, basso] nel PNG originale. Le coordinate sono deterministiche per la composizione grafica, non misure fisiche. Le cifre decimali non indicano accuratezza meccanica.

## Piazzole stimate visivamente
| Coppia | Sede | x | y | w | h | Attendibilità dell’attribuzione |
|---|---|---:|---:|---:|---:|---|
| 01–02 | SoC | 139 | 244 | 158 | 157 | Serigrafia SoC visibile |
| 01–02 | RAM | 129 | 449 | 174 | 114 | Serigrafia LPDDR; rapporto d’aspetto diverso dal chip |
| 01–02 | Storage | 356 | 350 | 132 | 157 | Serigrafia UFS visibile |
| 03–04 | SoC | 520 | 203 | 226 | 239 | Piazzola grande nell’area comune SOC/RAM/UFS |
| 03–04 | RAM | 786 | 184 | 119 | 123 | Attribuzione ipotizzata, non univoca |
| 03–04 | Storage | 786 | 342 | 119 | 121 | Attribuzione ipotizzata, non univoca |
| 05–06 | SoC | 470 | 158 | 327 | 328 | Serigrafia U1 SoC visibile |

## Risultato dell’analisi e limiti
Sono state esaminate tutte le immagini in sei tavole visuali, con ulteriore lettura in dettaglio dei tre PCB. Ogni SET contiene effettivamente 10 file. Le coppie sono interpretate come consecutive in base all’organizzazione fornita.

Non si può ricavare un montaggio completo affidabile dai dati: mancano scala comune, quote e pinout. Il PCB Lite presenta solo una piazzola SoC sul lato mostrato. I due SoC dei SET 04/06 e le due RAM dei SET 04/06 sono trattati come alternative di inventario, non come componenti da sovrapporre e neppure come alternative elettricamente compatibili. Nel SET 06 entrambe le RAM sono inizialmente mostrate separate nell’area esplosa.

Le periferiche, le parti del telaio e gli strati display/cover restano esplosi: le loro coordinate indicano un posto nella tavola, **non una posizione di montaggio sulla motherboard**. Non sono stati inventati connettori, incastri o orientamenti.

Anomalie: set04-soc-8e reca “8 Gen 3”; set04-soc-7g2 reca “7+ Gen 3”; set06-soc-vertv2 reca “Exynos 2400”; set06-soc-q6 reca “Dimensity 8300-Ultra”; set03-camf-32 presenta la stampa “52MP”. Il PNG set01-usb-flex include bande laterali bianche opache, escluse solo dal ritaglio del viewer. Le grafiche non costituiscono una distinta base tecnica verificata.

Test automatico Chromium: apertura senza errori JavaScript; cambio delle tre coppie; visibilità motherboard; ripristino visibilità; comando zoom. La resa della prima tavola è stata verificata anche tramite screenshot.
