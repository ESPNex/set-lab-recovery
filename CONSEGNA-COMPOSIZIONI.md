> **Aggiornamento audit elettronico (16/09/2026): nessuna configurazione collaudata.** Nove delle 29 composizioni hanno un conflitto RAM documentato; le restanti non sono approvate. Le immagini sono concept storici. Leggere [audit elettronico](electronics-audit/AUDIT-ELETTRONICO.md). Nuove immagini di assemblaggi tecnici sospese fino a disponibilità di progetto e prove reali.

# Composizioni finali V17 — senza fold

## Consegna effettiva

**29 PNG da 2200×1600 pixel**, composti a partire dai componenti esistenti, in `finals/`. Galleria offline con filtro per coppia: **`finals/viewer.html`**. Non sono le contact sheet di controllo: ciascun PNG contiene un esploso illustrativo con scocca, telaio, motherboard con chip dove le sedi grafiche sono individuate, batteria, display e vetro; moduli separati in basso e alternative/utensili a destra.

| Coppia | Immagini | Criterio principale |
|---|---:|---|
| SET01 + SET02 | 1 | Una selezione principale; altre immagini Wi-Fi/termiche visibili a lato |
| SET03 + SET04 | 2 | Due SoC e due RAM |
| SET05 + SET06 | 2 | Due SoC e due RAM |
| SET07 + SET08 | 2 | Due SoC e due RAM |
| SET09 + SET10 | 3 | Tre SoC, con memorie/termiche alternate |
| SET11 + SET12 | 10 | Dieci SoC; tre telai e due scocche alternati |
| SET13 + SET14 | 5 | Cinque batterie; tre SoC, tre display non-fold e memorie alternate |
| SET15 + SET16 | 4 | Quattro scocche; due moduli camera alternati, utensili sul banco |
| **Totale** | **29** | **Numero ricavato dai componenti, non imposto a 8** |

Criterio: per ogni coppia, massimo numero di varianti distinte in un ruolo principale; selezione ciclica degli altri ruoli. Non è un prodotto cartesiano né una matrice di compatibilità. Ogni componente attivo della coppia appare nelle sue composizioni, come selezione principale o alternativa/banco. Non sono 29 modelli di telefono realmente funzionanti.

## Esclusioni richieste

`disp-fold` escluso dalle finali. Anche `glass-utg`, vetro dedicato al fold, escluso per coerenza: nessuna configurazione pieghevole o back cover inventata. I due file restano nello storico e nel catalogo originario, con flag di esclusione in `coordinates-v17.json`; la lista originale non viene falsificata.

- Catalogo storico completo: **149 SKU / 152 asset**.
- Selezione attiva non-fold: **147 SKU / 150 asset**, tutti rappresentati nelle composizioni della rispettiva coppia.
- Nessun fold/UTG compare nelle selezioni, negli inventari o nei pixel compositati da quei file.

## Correzioni effettivamente applicate

1. Frontale SET03: scritta resa esplicitamente **32 MP AF**.
2. RAM16 SET06: etichetta editoriale **SK hynix / 16 GB / LPDDR5X / 9600 MHz**, coerente con la lista; rimossi marca/codice Samsung e unità Mbps del vecchio raster.
3. Grafite SET10: eliminata la sagoma superiore aggiuntiva; restano due fogli visibili. Crop e dimensioni aggiornati mantenendo le proporzioni.
4. Dimensity8300 SET12: rimossi codice MT6880V e sigle CPU/GPU non verificate, mantenuto il nome principale.

Sono ritocchi deterministici di etichette/sagome su immagini AI, **non fotografie autentiche di marcature del produttore**. Nessuna nuova generazione AI in questo turno. Hash prima/dopo in `analysis/v17-editorial-corrections.json`; originali pre-correzione recuperabili dal commit V16 `32f7d6cea73af18ccb45c0699d4c5fafc8126e67` e dagli archivi storici. Il nome della cartella `originals` indica la provenienza storica, non l'assenza di questa correzione V17.

## Posizionamento e limiti

- `finals/composition-manifest.json`: selezioni, inventari, provenienza, SHA256 e rettangolo pixel di **ogni** immagine compositata, scala e rotazione.
- `coordinates-v17.json`: coordinate nominali di catalogo, crop e sedi motherboard; non dimensioni di fabbricazione.
- Livelli esterni separati a scala nominale comune 41 px/cm; nessuna deformazione del rapporto raster. Batterie adattate proporzionalmente al riquadro del nucleo. Ingrandimenti dei moduli e dell'inventario indipendenti, come indicato sulle immagini.
- Chip contenuti al 90% delle sedi grafiche individuate. Pro03: solo SoC sovrapposto; RAM/UFS restano separati per ambiguità. Lite05: stesso criterio, perché mancano sedi esplicite RAM/UFS.
- eMMC `sto-32` non viene montata su una sede UFS. SIM ibrida e camere non vengono forzate in aperture non dimostrate compatibili.
- Mancano motherboard/display o altri ruoli in alcune coppie: i riferimenti riutilizzati sono marcati con **asterisco**, elencati in basso e tracciati nel manifest.
- Telai, back cover, vetri e camere **non sono certificati combacianti**. Le loro differenze rimangono visibili. Anche accoppiamenti SoC/RAM/storage sono editoriali, non elettronici.

## Revisione della consegna

Esaminate multimodalmente 8 tavole di controllo con tutte le 29 composizioni; approfondite le immagini singole 11–12 v09, 13–14 v02 e 15–16 v04. Riesaminata anche la tavola dei quattro ritocchi; il Dimensity8300 finale è stato ulteriormente pulito prima del compositing.

Controlli automatici: nessun rettangolo fuori canvas; 150/150 asset attivi coperti nella propria coppia; 0 asset esclusi compositati; 29 immagini con hash distinti. Questo controllo non equivale a leggere ogni microtesto né a validare CAD/pinout/materiali.

## Repository e recupero

Progetto `/usr/set-lab`; clone di controllo `/usr/set-lab-review/repo`, aggiornato dopo push. In Git sono presenti i 152 PNG di catalogo più i 29 PNG finali richiesti, **non** raw o contact sheet diagnostiche. Il vecchio audit V16 resta come documento storico riferito al suo commit: per il tree corrente usare manifest V17 e questa consegna.

`/usr` non è persistente: recupero aggiornato da GitHub privato https://github.com/ESPNex/set-lab-recovery. Il bundle nel workspace resta storico. La galleria finale è nuova; il precedente viewer del catalogo originale resta storico e distinto.
