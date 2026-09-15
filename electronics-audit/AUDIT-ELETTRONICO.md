# Audit elettronico preliminare dei SET

**16 settembre 2026 — esito: nessuna configurazione qualificata per la costruzione.**

Come richiesto nella scelta “Prima verifica i SET”, questa fase riguarda la verifica documentale, non nuove immagini di montaggi spacciati per collaudati. Le 29 immagini V17 rimangono illustrazioni storiche; **9 contengono già un conflitto tra generazione RAM e supporto documentato del SoC**. Le altre 20 non sono approvate per esclusione.

## Portata reale del lavoro

- Inventariate tutte le **149 voci** della lista `uploads/ls.ts`, con classificazione, documenti mancanti e riferimenti quando disponibili.
- **147 SKU attivi**, perché fold e UTG dedicato restano esclusi.
- Ricercate e confrontate **9 famiglie SoC** con fonti ufficiali; approfondimenti su memorie, assemblaggio BGA e USB PD.
- **Non** recuperati 149 datasheet, non svolta una qualifica completa di ogni codice. Le voci non ricercate individualmente sono esplicitamente marcate nel foglio.
- Esaminate le selezioni effettive delle **29 composizioni**: 9 conflitti RAM documentati, 5 sole coincidenze di tipo RAM, 15 core non valutati sufficientemente.
- **0 collaudi fisici, 0 configurazioni validate, 0 nuove immagini di assemblaggi.**

File di origine esaminati al commit `7628719efdb77f3bf52b30f8282554a1e3bc2a6f`. La lista originale è conservata, non riscritta. I nomi SKU interni non devono essere interpretati come MPN: per esempio `soc-8e` corrisponde nel catalogo a Snapdragon 8 Gen 3, non a 8 Elite.

## 1. Conflitti già riscontrati nelle immagini

Le conclusioni seguenti confrontano la **RAM selezionata nel manifest** con il tipo pubblicato dal produttore. Non sono risultati di prove al banco.

