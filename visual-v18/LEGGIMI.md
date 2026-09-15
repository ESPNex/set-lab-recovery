# V18 — posizionamento ricavato dalle immagini

29 PNG, **2800×1850 pixel**, organizzati per coppia: 01–02 (1), 03–04 (2), 05–06 (2), 07–08 (2), 09–10 (3), 11–12 (10), 13–14 (5), 15–16 (4).

Aprire **GALLERIA.html** per filtrare le coppie. Le anteprime sono incorporate e funzionano offline. Le immagini PNG sono nella stessa cartella.

## Cosa cambia rispetto alla V17

- Il nucleo con motherboard e batteria è ora sovrapposto al telaio, non semplicemente affiancato.
- Sei piani separano cover, retro/termica, telaio+nucleo, bordi/flex, display e vetro. I piani sono sfalsati sulla pagina solo per leggibilità: non rappresentano distanze reali tra gli strati.
- Regioni delle finestre/isole camera stimate visivamente per ciascuna cover ed evidenziate in rosso. Non sono misure dei centri di tutte le lenti.
- Fotocamera posteriore e termica hanno una proposta di posizione nel piano retro; periferiche numerate nel piano bordi/flex con coordinate locali.
- Vetri e display mantengono sagome, rapporti e fori originali. Il riferimento rosso superiore indica una zona da verificare, non un foro misurato aggiunto all'asset.
- Dettaglio ingrandito della motherboard con chip nelle sedi grafiche individuate. RAM/UFS su Pro03 e Lite05 restano separati dove le sedi non sono dimostrate; eMMC non forzata in UFS.
- Corretti i **9 abbinamenti di tipo RAM** segnalati nell'audit, selezionando `ram-12` LPDDR5X; i componenti presi da altre coppie hanno un asterisco. Non è una qualifica del package o del sistema.
- Per G99 selezionato `sto-64` della classe UFS2.2, anziché promettere una modalità UFS4.0. Dispositivo e circuito restano da qualificare.
- Nei render la RAM16 usa “bin da verificare” al posto di “9600 MHz”; il file sorgente del catalogo non è modificato da questo rendering.
- Tutti i **150 asset attivi / 147 SKU** restano visibili nella propria coppia, inclusi quelli relegati ad alternative/banco. Fold e UTG dedicato esclusi.

## Metodo e revisione

Riesaminati multimodalmente i cinque crop motherboard e quattro atlanti di cover, display, vetri e telai. Le sedi PCB derivano dai rettangoli del registro V17, ricontrollati visivamente. Le regioni cover sono stime normalizzate manuali. La disposizione periferica è una proposta basata sulla forma e sull'organizzazione tipica del dispositivo, non il risultato di una misurazione di connettori o piste.

Riesaminate le otto tavole di controllo comprendenti tutte le 29 composizioni, più le immagini individuali 07–08 v02 e 11–12 v09. Controllati automaticamente gli hash, i limiti del canvas, la copertura degli asset attivi e l'esclusione fold/UTG.

## Coordinate disponibili

`posizionamenti-v18.json` contiene per ogni immagine: selezione, cambi rispetto alla V17, riferimenti da altri SET, rettangolo pixel/rotazione/scala di ciascun asset posizionato, regione cover e note. Le coordinate locali dei piani usano il telefono nominale **74×158 mm** del catalogo come riferimento grafico, non come calibrazione fotografica o tolleranza di produzione.

Scala base 46 px/cm; chip adattati proporzionalmente alle sedi grafiche, batteria e moduli contenuti nei relativi inviluppi. Dettagli e inventari usano scale indipendenti. Nessun tratto disegnato è un routing elettrico; nessuna saldatura nascosta è verificata.

**Sono proposte di posizionamento visivo, non configurazioni collaudate.** Restano irrisolti package/ball map, interconnessioni e firmware, nonché allineamento preciso camera/cover, vetro/display, agganci, spessori e tolleranze. Le incompatibilità non vengono risolte deformando i componenti.
