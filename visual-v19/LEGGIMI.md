# V19 — una sola RAM e una sola archiviazione

**29 immagini PNG 2800×1850**, con galleria HTML offline filtrabile per coppia. Le immagini sono in questa cartella; le coordinate di presentazione e gli esiti sono in `posizionamenti-v19.json`.

## Correzione richiesta

In ciascuna tavola compare **esattamente una RAM e una memoria di archiviazione** (UFS oppure eMMC). Rimosse tutte le memorie alternative laterali e l'ingrandimento della motherboard che ripeteva i chip. Quando la sede non è dimostrata, la memoria selezionata appare solo nel riquadro dei componenti con sede sospesa, non anche sulla scheda.

Il vincolo è controllato su ogni tavola, contando le effettive operazioni di compositing per ruolo; non soltanto le voci della selezione. I restanti rettangoli dorati disegnati nel PCB sono sedi del raster, non ulteriori chip installati.

## Repository scaricato e lettura multimodale

Nuovo clone indipendente da GitHub in **`/usr/set-lab-review-v19/repo`**, commit sorgente `6fe4f2f1e716760f2b7d44237f9bf825655f7177`. Verificati i 152 hash dei componenti. Le immagini usate provengono da questo download.

Riesaminate otto tavole sorgente, una per coppia, con tutte le varianti selezionate di motherboard, telaio, cover, camera posteriore, display, vetro e batteria. Il confronto riguarda forma, orientamento, apertura, tipo di vista, traverse, rail e disposizione delle lenti. Non è un semplice test di somiglianza tra rettangoli o conteggio dei pixel. Riesaminate anche le otto tavole dei risultati V19, comprendenti tutte le 29 composizioni.

## Riscontri concreti

- **Telaio classic:** il raster rappresenta un frontale con tasto Home e feritoia superiore; non consente di identificare una vasca interna. La sovrapposizione è un confronto, non un incastro dimostrato.
- **Telaio flat:** vasca batteria stretta a sinistra e rail ampio a destra. Riposizionato il riquadro grafico della batteria a sinistra. La scala del rendering rimane illustrativa: non significa che la cella reale sia stata misurata o resa fisicamente compatibile ridimensionandola.
- **Telaio titanio:** una cornice aperta non rivela supporti interni, viti o appoggi del PCB.
- **Telaio magnetico:** l'anello centrale non permette di ricostruire automaticamente spessori e piano di appoggio della batteria.
- **Cover multifornate:** moduli a due lenti affiancate e periscopi non corrispondono automaticamente a tre fori verticali o a isole con altre aperture. Non è stato dichiarato il montaggio delle lenti nei fori.
- **Vetro 7i:** foro superiore decentrato rispetto ai display selezionati con camera centrale; accoppiamento ottico segnalato come non accettato.
- **Vetro GG3:** fessura superiore diversa da notch/foro dei display; non trattata come equivalente.

Gli esiti specifici compaiono nella sezione **Lettura degli incastri** di ogni immagine. I confronti telaio/PCB restano visibili per mostrare il problema, non come prova di montaggio riuscito.

## Limiti, senza ambiguità

L'analisi multimodale può riconoscere dove il disegno suggerisce un alloggiamento e dove le forme si contraddicono. Non ricava dai PNG l'interno non visibile, le tolleranze, l'altezza dei connettori, il pinout o l'effettiva saldabilità. **Nessuna delle 29 configurazioni è dichiarata fisicamente collaudata o pronta per la fabbricazione.**

I numeri nel JSON servono a riprodurre la tavola, non a sostituire questa distinzione. Restano applicate le precedenti sostituzioni dei nove abbinamenti di tipo RAM errati e la selezione UFS2.2 per G99, senza estenderle a una qualifica elettronica completa. Fold e UTG restano esclusi.

Le memorie alternative non selezionate sono conservate nel catalogo e nelle versioni storiche, ma **non vengono più mostrate in queste tavole**. Di conseguenza la vecchia regola “ogni asset in ogni coppia” non prevale sulla nuova richiesta di una sola memoria per ruolo.

V18 conservata nel repository (`visual-v18/`) e nello ZIP `/usr/set-lab-delivery/Configurazioni-V18.zip`; i duplicati del workspace sono stati rimossi solo dopo verifica degli hash, lasciando spazio alla consegna aggiornata. `/usr` non è persistente: il progetto aggiornato è anche su GitHub dopo push verificato.