| Immagini | Abbinamento presente | Riscontro |
|---|---|---|
| 01–02 v01; 15–16 v01–v04 | Snapdragon 8 Elite + 4 GB LPDDR4X | Qualcomm documenta LPDDR5X: abbinamento da respingere nel progetto documentato. [3](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-8-Elite-Platform-Product-Brief.pdf) |
| 03–04 v02 | Snapdragon 8 Gen 3 + 6 GB LPDDR4X | Qualcomm documenta LPDDR5X: non una RAM intercambiabile tramite ridimensionamento grafico. [1](https://docs.qualcomm.com/doc/87-71408-1/87-71408-1_REV_G_Snapdragon_8_gen_3_Mobile_Platform_Product_Brief.pdf) |
| 11–12 v09 | Dimensity 8300 + 4 GB LPDDR4X | MediaTek documenta LPDDR5X fino a 8533 Mbps. [1](https://www.mediatek.com/products/tablets/mediatek-dimensity-8300) |
| 13–14 v01 e v04 | Exynos 2500 + 12 GB LPDDR4X | Samsung documenta LPDDR5X, con storage UFS 4.0. [1](https://semiconductor.samsung.com/processor/mobile-processor/exynos-2500/) |

**Non basta sostituire la RAM nelle immagini:** restano da verificare package, ball map, capacità supportata, numero di canali, rail, timing, routing, firmware e scheda reale.

## 2. Situazione per coppia

| Coppia | Esito preliminare / azione |
|---|---|
| 01–02 | Il solo core illustrato ha conflitto RAM. Ripartire da una BOM documentata; mainboard SBS-A7 non qualificata. |
| 03–04 | v02 respinta per RAM; v01 coincide solo nella famiglia LPDDR5X. Sedi e scheda Pro non qualificate. |
| 05–06 | Non approvata. Ricercata la famiglia 8300, senza estendere automaticamente la qualifica al suffisso Ultra. Exynos2400/LPDDR5 e relativi package richiedono approfondimento primario specifico. |
| 07–08 | Entrambe coincidono solo nel tipo LPDDR5X; nessuna qualifica di memoria specifica, velocità effettiva, storage o PCB. |
| 09–10 | Solo Dimensity9500 confrontato qui con specifica primaria; dati del catalogo da correggere. Le altre varianti restano non valutate sufficientemente. |
| 11–12 | v09 respinta per RAM; HelioG99 ha coincidenza di tipo RAM ma dubbio storage/modalità. Altre otto varianti senza confronto primario sufficiente in questa passata. |
| 13–14 | v01 e v04 respinte per RAM; Kirin9010 e TensorG4 richiedono fonti di integrazione specifiche. Le sole memorie LPDDR4X del gruppo non rendono tutti i SoC intercambiabili. |
| 15–16 | Tutte e quattro ereditano il core Elite/LPDDR4X incompatibile; i quattro gusci e i moduli camera non definiscono quattro progetti hardware. |

Per i cinque casi di sola coincidenza di tipo: 7+ Gen3/LPDDR5X, 8s Gen4/LPDDR5X, Dimensity9400/LPDDR5X, Dimensity9500/LPDDR5X e G99/LPDDR4X. Fonti rispettive: [1](https://docs.qualcomm.com/doc/87-73943-1/87-73943-1_REV_E_Snapdragon_7__Gen_3_Mobile_Platform_Product_Brief.pdf), [1](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Product-Brief-Snapdragon-8s-Gen-4.pdf), [3](https://www.mediatek.com/products/smartphones/mediatek-dimensity-9400), [1](https://www.mediatek.com/products/smartphones/mediatek-dimensity-9500), [1](https://www.mediatek.com/products/smartphones/mediatek-helio-g99).

“Tipo coincidente” **non significa** che un particolare chip di RAM sia saldabile o avviabile con quel SoC.

## 3. Errori del catalogo e rettifiche del mio lavoro

### Unità RAM: la correzione V17 non era una validazione

Avevo sostituito l'etichetta della RAM16 con “9600 MHz” per aderire al catalogo. Questo passaggio era **editoriale, non tecnicamente corretto come attestazione della velocità**. SK hynix pubblica 8533–9600 **Mbps** per la famiglia LPDDR5T/5X e distingue package PoP, MCP e discreti. Non ho identificato l'MPN preciso del modulo 16 GB del catalogo. Non trasformo quindi automaticamente quella voce in un componente certificato a 9600 Mbps. [2](https://product.skhynix.com/products/dram/lpddr.go?appTypCd=APX02&treeNo=1055)

Occorre separare clock in MHz e data rate, riportando la convenzione esatta della specifica. Il G99, ad esempio, è descritto con LPDDR4X fino a 2133 MHz e nella tabella con 4266 Mbps: non sono numeri intercambiabili mantenendo la stessa unità. [1](https://www.mediatek.com/products/smartphones/mediatek-helio-g99)

### Dimensity9500

La lista contiene “2 nm”, “Cortex-X930” e “Immortalis G930”. La pagina ufficiale riporta TSMC **N3P**, core **C1-Ultra / C1-Premium / C1-Pro**, GPU **Mali-G1 Ultra MC12**, LPDDR5X 10667 e UFS4.1 a quattro lane. I dati del catalogo non possono essere usati come distinta tecnica senza revisione. [1](https://www.mediatek.com/products/smartphones/mediatek-dimensity-9500)

### Dimensity8300: non tutte le scritte rimosse erano false

Nella V17 ho rimosso microtesto non verificato; la ricerca ora conferma per la famiglia 8300 Cortex-A715/A510 e Mali-G615. “Non verificato allora” non significa “errato”. La rimozione grafica non costituiva una correzione elettronica né provava il codice di package MT6880V. [1](https://www.mediatek.com/products/tablets/mediatek-dimensity-8300)

### HelioG99 e storage

MediaTek documenta **UFS2.2**, mentre v02 della coppia 11–12 seleziona `sto-1tb`, descritto UFS4.0. Non si può promettere funzionamento in modalità UFS4.0. Tuttavia, **la sola differenza di versione non basta per dichiarare impossibile qualsiasi funzionamento in modalità precedente**: serve il datasheet dell'esatto dispositivo, con alimentazioni, pinout e modalità supportate. [1](https://www.mediatek.com/products/smartphones/mediatek-helio-g99)

## 4. Blocco comune: le cinque motherboard

Nel repository non ho individuato file PCB/schematici KiCad, Gerber, BRD o STEP che consentano la verifica delle schede SBS-A7, SBS-X9 Pro, SBS-L3, SBS-G8 Game e SBS-RF mmWave. Sono disponibili illustrazioni, descrizioni e coordinate grafiche.

Le ricerche mirate per SBS-A7 e SBS-X9/SBS-G8 non hanno restituito documentazione tecnica pertinente. **Non è una prova che quei nomi non esistano; significa che non ho una scheda fisica documentata a cui ancorare il progetto.** Non è stata eseguita una ricerca esaustiva mondiale su ogni nome.

Rettangoli nominati “SoC/RAM/UFS” non specificano piste, pin, alimentazioni o compatibilità. La completezza del catalogo grafico non è completezza della BOM: “PMIC integrato” senza codice/schema non definisce tutti i componenti necessari al funzionamento.

## 5. Perché il millimetro e una bella immagine non bastano

Per i BGA servono land pattern specifici del package, diametri pad, solder mask, ball map, stencil e processo di rifusione. La guida TI mostra esempi di pitch inferiori al millimetro e distingue controlli elettrici e ispezioni X-ray. Questi esempi spiegano il metodo: **non forniscono le quote dei nostri SoC** e non vanno riutilizzati come loro footprint. [2](https://www.ti.com/lit/an/spraa99c/spraa99c.pdf)

Ridurre un chip al 90% di una piazzola visiva, come nel compositing V17, è un'operazione illustrativa: non verifica né il numero né la posizione dei contatti. Un'immagine non mostra continuità, cortocircuiti, avvio o affidabilità delle saldature nascoste.

Analogamente, la dicitura “USB-C PD3.1 140W” non qualifica tutto il telefono. La specifica USB PD3.1 introduce nuovi livelli di tensione e potenza; non è un certificato del singolo connettore, power path, caricatore o batteria del catalogo. [1](https://www.usb.org/sites/default/files/2021-05/USB%20PG%20USB%20PD%203.1%20DevUpdate%20Announcement_FINAL.pdf)

## 6. Documenti e prove necessari prima di nuove tavole tecniche

Per ogni configurazione candidata richiedere:

1. **Base identificata:** produttore/modello/revisione di una scheda reale, oppure progetto completo con BOM e MPN acquistabili.
2. **Interconnessione:** schema, netlist, stack-up, routing, ball map e land pattern corretti, XY di assemblaggio con origine/unità/rotazioni e tolleranze.
3. **Integrazione:** PMIC, sequenze e rail; clock/reset; memorie qualificate; firmware/BSP/boot; pinout e driver di display, touch, camere e radio.
4. **Meccanica:** CAD del telaio e moduli, quote e tolleranze, volumi, aperture, connettori/flex e dissipazione. Non tutti i moduli devono essere saldati direttamente alla motherboard.
5. **Batteria e alimentazione:** cella identificata, protezioni, NTC, limiti di carica/scarica, topologia e caricatore appropriati. Nessun collegamento basato sulla sola capacità o sulla potenza scritta sulla porta.
6. **Collaudo tracciabile:** piano con criteri di accettazione, unità/revisione testata, controlli di assemblaggio, assorbimenti e rail, boot, stress RAM/storage, periferiche, termica e RF quando applicabile; risultati effettivi del laboratorio.

Questa è una checklist di qualificazione, non un'istruzione di saldatura per i componenti attuali.

## Decisione

**Sospendere la generazione di immagini dichiarate “collaudate”.** Conservare i 29 PNG come concept, segnalare i conflitti nel manifest e nella galleria. Nessun file viene eliminato e nessun esito di prova viene inventato.

Nel workspace: `AUDIT-ELETTRONICO.md` e `AUDIT-ELETTRONICO.xlsx`. Nel repository: cartella `electronics-audit/`, CSV dei 149 SKU e delle 29 configurazioni, registro fonti ed esito sintetico. La prossima soglia utile non è “più immagini”, ma **una configurazione con motherboard e BOM realmente documentate**.
