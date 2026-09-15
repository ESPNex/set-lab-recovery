import type {
  BuildState,
  Category,
  DeviceInfo,
  OSConfig,
  PartDef,
  Profile,
  QualitySettings,
  SlotId,
  ToolId,
} from "./types";

/* =====================================================================
   PRECISE SLOT MAP — all coordinates in cm, phone is 7.4 x 15.8
   x = width, y = stack height (screen up), z = length (top of phone = -z)
   ===================================================================== */
export interface SlotDef {
  id: SlotId;
  name: string;
  pos: [number, number, number];
  size: [number, number, number];
  explode: number; // vertical lift in exploded view
  needsFrame: boolean;
  needsBoard?: boolean;
  optional?: boolean;
  desc: string;
}

export const SLOTS: Record<SlotId, SlotDef> = {
  frame: { id: "frame", name: "Telaio / Chassis", pos: [0, 0.12, 0], size: [7.40, 0.90, 15.80], explode: 0, needsFrame: false, desc: "La struttura portante: senza telaio non si monta nulla." },
  soc: { id: "soc", name: "SoC (processore)", pos: [1.18, 0.285, -4.62], size: [1.28, 0.10, 1.28], explode: 1.7, needsFrame: true, needsBoard: true, desc: "Il cervello. Va saldato sull'area BGA della scheda madre." },
  ram: { id: "ram", name: "Modulo RAM", pos: [-1.42, 0.275, -5.48], size: [1.22, 0.08, 1.48], explode: 1.9, needsFrame: true, needsBoard: true, desc: "Memoria volatile LPDDR. Più è veloce, più app restano aperte." },
  storage: { id: "storage", name: "Memoria UFS", pos: [-1.42, 0.275, -2.52], size: [1.22, 0.08, 1.52], explode: 2.1, needsFrame: true, needsBoard: true, desc: "Archiviazione flash UFS. Serve per installare il sistema operativo." },
  motherboard: { id: "motherboard", name: "Scheda madre", pos: [0.05, 0.145, -3.35], size: [6.55, 0.14, 7.10], explode: 1.25, needsFrame: true, desc: "Il PCB principale. Fissata con 4 viti Phillips M1.6." },
  thermal: { id: "thermal", name: "Sistema termico", pos: [0.2, 0.0, -3.5], size: [5.6, 0.07, 4.8], explode: 0.7, needsFrame: true, desc: "Vapor chamber o grafite, sotto la scheda madre." },
  battery: { id: "battery", name: "Batteria", pos: [0, -0.02, 3.5], size: [6.4, 0.44, 6.8], explode: 0.85, needsFrame: true, desc: "Cella Li-Po: si posa nella vasca inferiore e aderisce con le linguette arancioni (per toglierla: plettro)." },
  display: { id: "display", name: "Pannello display", pos: [0, 0.46, 0], size: [7.05, 0.12, 15.2], explode: 2.75, needsFrame: true, desc: "OLED/LCD incollato al telaio: serve colla B-7000." },
  glass: { id: "glass", name: "Vetro protettivo", pos: [0, 0.56, 0], size: [7.15, 0.06, 15.4], explode: 3.35, needsFrame: true, desc: "Il vetro sopra il pannello. Si aggancia a pressione sul telaio." },
  backcover: { id: "backcover", name: "Cover posteriore", pos: [0, -0.36, 0], size: [7.4, 0.12, 15.8], explode: -1.2, needsFrame: true, desc: "Scocca posteriore a tutta superficie, incollata: colla + plettro." },
  cameraRear: { id: "cameraRear", name: "Fotocamera posteriore", pos: [-2.0, -0.55, -5.7], size: [2.6, 0.38, 2.8], explode: -1.8, needsFrame: true, desc: "Modulo fotocamere, sporge dalla cover." },
  cameraFront: { id: "cameraFront", name: "Fotocamera frontale", pos: [0, 0.26, -6.85], size: [0.62, 0.08, 0.62], explode: 2.35, needsFrame: true, desc: "Sotto il punch-hole in alto al centro del display." },
  speaker: { id: "speaker", name: "Altoparlante", pos: [1.7, -0.23, 7.05], size: [2.4, 0.34, 1.0], explode: -0.45, needsFrame: true, optional: true, desc: "Speaker principale sul bordo inferiore." },
  usb: { id: "usb", name: "Porta USB-C", pos: [0, -0.23, 7.2], size: [2.2, 0.3, 0.9], explode: -0.55, needsFrame: true, optional: true, desc: "Connettore di ricarica su flex." },
  mic: { id: "mic", name: "Microfono", pos: [-1.7, -0.23, 7.05], size: [0.7, 0.28, 0.7], explode: -0.5, needsFrame: true, optional: true, desc: "Microfono principale per chiamate." },
  haptics: { id: "haptics", name: "Motore aptico", pos: [2.5, -0.23, 5.5], size: [1.3, 0.3, 0.8], explode: -0.4, needsFrame: true, optional: true, desc: "Vibrazione: ERM economico o asse X preciso." },
  antenna: { id: "antenna", name: "Flex antenna", pos: [0, 0.3, -7.0], size: [6.6, 0.05, 0.9], explode: 1.5, needsFrame: true, optional: true, desc: "Flex Wi-Fi/5G lungo il bordo superiore." },
  sim: { id: "sim", name: "Carrello SIM", pos: [-3.5, 0.18, -2.5], size: [0.55, 0.12, 2.2], explode: 1.1, needsFrame: true, optional: true, desc: "Slot nano-SIM sul fianco sinistro." },
};

export const SLOT_LIST = Object.values(SLOTS);

/* ------------------------------ screws ------------------------------ */
export interface ScrewDef {
  id: string;
  pos: [number, number, number];
  group: "board" | "sub";
}
export const SCREWS: ScrewDef[] = [
  { id: "s1", pos: [3.1, 0.27, -6.3], group: "board" },
  { id: "s2", pos: [-2.5, 0.27, -6.3], group: "board" },
  { id: "s3", pos: [3.1, 0.27, -0.35], group: "board" },
  { id: "s4", pos: [-2.5, 0.27, -0.35], group: "board" },
  { id: "s5", pos: [1.5, -0.06, 6.9], group: "sub" },
  { id: "s6", pos: [-1.5, -0.06, 6.9], group: "sub" },
];

export const GLUE_ZONES = ["display", "backcover", "battery"] as const;

/* =====================================================================
   PARTS CATALOG
   ===================================================================== */
const p = (
  id: string,
  name: string,
  brand: string,
  category: Category,
  slot: SlotId,
  score: number,
  desc: string,
  opts: Partial<PartDef> = {}
): PartDef => ({ id, name, brand, category, slot, stats: { score }, desc, ...opts });

export const PARTS: PartDef[] = [
  /* ---- telai ---- */
  p("frame-alu", "Telaio Alluminio 6013", "Vertex", "telaio", "frame", 70, "Monoscocca in alluminio serie 6000, fresata CNC.", { specs: ["Alluminio 6013", "168 g", "Finitura sabbiata"], svg: { kind: "plate", base: "#8f98a5", accent: "#c8d0da", label: "VERTEX AL-6013", pattern: "stripes" } }),
  p("frame-ti", "Telaio Titanio Grado 5", "AeroForge", "telaio", "frame", 92, "Titanio aerospaziale: leggero, rigido, premium.", { specs: ["Ti-6Al-4V", "149 g", "Spazzolato"], svg: { kind: "plate", base: "#6d7480", accent: "#aab3c0", label: "TI-6Al-4V", pattern: "stripes" } }),
  p("frame-poly", "Telaio Policarbonato", "EcoLine", "telaio", "frame", 48, "Economico e resistente alle cadute, ma flette.", { specs: ["PC riciclato", "182 g"], svg: { kind: "plate", base: "#3c4450", accent: "#5a6572", label: "ECO-PC", pattern: "none" } }),
  p("frame-mag", "Telaio Qi2 magnetico", "Vertex", "telaio", "frame", 76, "Anello magnetico Qi2 integrato nel telaio.", { specs: ["Al 6013", "magneti N52"] }),

  /* ---- SoC (marche e modelli reali) ---- */
  p("soc-x90", "Snapdragon 8 Elite", "Qualcomm", "processori", "soc", 96, "Oryon 2ª gen, 3 nm, GPU Adreno 830 con RayTracing.", { specs: ["3 nm", "4.32 GHz", "NPU 100 TOPS"] }),
  p("soc-8e", "Snapdragon 8 Gen 3", "Qualcomm", "processori", "soc", 88, "Il flagship della scorsa generazione, ancora validissimo.", { specs: ["4 nm", "3.3 GHz", "Adreno 750"] }),
  p("soc-vertv2", "Exynos 2400", "Samsung", "processori", "soc", 80, "Core ARM v9 e GPU Xclipse: il ritorno di Samsung.", { specs: ["4 nm", "3.2 GHz", "RDNA3"] }),
  p("soc-7g2", "Snapdragon 7+ Gen 3", "Qualcomm", "processori", "soc", 74, "Fascia alta accessibile, molto efficiente.", { specs: ["4 nm", "2.8 GHz"] }),
  p("soc-q6", "Dimensity 8300-Ultra", "MediaTek", "processori", "soc", 66, "Media gamma aggressivo con AI generativa on-device.", { specs: ["4 nm", "3.35 GHz"] }),
  p("soc-g99", "Helio G99", "MediaTek", "processori", "soc", 44, "Il re dei 200 €: onesto, niente 5G.", { specs: ["6 nm", "2.2 GHz"] }),
  p("soc-helio", "Unisoc T7250", "Unisoc", "processori", "soc", 38, "Per smartphone da 129 €: fa il suo dovere.", { specs: ["12 nm", "1.8 GHz"] }),
  p("soc-8e2", "Snapdragon 8 Elite Gen 5", "Qualcomm", "processori", "soc", 98, "Oryon 3ª gen, 3 nm, NPU da 120 TOPS: il tetto delle prestazioni.", { specs: ["3 nm", "4.6 GHz", "Adreno 840"] }),
  p("soc-tensor", "Tensor G5", "Google", "processori", "soc", 78, "TPU on-device e fotocamere computational.", { specs: ["3 nm", "TPU v6"] }),
  p("soc-d9400", "Dimensity 9400", "MediaTek", "processori", "soc", 90, "All-big cores e ray tracing mobile.", { specs: ["3 nm", "3.6 GHz"] }),
  p("soc-dim95", "Dimensity 9500", "MediaTek", "processori", "soc", 95, "Cortex-X930 a 4.2 GHz, GPU Immortalis G930: flagship MediaTek 2026.", { specs: ["2 nm", "4.2 GHz", "Immortalis"] }),

  /* ---- RAM ---- */
  p("ram-4", "4 GB LPDDR4X", "Micron", "memorie", "ram", 38, "Minimo sindacale nel 2026.", { specs: ["4266 MHz"] }),
  p("ram-6", "6 GB LPDDR4X", "Samsung", "memorie", "ram", 52, "Compromesso onesto.", { specs: ["4266 MHz"] }),
  p("ram-8", "8 GB LPDDR5", "SK Hynix", "memorie", "ram", 68, "Lo standard attuale.", { specs: ["6400 MHz"] }),
  p("ram-12", "12 GB LPDDR5X", "Samsung", "memorie", "ram", 84, "Multitasking senza pensieri.", { specs: ["8533 MHz"] }),
  p("ram-16", "16 GB LPDDR5X", "SK Hynix", "memorie", "ram", 95, "Per chi tiene 80 app aperte.", { specs: ["9600 MHz"] }),
  p("ram-24", "24 GB LPDDR5X", "Samsung", "memorie", "ram", 98, "Più RAM di un ultrabook 2022.", { specs: ["10667 MHz"] }),

  /* ---- storage ---- */
  p("sto-64", "64 GB UFS 2.2", "Micron", "memorie", "storage", 30, "Si riempie subito, lento nei trasferimenti.", { specs: ["~500 MB/s"] }),
  p("sto-128", "128 GB UFS 3.1", "Samsung", "memorie", "storage", 55, "Taglio base sensato.", { specs: ["~1.2 GB/s"] }),
  p("sto-256", "256 GB UFS 3.1", "Kioxia", "memorie", "storage", 66, "Il punto giusto.", { specs: ["~1.9 GB/s"] }),
  p("sto-512", "512 GB UFS 4.0", "Samsung", "memorie", "storage", 82, "Spazio e velocità.", { specs: ["~3.5 GB/s"] }),
  p("sto-1tb", "1 TB UFS 4.0", "Samsung", "memorie", "storage", 92, "Non cancellerai mai più nulla.", { specs: ["~4.2 GB/s"] }),

  /* ---- scheda madre ---- */
  p("board-std", "Mainboard SBS-A7", "SBS Parts", "schede", "motherboard", 62, "PCB 8 strati con PMIC e ricetrasmettitore.", { specs: ["8-layer PCB", "PMIC integrato"] }),
  p("board-pro", "Mainboard SBS-X9 Pro", "SBS Parts", "schede", "motherboard", 88, "PCB 12 strati, alimentazione a 3 fasi, shielding extra.", { specs: ["12-layer PCB", "Fase tripla"] }),

  /* ---- termico ---- */
  p("th-gra", "Foglio di grafite", "CoolCo", "raffreddamento", "thermal", 45, "Semplice, sottile, passivo.", { specs: ["Spessore 0.3 mm"] }),
  p("th-vc", "Vapor chamber", "CoolCo", "raffreddamento", "thermal", 78, "Camera di vapore in rame: cala di 6°C sotto stress.", { specs: ["Cu 2200 mm²"] }),
  p("th-gra-vc", "Grafene + VC", "CoolCo", "raffreddamento", "thermal", 94, "Il meglio: grafene sopra la vapor chamber.", { specs: ["Grafene 1400 W/mK"] }),

  /* ---- batterie ---- */
  p("bat-3000", "Cella 3000 mAh", "ATL", "batterie", "battery", 40, "Sopravvive al pranzo.", { specs: ["3.87 V", "11.6 Wh"] }),
  p("bat-4500", "Cella 4500 mAh", "ATL", "batterie", "battery", 62, "Giornata piena serena.", { specs: ["3.87 V", "17.4 Wh"] }),
  p("bat-5000", "Cella 5000 mAh", "BYD", "batterie", "battery", 72, "Il classico moderno.", { specs: ["3.87 V", "19.4 Wh"] }),
  p("bat-6000", "Cella 6000 mAh Si/C", "ATL", "batterie", "battery", 82, "Silicio-carbonio: due giorni reali.", { specs: ["3.92 V", "23.5 Wh"] }),
  p("bat-7000", "Cella 7000 mAh Si/C", "BYD", "batterie", "battery", 90, "Tre giorni se non filmi in 8K.", { specs: ["3.95 V", "27.6 Wh"] }),
  p("bat-dual", "Doppia cella 5500 mAh", "ATL", "batterie", "battery", 86, "Due pouch in parallelo: picchi di scarica più alti.", { specs: ["3.87 V", "21.3 Wh"] }),

  /* ---- display ---- */
  p("disp-lcd", 'LCD IPS 6.1" 60Hz', "BOE", "display", "display", 40, "Onesto, ma notch grosso e 60 Hz.", { specs: ["720x1560", "Notch a goccia"], stats: { score: 40, extra: { cut: "notch", hz: 60 } } }),
  p("disp-oled", 'OLED 6.4" 90Hz', "Samsung Display", "display", "display", 62, "Neri veri e punch-hole.", { specs: ["1080x2340", "Punch-hole"], stats: { score: 62, extra: { cut: "punch", hz: 90 } } }),
  p("disp-am", 'AMOLED LTPO 6.7" 120Hz', "Samsung Display", "display", "display", 82, "LTPO adattivo, 1800 nit.", { specs: ["1220x2712", "Punch-hole"], stats: { score: 82, extra: { cut: "punch", hz: 120 } } }),
  p("disp-2k", 'AMOLED 2K 6.9" 144Hz', "Samsung Display", "display", "display", 94, "Esagerato: 2K, 144 Hz, 3000 nit.", { specs: ["1440x3200", "Punch-hole"], stats: { score: 94, extra: { cut: "punch", hz: 144 } } }),

  /* ---- vetro ---- */
  p("glass-gg5", "Gorilla Glass 5", "Corning", "vetro", "glass", 55, "Protezione base, si graffia col tempo.", { specs: ["Cadute 1.6 m"] }),
  p("glass-dt", "Dragontrail Star 2", "AGC", "vetro", "glass", 62, "Buon compromesso giapponese.", { specs: ["Cadute 2 m"] }),
  p("glass-victus3", "Gorilla Glass Victus 2", "Corning", "vetro", "glass", 88, "Sopravvive all'asfalto da 2 m.", { specs: ["Cadute 2 m"] }),
  p("glass-zaf", "Zaffiro sintetico", "CrystalLux", "vetro", "glass", 95, "Praticamente inattaccabile. Costoso.", { specs: ["9 Mohs"] }),

  /* ---- cover posteriori ---- */
  p("back-glossy", "Cover vetro lucido", "LuxGuard", "telaio", "backcover", 70, "Vetro temperato glossy: impronte a volontà.", { specs: ["Vetro 0.6 mm"] }),
  p("back-matte", "Cover vetro satinato", "LuxGuard", "telaio", "backcover", 74, "Satinata anti-impronta, grip migliore.", { specs: ["AG etching"] }),
  p("back-cer", "Cover in ceramica", "LuxGuard", "telaio", "backcover", 88, "Zirconia: fredda al tatto, eterna.", { specs: ["ZrO₂ sinterizzata"] }),
  p("back-alu", "Cover alluminio", "Vertex", "telaio", "backcover", 64, "Unibody metallico, disperde bene il calore.", { specs: ["Alluminio 6013"] }),
  p("back-leather", "Cover pelle vegana", "EcoLine", "telaio", "backcover", 58, "Morbida, calda, zero scivolamenti.", { specs: ["PU bio-based"] }),

  /* ---- fotocamere ---- */
  p("cam-dual", "Dual 12 MP · IMX363", "Sony", "fotocamere", "cameraRear", 45, "Due fotocamere pulite, niente zoom.", { specs: ["12+8 MP", "EIS"] }),
  p("cam-triple", "Triple 50 MP OIS · IMX906", "Sony", "fotocamere", "cameraRear", 76, "Principale 50 MP stabilizzata + ultrawide + tele 2x.", { specs: ["50+12+10 MP", "OIS"] }),
  p("cam-quad", "Quad 200 MP · ISOCELL HP2", "Samsung", "fotocamere", "cameraRear", 95, "200 MP, periscopio 5x, notte stellare.", { specs: ["200 MP", "Periscopio 5x"] }),
  p("camf-8", "Frontale 8 MP · IMX355", "Sony", "fotocamere", "cameraFront", 40, "Videochiamate dignitose.", { }),
  p("camf-32", "Frontale 32 MP AF · IMX615", "Sony", "fotocamere", "cameraFront", 72, "Autofocus e 4K frontale.", { }),

  /* ---- audio ---- */
  p("spk-mono", "Speaker mono bottom", "AAC Technologies", "audio", "speaker", 40, "Un solo speaker: si tappa con un dito.", { specs: ["0.8 W"] }),
  p("spk-stereo", "Stereo con capsula", "AAC Technologies", "audio", "speaker", 70, "Capsula auricolare come secondo canale.", { specs: ["2x 1 W"] }),
  p("spk-dolby", "Stereo simmetrico + Atmos", "AAC Technologies", "audio", "speaker", 90, "Due casse vere, scena larga, Dolby Atmos.", { specs: ["2x 1.2 W", "Atmos"] }),

  /* ---- porte ---- */
  p("usb-20", "USB-C 2.0", "Amphenol", "porte", "usb", 45, "Solo ricarica e dati lenti.", { specs: ["480 Mbps"] }),
  p("usb-32", "USB-C 3.2 Gen 2", "Amphenol", "porte", "usb", 72, "Trasferimenti seri e video out.", { specs: ["10 Gbps", "DP Alt"] }),
  p("usb-40", "USB4 40 Gbps", "Amphenol", "porte", "usb", 90, "Il top: 40 Gbps, docking completa.", { specs: ["40 Gbps"] }),

  /* ---- moduli ---- */
  p("ant-wifi5", "Flex Wi-Fi 5 / 4G", "Qorvo", "moduli", "antenna", 50, "Connettività essenziale.", { }),
  p("ant-wifi7", "Flex Wi-Fi 7 / 5G mmWave", "Qorvo", "moduli", "antenna", 90, "Latenza minima e banda enorme.", { }),
  p("hap-erm", "Motorino ERM", "Leaderdrive", "moduli", "haptics", 40, "Vibrazione 'zanzara'.", { }),
  p("hap-x", "Motore lineare asse X", "Leaderdrive", "moduli", "haptics", 86, "Tic precisi, feedback da flagship.", { }),
  p("mic-1", "MEMS singolo", "Knowles", "moduli", "mic", 45, "Un microfono, tanti rumori.", { }),
  p("mic-3", "Array 3 MEMS", "Knowles", "moduli", "mic", 82, "Cancellazione rumore in chiamata.", { }),
  p("sim-nano", "Carrello nano-SIM", "Luxshare", "moduli", "sim", 50, "Slot fisico classico.", { }),
  p("sim-esim", "Modulo eSIM + nano", "Luxshare", "moduli", "sim", 85, "Doppia eSIM oltre alla nano.", { }),

  /* ---- gamma extra 2026 (10 nuovi SKU) ---- */
  p("frame-classic", "Telaio Classico 2016", "RetroWorks", "telaio", "frame", 52, "Vecchia scuola: bezel marcati, schermo 4:3 e tasto home fisico nel mento.", { specs: ["16:9", "home fisico", "AL 6063"] }),
  p("soc-exy26", "Exynos 2600", "Samsung", "processori", "soc", 89, "2 nm GAA, GPU Xclipse 960 con ray tracing di seconda generazione.", { specs: ["2 nm", "3.8 GHz"] }),
  p("soc-ten6", "Tensor G6", "Google", "processori", "soc", 81, "TPU dedicata per Gemini on-device e fotocamere computazionali.", { specs: ["3 nm", "TPU v7"] }),
  p("ram-18", "18 GB LPDDR5X", "SK Hynix", "memorie", "ram", 96, "Taglio raro: multitasking da workstation in tasca.", { specs: ["9600 MHz"] }),
  p("sto-1tb41", "1 TB UFS 4.1", "Kioxia", "memorie", "storage", 94, "UFS 4.1 con scrittura sequenziale a 4.8 GB/s.", { specs: ["~4.8 GB/s"] }),
  p("cam-peri2", "Periscopio 6x 200 MP", "Sony", "fotocamere", "cameraRear", 96, "Prisma 6x con OIS gimbal e sensore da 1/1.3\".", { specs: ["200 MP", "6x ottico"] }),
  p("camf-50b", "Frontale 50 MP AF OIS", "Samsung", "fotocamere", "cameraFront", 84, "Selfie stabilizzati e video 4K60 frontale.", { specs: ["50 MP", "OIS"] }),
  p("spk-dual", "Stereo dual driver 1.4 W", "Goertek", "audio", "speaker", 92, "Due driver simmetrici con camera di risonanza.", { specs: ["2x 1.4 W", "Atmos"] }),
  p("usb-40b", "USB4 40 Gbps flex", "Amphenol", "porte", "usb", 91, "40 Gbps, DP 2.1 e ricarica 140 W sullo stesso flex.", { specs: ["40 Gbps", "140 W"] }),
  p("hap-xl", "LRA X-axis premium", "Leaderdrive", "moduli", "haptics", 94, "Il motore aptico più grande della categoria: feedback da console.", { specs: ["X-axis", "wideband"] }),

  /* ---- consumabili ---- */
  p("cons-screws", "Viti Phillips M1.6 (set)", "SBS Parts", "consumabili", "frame", 50, "Set di viti di ricambio, sempre nel banco.", {}),
  p("cons-glue", "Colla B-7000 15 ml", "SBS Parts", "consumabili", "frame", 50, "La colla specifica per smartphone: flessibile, rimovibile.", {}),
  p("cons-tabs", "Linguette adesive batteria", "SBS Parts", "consumabili", "frame", 50, "Adesivo pretagliato per celle Li-Po.", {}),

  /* ---- extra gamma 2026 ---- */
  p("sto-2tb", "2 TB UFS 4.1", "Samsung", "memorie", "storage", 96, "Due tera in tasca. Per chi filma in 8K.", { specs: ["~4.8 GB/s"] }),
  p("disp-oled63", 'OLED 6.3" 120Hz Flat', "BOE", "display", "display", 72, "Pannello flat senza curve: meno tocchi fantasma.", { stats: { score: 72, extra: { cut: "punch", hz: 120 } }, specs: ["1080x2400", "Punch-hole"] }),
  p("back-blue", "Cover vetro Blu Abisso", "LuxGuard", "telaio", "backcover", 71, "Blu profondo semilucido, elegante in ogni tasca.", { specs: ["AG satinato"] }),
  p("back-green", "Cover vetro Verde Salvia", "LuxGuard", "telaio", "backcover", 69, "Verde salvia opaco: il colore dell'anno.", { specs: ["AG satinato"] }),

  /* ---- shop PCBS-style: tante SKU per categoria ---- */
  p("frame-ss", "Telaio acciaio inox 316L", "AeroForge", "telaio", "frame", 84, "Acciaio chirurgico, pesante ma indeformabile.", { specs: ["316L", "198 g"] }),
  p("frame-mg", "Telaio magnesio", "Vertex", "telaio", "frame", 80, "Più leggero dell'alluminio, smorza le vibrazioni.", { specs: ["AZ91D", "138 g"] }),
  p("frame-flat", "Telaio flat-edge 2026", "Vertex", "telaio", "frame", 73, "Bordi piatti da flagship, grip in vetro laterale.", { specs: ["Al 6013", "flat"] }),
  p("soc-8s", "Snapdragon 8s Gen 4", "Qualcomm", "processori", "soc", 82, "Fascia alta senza il prezzo Elite.", { specs: ["4 nm", "3.2 GHz"] }),
  p("soc-8g2", "Snapdragon 8 Gen 2", "Qualcomm", "processori", "soc", 76, "Ancora ottimo nel 2026 se raffreddato.", { specs: ["4 nm", "3.2 GHz"] }),
  p("soc-7g3", "Snapdragon 7 Gen 3", "Qualcomm", "processori", "soc", 60, "Media gamma 5G efficiente.", { specs: ["4 nm"] }),
  p("soc-6g1", "Snapdragon 6 Gen 1", "Qualcomm", "processori", "soc", 50, "Entry 5G per listini sotto i 250 €.", { specs: ["4 nm"] }),
  p("soc-d9300", "Dimensity 9300+", "MediaTek", "processori", "soc", 86, "All-big cores, ottimo in gaming.", { specs: ["4 nm", "3.4 GHz"] }),
  p("soc-d8300", "Dimensity 8300", "MediaTek", "processori", "soc", 64, "Gaming mid-range aggressivo.", { specs: ["4 nm"] }),
  p("soc-d7300", "Dimensity 7300", "MediaTek", "processori", "soc", 54, "5G e fotocamere 200 MP entry.", { specs: ["4 nm"] }),
  p("soc-ex2500", "Exynos 2500", "Samsung", "processori", "soc", 84, "3 nm Samsung Foundry, GPU Xclipse 950.", { specs: ["3 nm"] }),
  p("soc-tensor4", "Tensor G4", "Google", "processori", "soc", 72, "AI photo stack, modem 5G Samsung.", { specs: ["4 nm"] }),
  p("soc-kirin", "Kirin 9010", "HiSilicon", "processori", "soc", 70, "NPU Da Vinci, 5G proprietario.", { specs: ["7 nm"] }),
  p("ram-8x", "8 GB LPDDR5X", "Micron", "memorie", "ram", 74, "Velocità da flagship in taglio 8 GB.", { specs: ["8533 MHz"] }),
  p("ram-12lp4", "12 GB LPDDR4X", "Micron", "memorie", "ram", 70, "Tanta capacità, bus più lento.", { specs: ["4266 MHz"] }),
  p("ram-32", "32 GB LPDDR5X", "SK Hynix", "memorie", "ram", 99, "Workstation in tasca.", { specs: ["10667 MHz"] }),
  p("sto-32", "32 GB eMMC 5.1", "Micron", "memorie", "storage", 18, "Lento e piccolo: solo per prototipi.", { specs: ["~250 MB/s"] }),
  p("sto-256u4", "256 GB UFS 4.0", "Kioxia", "memorie", "storage", 78, "UFS 4.0 nel taglio più venduto.", { specs: ["~3.5 GB/s"] }),
  p("sto-512u31", "512 GB UFS 3.1", "Micron", "memorie", "storage", 70, "Capacità alta, bus generazione precedente.", { specs: ["~1.9 GB/s"] }),
  p("board-lite", "Mainboard SBS-L3", "SBS Parts", "schede", "motherboard", 48, "6 strati, PMIC singolo: per entry-level.", { specs: ["6-layer"] }),
  p("board-rf", "Mainboard SBS-RF mmWave", "SBS Parts", "schede", "motherboard", 92, "Shielding 5G mmWave e antenne on-board.", { specs: ["12-layer", "mmWave"] }),
  p("board-game", "Mainboard SBS-G8 Game", "SBS Parts", "schede", "motherboard", 80, "VRM rinforzato per SoC in turbo continuo.", { specs: ["10-layer"] }),
  p("th-cu", "Heatpipe rame 0.4 mm", "CoolCo", "raffreddamento", "thermal", 58, "Heatpipe piatta sotto il SoC.", { specs: ["Cu"] }),
  p("th-gr2", "Doppia grafite", "CoolCo", "raffreddamento", "thermal", 52, "Due fogli impilati, costo basso.", { specs: ["0.2+0.2 mm"] }),
  p("th-coil", "VC + bobina Qi2", "CoolCo", "raffreddamento", "thermal", 88, "Vapor chamber forata per ricarica wireless magnetica.", { specs: ["Qi2 15 W"] }),
  p("bat-3500", "Cella 3500 mAh", "BYD", "batterie", "battery", 48, "Compatta per telai sottili.", { specs: ["3.85 V"] }),
  p("bat-4000", "Cella 4000 mAh", "ATL", "batterie", "battery", 56, "Equilibrio spessore/autonomia.", { specs: ["3.87 V"] }),
  p("bat-5500", "Cella 5500 mAh Si/C", "ATL", "batterie", "battery", 78, "Silicio-carbonio nel taglio medio.", { specs: ["3.90 V"] }),
  p("bat-8000", "Cella 8000 mAh stacked", "BYD", "batterie", "battery", 94, "Due pouch stacked: brick ma tre giorni.", { specs: ["3.95 V"] }),
  p("bat-stacked", "Cella stacked 6800 mAh Si/C", "ATL", "batterie", "battery", 88, "Doppia pouch silicio-carbonio impilata: densità record in 7.4 mm.", { specs: ["3.94 V", "26.5 Wh", "80 W"] }),
  p("disp-lcd67", 'LCD IPS 6.7" 90Hz', "BOE", "display", "display", 48, "Grande e economico, neri grigi.", { specs: ["1080x2400"], stats: { score: 48, extra: { cut: "notch", hz: 90 } } }),
  p("disp-oled61", 'OLED 6.1" 120Hz', "LG Display", "display", "display", 76, "Compatto LTPO, 1-120 Hz.", { specs: ["1179x2556"], stats: { score: 76, extra: { cut: "punch", hz: 120 } } }),
  p("disp-fold", 'OLED pieghevole 7.6"', "Samsung Display", "display", "display", 90, "Pannello pieghevole UTG (montaggio su telaio rigido: solo test).", { specs: ["1812x2176"], stats: { score: 90, extra: { cut: "punch", hz: 120 } } }),
  p("disp-eco", 'TFT 6.5" 60Hz', "Tianma", "display", "display", 28, "Il più economico: colori spenti.", { specs: ["720x1600"], stats: { score: 28, extra: { cut: "notch", hz: 60 } } }),
  p("glass-gg3", "Gorilla Glass 3", "Corning", "vetro", "glass", 40, "Vecchia generazione, si graffia subito.", { specs: ["1.2 m"] }),
  p("glass-gg7", "Gorilla Glass 7i", "Corning", "vetro", "glass", 70, "Fascia media 2025-26.", { specs: ["1.8 m"] }),
  p("glass-armor", "Gorilla Armor 2", "Corning", "vetro", "glass", 96, "Anti-riflesso e durezza da asfalto.", { specs: ["2 m", "AR"] }),
  p("glass-utg", "Ultra Thin Glass", "Schott", "vetro", "glass", 80, "Vetro pieghevole 30 µm.", { specs: ["UTG"] }),
  p("back-red", "Cover vetro Rosso lava", "LuxGuard", "telaio", "backcover", 70, "Rosso saturo lucido.", { specs: ["gloss"] }),
  p("back-black", "Cover vetro Nero piano", "LuxGuard", "telaio", "backcover", 72, "Nero assorbente, zero riflessi.", { specs: ["AG"] }),
  p("back-white", "Cover vetro Bianco perla", "LuxGuard", "telaio", "backcover", 68, "Bianco ottico con bordo oro.", { specs: ["pearl"] }),
  p("back-carbon", "Cover fibra di carbonio", "AeroForge", "telaio", "backcover", 82, "Twille 3K, leggerissima.", { specs: ["3K twill"] }),
  p("back-wood", "Cover legno noce", "EcoLine", "telaio", "backcover", 55, "Impiallacciatura naturale, unica.", { specs: ["noce"] }),
  p("cam-uw", "Dual 50+50 MP UW", "Sony", "fotocamere", "cameraRear", 68, "Principale + ultrawide stesso sensore.", { specs: ["50+50", "OIS"] }),
  p("cam-peri10", "Periscopio 10x 64 MP", "Sony", "fotocamere", "cameraRear", 92, "Prisma 10x ottico, OIS gimbal.", { specs: ["64 MP", "10x"] }),
  p("cam-1inch", "Sensore 1\" 50 MP", "Sony", "fotocamere", "cameraRear", 90, "IMX989 class: foto da compact.", { specs: ["1-inch", "OIS"] }),
  p("camf-12", "Frontale 12 MP", "Sony", "fotocamere", "cameraFront", 52, "Selfie puliti, no AF.", { specs: ["12 MP"] }),
  p("camf-50", "Frontale 50 MP AF", "Samsung", "fotocamere", "cameraFront", 80, "Autofocus e ritratto 2x crop.", { specs: ["50 MP AF"] }),
  p("spk-stereo-bot", "Stereo bottom dual", "Goertek", "audio", "speaker", 78, "Due driver sul bordo inferiore.", { specs: ["2x 1.1 W"] }),
  p("spk-hires", "Speaker Hi-Res 192 kHz", "AAC Technologies", "audio", "speaker", 88, "Certificazione Hi-Res Audio.", { specs: ["192 kHz"] }),
  p("usb-pd", "USB-C PD 3.1 140W", "Amphenol", "porte", "usb", 80, "Ricarica notebook-class.", { specs: ["140 W", "USB 2.0"] }),
  p("usb-dp", "USB-C DP 2.1 8K", "Amphenol", "porte", "usb", 86, "Video 8K60 su monitor esterno.", { specs: ["DP 2.1"] }),
  p("ant-wifi6e", "Flex Wi-Fi 6E / 5G sub-6", "Broadcom", "moduli", "antenna", 70, "6 GHz indoor, niente mmWave.", { specs: ["6E"] }),
  p("ant-uwb", "Flex UWB + NFC", "NXP", "moduli", "antenna", 78, "Chiavi digitali e pagamenti.", { specs: ["UWB", "NFC"] }),
  p("hap-z", "Motore lineare asse Z", "Nidec", "moduli", "haptics", 70, "Tap verticali, più economico dell'asse X.", { specs: ["Z-axis"] }),
  p("hap-dual", "Doppio LRA stereo", "Leaderdrive", "moduli", "haptics", 92, "Due motori: haptic stereo.", { specs: ["2x LRA"] }),
  p("mic-4", "Array 4 MEMS beamforming", "Knowles", "moduli", "mic", 90, "Studio vocale in tasca.", { specs: ["4 MEMS"] }),
  p("sim-dual", "Carrello dual nano-SIM", "Luxshare", "moduli", "sim", 62, "Due nano, niente microSD.", { specs: ["dual"] }),
  p("sim-hybrid", "Carrello ibrido SIM/SD", "Luxshare", "moduli", "sim", 58, "O seconda SIM o microSD.", { specs: ["hybrid"] }),
  p("cons-thermalp", "Pad termico 1 mm (set)", "SBS Parts", "consumabili", "frame", 50, "Pad per SoC e UFS.", {}),
  p("cons-kapton", "Nastro Kapton 10 mm", "SBS Parts", "consumabili", "frame", 50, "Isolamento flex e batterie.", {}),
  p("cons-ipa", "IPA 99% 100 ml", "SBS Parts", "consumabili", "frame", 50, "Sgrassa prima della colla.", {}),
  p("cons-tweezers", "Pinzette ESD", "SBS Parts", "consumabili", "frame", 50, "Maneggiano flex e viti cadute.", {}),
];

export const SLOT_PROMPT: Record<SlotId, string> = {
  frame: "empty CNC smartphone aluminum midframe chassis, hollow interior, no electronics, brushed metal, rounded rectangle",
  soc: "single square black SoC BGA chip, gold edge balls, laser etch, isolated package, NO motherboard",
  ram: "rectangular LPDDR memory package, dark epoxy, gold contacts, isolated chip",
  storage: "UFS NAND flash BGA chip, black package, gold pads, isolated",
  motherboard: "BARE empty smartphone PCB, NO chips, NO SoC, NO RAM, gold unpopulated BGA pad grids, copper traces, tiny passives only",
  thermal: "thin copper vapor chamber cooling plate, no chips on it",
  battery: "silver foil Li-Po pouch cell, warning label, gold nickel tabs, isolated",
  display: "smartphone OLED panel screen OFF, thin bezel, punch-hole, no phone body",
  glass: "clear smartphone protective glass sheet, rounded corners, reflections, isolated",
  backcover: "smartphone back glass, rounded corners, EMPTY square camera cutout top-left, no camera module",
  cameraRear: "isolated smartphone rear camera module with glass lenses, black metal island, no phone body",
  cameraFront: "tiny isolated front camera module, single lens, no phone body",
  speaker: "tiny rectangular smartphone speaker driver, metal grille, isolated",
  usb: "USB-C flex cable connector, gold fingers, tan flex, isolated",
  mic: "tiny MEMS microphone capsule, metal can, isolated",
  haptics: "linear haptic vibration motor, metal, isolated",
  antenna: "tan flexible antenna ribbon cable with copper traces, isolated",
  sim: "nano-SIM metal tray, isolated",
};

export function detailedPartPrompt(part: { name: string; brand: string; slot: SlotId; specs?: string[] }): string {
  const extra = part.specs?.length ? `, markings ${part.specs.join(" / ")}` : "";
  return `Photorealistic top-down product macro of ${part.name} by ${part.brand}, ${SLOT_PROMPT[part.slot]}${extra}. Centered on pure black background, overhead studio lighting, extremely sharp, no watermark, no collage.`;
}

const slotFiles: Record<SlotId, string> = {
  frame: "midframe", soc: "soc-snap", ram: "ram-lpddr", storage: "ufs-chip",
  motherboard: "pcb-bare", thermal: "vapor-chamber", battery: "battery-pouch",
  display: "disp-punch-top", glass: "glass", backcover: "slot-backcover",
  cameraRear: "cam-triple", cameraFront: "cam-front", speaker: "speaker",
  usb: "usb-flex", mic: "mic", haptics: "haptic", antenna: "antenna-flex", sim: "sim-tray",
};
const ID_FILE: Record<string, string> = {
  "bat-stacked": "bat-stacked", "soc-dim95": "soc-dim95",
  "soc-exy26": "soc-exynos", "soc-ten6": "soc-snap", "ram-18": "ram-sk", "sto-1tb41": "ufs-kioxia",
  "cam-peri2": "cam-peri", "camf-50b": "cam-front", "spk-dual": "speaker", "usb-40b": "usb-flex", "hap-xl": "haptic",
  "back-blue": "back-blue", "back-green": "back-green", "back-cer": "back-ceramic",
  "back-red": "back-red", "back-black": "back-black", "back-glossy": "slot-backcover",
  "th-coil": "coil-wireless", "th-vc": "vapor-chamber", "th-gra-vc": "vapor-chamber",
  "soc-8e2": "soc-a19", "soc-x90": "soc-snap", "soc-8e": "soc-snap", "soc-8s": "soc-snap",
  "soc-ex2500": "soc-exynos", "soc-vertv2": "soc-exynos",
  "ram-16": "ram-sk", "ram-24": "ram-sk", "ram-32": "ram-sk", "ram-8x": "ram-sk",
  "sto-256u4": "ufs-kioxia", "sto-512": "ufs-kioxia", "sto-1tb": "ufs-chip",
  "board-std": "pcb-bare", "board-pro": "pcb-bare",
  "frame-alu": "midframe", "frame-ti": "frame-ti", "frame-mag": "midframe",
  "cam-triple": "cam-triple", "cam-quad": "cam-triple", "cam-peri10": "cam-peri",
  "cam-1inch": "cam-peri", "cam-uw": "cam-triple",
  "disp-lcd": "disp-punch-top", "disp-oled": "disp-punch-top", "disp-am": "disp-punch-top",
  "disp-2k": "disp-punch-top", "disp-oled63": "disp-punch-top",
};
const partImgs = import.meta.glob("../assets/parts/*.{png,jpg}", { eager: true, import: "default" }) as Record<string, string>;
function fileUrl(name: string): string | undefined {
  const png = Object.entries(partImgs).find(([k]) => k.endsWith("/" + name + ".png"));
  if (png) return png[1];
  const jpg = Object.entries(partImgs).find(([k]) => k.endsWith("/" + name + ".jpg"));
  return jpg?.[1];
}
export function photoUrlForPart(pt: { id: string; slot: SlotId }): string | undefined {
  return fileUrl(ID_FILE[pt.id] ?? slotFiles[pt.slot]);
}
/** All baked photos, for the custom editor. */
export function inventoryPhotos(): { id: string; url: string; slot: SlotId }[] {
  const out: { id: string; url: string; slot: SlotId }[] = [];
  const seen = new Set<string>();
  for (const pt of PARTS) {
    const url = photoUrlForPart(pt);
    if (!url || seen.has(url)) continue;
    seen.add(url);
    out.push({ id: pt.id, url, slot: pt.slot });
  }
  return out;
}
/* Prezzi OEM indicativi (€) e benchmark reali — AnTuTu v10 / Geekbench 6.
   Fonti: cpu-monkey, techpp, smartprix (confronti 2024-26). */
const MARKET: Record<string, { price: number; antutu?: number; gb6s?: number; gb6m?: number }> = {
  "soc-8e2": { price: 260, antutu: 3400000, gb6s: 3500, gb6m: 11000 },
  "soc-x90": { price: 240, antutu: 3025991, gb6s: 3234, gb6m: 10059 },
  "soc-dim95": { price: 210, antutu: 3150000, gb6s: 3000, gb6m: 9600 },
  "soc-exy26": { price: 195, antutu: 2850000, gb6s: 2900, gb6m: 9300 },
  "soc-ten6": { price: 105, antutu: 1550000, gb6s: 2100, gb6m: 5600 },
  "ram-18": { price: 36 }, "sto-1tb41": { price: 54 },
  "cam-peri2": { price: 88 }, "camf-50b": { price: 22 }, "spk-dual": { price: 16 }, "usb-40b": { price: 12 }, "hap-xl": { price: 9 },
  "frame-classic": { price: 10 },
  "soc-d9400": { price: 180, antutu: 2997173, gb6s: 2874, gb6m: 8969 },
  "soc-8e": { price: 190, antutu: 2100000, gb6s: 2300, gb6m: 7400 },
  "soc-8s": { price: 120, antutu: 1750000, gb6s: 2000, gb6m: 6200 },
  "soc-8g2": { price: 110, antutu: 1600000, gb6s: 2000, gb6m: 5600 },
  "soc-ex2500": { price: 130, antutu: 1900000, gb6s: 2400, gb6m: 7600 },
  "soc-vertv2": { price: 110, antutu: 1650000, gb6s: 2200, gb6m: 6800 },
  "soc-d9300": { price: 140, antutu: 2050000, gb6s: 2300, gb6m: 7200 },
  "soc-tensor": { price: 80, antutu: 1250000, gb6s: 2000, gb6m: 5200 },
  "soc-tensor4": { price: 70, antutu: 1150000, gb6s: 1900, gb6m: 4900 },
  "soc-kirin": { price: 95, antutu: 950000, gb6s: 1500, gb6m: 4200 },
  "soc-7g2": { price: 55, antutu: 1500000, gb6s: 1900, gb6m: 5100 },
  "soc-7g3": { price: 40, antutu: 820000, gb6s: 1100, gb6m: 3000 },
  "soc-6g1": { price: 28, antutu: 600000, gb6s: 950, gb6m: 2700 },
  "soc-q6": { price: 45, antutu: 1400000, gb6s: 1000, gb6m: 3900 },
  "soc-d8300": { price: 48, antutu: 1450000, gb6s: 1050, gb6m: 4000 },
  "soc-d7300": { price: 32, antutu: 750000, gb6s: 1000, gb6m: 2600 },
  "soc-g99": { price: 18, antutu: 400000, gb6s: 720, gb6m: 1900 },
  "soc-helio": { price: 10, antutu: 260000, gb6s: 450, gb6m: 1300 },
  "ram-4": { price: 6 }, "ram-6": { price: 9 }, "ram-8": { price: 14 }, "ram-8x": { price: 18 },
  "ram-12": { price: 22 }, "ram-12lp4": { price: 17 }, "ram-16": { price: 30 }, "ram-24": { price: 45 }, "ram-32": { price: 70 },
  "sto-32": { price: 4 }, "sto-64": { price: 6 }, "sto-128": { price: 9 }, "sto-256": { price: 14 },
  "sto-256u4": { price: 19 }, "sto-512": { price: 26 }, "sto-512u31": { price: 21 }, "sto-1tb": { price: 48 }, "sto-2tb": { price: 95 },
  "bat-3000": { price: 6 }, "bat-3500": { price: 7 }, "bat-4000": { price: 8 }, "bat-4500": { price: 9 },
  "bat-5000": { price: 11 }, "bat-5500": { price: 13 }, "bat-6000": { price: 15 }, "bat-7000": { price: 18 },
  "bat-8000": { price: 22 }, "bat-dual": { price: 19 }, "bat-stacked": { price: 24 },
  "disp-eco": { price: 18 }, "disp-lcd": { price: 24 }, "disp-lcd67": { price: 28 }, "disp-oled": { price: 42 },
  "disp-oled63": { price: 48 }, "disp-oled61": { price: 62 }, "disp-am": { price: 78 }, "disp-2k": { price: 120 }, "disp-fold": { price: 160 },
  "glass-gg3": { price: 6 }, "glass-gg5": { price: 9 }, "glass-gg7": { price: 14 }, "glass-dt": { price: 12 },
  "glass-victus3": { price: 28 }, "glass-armor": { price: 42 }, "glass-zaf": { price: 55 }, "glass-utg": { price: 38 },
  "cam-dual": { price: 14 }, "cam-uw": { price: 26 }, "cam-triple": { price: 42 }, "cam-1inch": { price: 68 },
  "cam-quad": { price: 95 }, "cam-peri10": { price: 78 }, "camf-8": { price: 5 }, "camf-12": { price: 8 }, "camf-32": { price: 14 }, "camf-50": { price: 20 },
  "board-lite": { price: 12 }, "board-std": { price: 22 }, "board-pro": { price: 38 }, "board-rf": { price: 52 }, "board-game": { price: 44 },
  "frame-poly": { price: 6 }, "frame-alu": { price: 14 }, "frame-mag": { price: 18 }, "frame-mg": { price: 24 },
  "frame-flat": { price: 16 }, "frame-ti": { price: 42 }, "frame-ss": { price: 30 },
};

for (const pt of PARTS) {
  pt.img = photoUrlForPart(pt);
  if (pt.slot === "motherboard") pt.yaw = 90;
  if (pt.slot === "battery") pt.yaw = -90;
  if (pt.slot === "haptics") pt.yaw = 180;
  if (pt.slot === "sim") pt.yaw = 90;
  /* i componenti saldati sulla scheda seguono la sua rotazione a 90° */
  if (pt.slot === "soc" || pt.slot === "ram" || pt.slot === "storage") pt.yaw = 90;
  const mk = MARKET[pt.id];
  if (mk && !pt.market) pt.market = mk;
  else if (!pt.market) pt.market = { price: Math.max(3, Math.round((pt.stats?.score ?? 50) * 0.6)) };
}

/* =====================================================================
   OPERATING SYSTEMS
   ===================================================================== */
export const BUILTIN_OS: OSConfig[] = [
  /* Android 9 "Pie" (2018) — Material Design 2: sfondo chiaro, toggles in
     cerchi colorati, orologio a sinistra nella status bar, dock con ricerca. */
  {
    id: "android9",
    name: "Android 9 Pie",
    versionLabel: "9 · API 28 · 2018",
    base: "android9",
    wallpaperA: "#17606b",
    wallpaperB: "#081c26",
    pattern: "waves",
    accent: "#4285f4",
    iconShape: "squircle",
    gridCols: 5,
    fontScale: 1,
    animSpeed: 1,
    showWidget: true,
    bootText: "android",
    darkDefault: false,
    builtin: true,
    navMode: "buttons",
    lockClock: "classic",
    qsStyle: "circles",
    searchBar: true,
    themedIcons: false,
    bootAnim: "orbit",
    sbStyle: "split",
  },
  /* Android 16 (2025) — Material 3 Expressive: orologio gigante, pillole QS
     che diventano rettangoli, blur, slider massicci, icone tematiche. */
  {
    id: "android16",
    name: "Android 16",
    versionLabel: "16 · API 36 · M3 Expressive",
    base: "android16",
    wallpaperA: "#2c3e70",
    wallpaperB: "#0d1424",
    pattern: "waves",
    accent: "#a8c7fa",
    iconShape: "circle",
    gridCols: 4,
    fontScale: 1.05,
    animSpeed: 0.85,
    showWidget: true,
    bootText: "android",
    darkDefault: true,
    builtin: true,
    navMode: "gestures",
    lockClock: "stack",
    qsStyle: "pills",
    searchBar: true,
    themedIcons: true,
    bootAnim: "dots",
    sbStyle: "split",
  },
];

/** Valori effettivi di stile: le opzioni avanzate vuote ereditano dallo stile base. */
export function osEffective(c: OSConfig): {
  navMode: "gestures" | "buttons";
  lockClock: "stack" | "classic" | "corner" | "bold";
  qsStyle: "circles" | "pills";
  searchBar: boolean;
  themedIcons: boolean;
} {
  const a16 = c.base === "android16";
  return {
    navMode: c.navMode ?? (a16 ? "gestures" : "buttons"),
    lockClock: c.lockClock ?? (a16 ? "stack" : "classic"),
    qsStyle: c.qsStyle && c.qsStyle !== "auto" ? c.qsStyle : a16 ? "pills" : "circles",
    searchBar: c.searchBar ?? true,
    themedIcons: c.themedIcons ?? a16,
  };
}

export const WALLPAPER_PRESETS: { a: string; b: string; label: string }[] = [
  { a: "#17606b", b: "#081c26", label: "Laguna" },
  { a: "#2c3e70", b: "#0d1424", label: "Notte blu" },
  { a: "#5b2a86", b: "#160a24", label: "Viola" },
  { a: "#7a3014", b: "#1c0a05", label: "Magma" },
  { a: "#274a3d", b: "#0d1a14", label: "Foresta" },
  { a: "#86303f", b: "#1e0910", label: "Vino" },
  { a: "#3c4450", b: "#101318", label: "Grafite" },
  { a: "#a3671c", b: "#241305", label: "Ambra" },
];

export function defaultCustomOS(name: string, base: "android9" | "android16" | "custom" = "android16"): OSConfig {
  const ref = BUILTIN_OS.find((b) => b.base === base) ?? BUILTIN_OS[1];
  return {
    id: "custom-" + Date.now().toString(36) + Math.floor(Math.random() * 999),
    name: name || "MyOS",
    versionLabel: "1.0 · custom",
    base,
    wallpaperA: "#274a3d",
    wallpaperB: "#0d1a14",
    pattern: base === "android16" ? "waves" : "peaks",
    accent: base === "android16" ? "#a8c7fa" : "#4285f4",
    iconShape: base === "android16" ? "circle" : "squircle",
    gridCols: base === "android16" ? 4 : 5,
    fontScale: 1,
    animSpeed: 1,
    showWidget: true,
    bootText: name || "MyOS",
    darkDefault: base === "android16",
    navMode: ref.navMode,
    lockClock: ref.lockClock,
    qsStyle: ref.qsStyle,
    searchBar: true,
    themedIcons: base === "android16",
    bootAnim: base === "android16" ? "dots" : "orbit",
    sbStyle: base === "android16" ? "split" : "split",
  };
}

/* =====================================================================
   PERFORMANCE MODEL
   ===================================================================== */
const W: Partial<Record<SlotId, number>> = {
  soc: 0.34, ram: 0.15, storage: 0.11, display: 0.1, thermal: 0.07, battery: 0.05,
  glass: 0.03, cameraRear: 0.04, cameraFront: 0.02, speaker: 0.02, usb: 0.01,
  antenna: 0.02, frame: 0.02, backcover: 0.02, haptics: 0.01, mic: 0.01,
};

export function partById(id: string): PartDef | undefined {
  return PARTS.find((x) => x.id === id);
}

export interface PerfReport {
  score: number;
  tier: string;
  bootMs: number;
  launchLag: number; // ms of artificial app-open delay
  animScale: number; // >1 = slower UI
  bench: { cpu: number; gpu: number; mem: number; disk: number; total: number };
  batteryHours: number;
  missing: string[];
  completeness: number; // 0..100
  canPowerOn: boolean;
}

export function computePerf(installed: Partial<Record<SlotId, string>>): PerfReport {
  let score = 0;
  let wsum = 0;
  const val = (s: SlotId) => {
    const id = installed[s];
    if (!id) return null;
    return partById(id)?.stats?.score ?? 60;
  };
  for (const [slot, w] of Object.entries(W) as [SlotId, number][]) {
    const v = val(slot);
    if (v != null) {
      score += v * w;
      wsum += w;
    }
  }
  const norm = wsum > 0 ? score / wsum : 0;

  const missing: string[] = [];
  (["frame", "motherboard", "soc", "ram", "storage", "battery", "display"] as SlotId[]).forEach((s) => {
    if (!installed[s]) missing.push(SLOTS[s].name);
  });

  const socV = val("soc") ?? 0;
  const ramV = val("ram") ?? 0;
  const stoV = val("storage") ?? 0;
  const dispV = val("display") ?? 0;
  const thV = val("thermal") ?? 30;

  const installedCount = Object.keys(installed).length;
  const completeness = Math.min(100, Math.round((installedCount / 15) * 82 + (wsum > 0.9 ? 18 : wsum * 20)));

  const tier = norm < 35 ? "Entry-level" : norm < 55 ? "Media gamma" : norm < 78 ? "Fascia alta" : "Flagship";
  const bootMs = Math.round(10500 - norm * 72);
  const launchLag = Math.round(Math.max(0, 1050 - norm * 10.5));
  const animScale = Math.max(0.75, 1.55 - norm / 95);

  const batId = installed["battery"];
  const cap = batId ? 2600 + (partById(batId)?.stats?.score ?? 40) * 42 : 0;
  const batteryHours = cap > 0 ? Math.round((cap / 330) * 10) / 10 : 0;

  return {
    score: Math.round(norm),
    tier,
    bootMs,
    launchLag,
    animScale,
    bench: {
      cpu: Math.round(socV * 24.6 + ramV * 3.1),
      gpu: Math.round(socV * 17.8 + dispV * 7.4 + thV * 4.2),
      mem: Math.round(ramV * 22.4 + stoV * 9.6),
      disk: Math.round(stoV * 38.5 + 240),
      total: Math.round(socV * 42.4 + ramV * 25.5 + stoV * 19.1 + dispV * 7.4 + thV * 4.2 + 240),
    },
    batteryHours,
    missing,
    completeness,
    canPowerOn: missing.length === 0,
  };
}

/* =====================================================================
   BUILD GUIDE
   ===================================================================== */
export type StepFocus = { kind: "slot" | "glue" | "screw" | "button"; id: string };

export interface GuideStep {
  id: string;
  label: string;
  detail: string;
  optional?: boolean;
  tool?: ToolId; // attrezzo consigliato (clic sul passo = lo equipaggia)
  action?: "tap" | "hold"; // tocco singolo o pressione lunga
  focus?: StepFocus | null; // punto evidenziato in 3D mentre il passo è attivo
  status?: (b: BuildState) => string | null;
  done: (b: BuildState) => boolean;
}

const has = (b: BuildState, s: SlotId) => !!b.installed[s];
const boardScrewsOk = (b: BuildState) =>
  ["s1", "s2", "s3", "s4"].every((id) => !b.screwsOut[id] && !b.screwsLoose[id]);
const boardTightCount = (b: BuildState) =>
  ["s1", "s2", "s3", "s4"].filter((id) => !b.screwsOut[id] && !b.screwsLoose[id]).length;
const minorCount = (b: BuildState) =>
  (["speaker", "usb", "mic", "haptics"] as SlotId[]).filter((s) => has(b, s)).length;

export const GUIDE: GuideStep[] = [
  { id: "g-frame", label: "Installa il telaio", detail: "Dal magazzino scegli un telaio, poi TOCCA la sagoma grande che pulsa sul banco.", tool: "hands", action: "tap", focus: { kind: "slot", id: "frame" }, done: (b) => has(b, "frame") },
  { id: "g-antenna", label: "Flex antenna", detail: "Il flex Wi-Fi/5G si incastra sul bordo superiore del telaio.", optional: true, tool: "hands", action: "tap", focus: { kind: "slot", id: "antenna" }, done: (b) => has(b, "antenna") },
  { id: "g-board", label: "Scheda madre", detail: "Selezionala dal magazzino e TOCCA la sagoma nella metà ALTA del telefono.", tool: "hands", action: "tap", focus: { kind: "slot", id: "motherboard" }, done: (b) => has(b, "motherboard") },
  { id: "g-screws", label: "Avvita le 4 viti M1.6", detail: "Appena posi la scheda, 4 viti restano ALLENTATE (sollevate). Equipaggia il cacciavite e tieni premuto su ciascuna finché non scende a filo. Una vite trasparente sul foro è nel vassoio: tieni premuto per riavvitarla.", tool: "screwdriver", action: "hold", focus: { kind: "screw", id: "board" }, status: (b) => (has(b, "motherboard") && !boardScrewsOk(b) ? `${boardTightCount(b)}/4 avvitate` : null), done: (b) => has(b, "motherboard") && boardScrewsOk(b) },
  { id: "g-soc", label: "SoC sulla scheda", detail: "Il processore va nell'area quadrata BGA: TOCCA la sagoma sulla scheda.", tool: "hands", action: "tap", focus: { kind: "slot", id: "soc" }, done: (b) => has(b, "soc") },
  { id: "g-ram", label: "Modulo RAM", detail: "Slot LPDDR in alto a sinistra sulla scheda.", tool: "hands", action: "tap", focus: { kind: "slot", id: "ram" }, done: (b) => has(b, "ram") },
  { id: "g-sto", label: "Memoria UFS", detail: "Senza memoria nessun OS può essere flashato.", tool: "hands", action: "tap", focus: { kind: "slot", id: "storage" }, done: (b) => has(b, "storage") },
  { id: "g-thermal", label: "Sistema termico", detail: "Va SOTTO la scheda madre, nella metà alta: si posa e basta.", tool: "hands", action: "tap", focus: { kind: "slot", id: "thermal" }, done: (b) => has(b, "thermal") },
  { id: "g-battery", label: "Batteria nella vasca", detail: "La metà BASSA del telefono è la vasca batteria: posa la cella a filo. Aderisce da sola con le linguette arancioni (per rimuoverla servirà il plettro).", tool: "hands", action: "tap", focus: { kind: "slot", id: "battery" }, done: (b) => has(b, "battery") },
  { id: "g-small", label: "Moduli del bordo inferiore", detail: "Speaker, USB-C, microfono e motorino aptico: 4 micro-sedi sul fondo. Dopo USB o speaker compariranno 2 viti da avvitare.", optional: true, tool: "hands", action: "tap", status: (b) => `${minorCount(b)}/4 montati`, done: (b) => minorCount(b) === 4 },
  { id: "g-subscrews", label: "Avvita le 2 viti inferiori", detail: "Dopo USB o speaker, 2 viti M1.2 restano allentate sul bordo inferiore: cacciavite e pressione lunga su ciascuna.", optional: true, tool: "screwdriver", action: "hold", focus: { kind: "screw", id: "sub" }, status: (b) => ((b.installed.usb || b.installed.speaker) && ["s5", "s6"].some((s) => b.screwsLoose[s]) ? `${["s5", "s6"].filter((s) => !b.screwsOut[s] && !b.screwsLoose[s]).length}/2 avvitate` : null), done: (b) => !(b.installed.usb || b.installed.speaker) || ["s5", "s6"].every((s) => !b.screwsLoose[s] && !b.screwsOut[s]) },
  { id: "g-sim", label: "Carrello SIM", detail: "Slot sul fianco sinistro: senza carrello niente rete mobile (ma il Wi-Fi funziona).", optional: true, tool: "hands", action: "tap", focus: { kind: "slot", id: "sim" }, done: (b) => has(b, "sim") },
  { id: "g-camf", label: "Fotocamera frontale", detail: "Sede piccola al centro in alto, sotto il futuro punch-hole.", tool: "hands", action: "tap", focus: { kind: "slot", id: "cameraFront" }, done: (b) => has(b, "cameraFront") },
  { id: "g-glu disp", label: "Colla sul bordo display", detail: "Equipaggia la COLLA B-7000 e TIENI PREMUTO sul contorno luminoso attorno alla sede del display: il cordolo appare sui 4 lati.", tool: "glue", action: "hold", focus: { kind: "glue", id: "display" }, done: (b) => !!b.glueApplied["display"] },
  { id: "g-disp", label: "Pannello display", detail: "Ora il display si può posare: TOCCA la sagoma e preme sull'adesivo appena steso.", tool: "hands", action: "tap", focus: { kind: "slot", id: "display" }, done: (b) => has(b, "display") },
  { id: "g-glass", label: "Vetro protettivo", detail: "Si aggancia a pressione sopra il pannello, senza colla.", tool: "hands", action: "tap", focus: { kind: "slot", id: "glass" }, done: (b) => has(b, "glass") },
  { id: "g-glue back", label: "Colla sul perimetro posteriore", detail: "Gira il telefono (vista retro) e stendi la COLLA sul contorno della sede cover.", tool: "glue", action: "hold", focus: { kind: "glue", id: "backcover" }, done: (b) => !!b.glueApplied["backcover"] },
  { id: "g-back", label: "Cover posteriore", detail: "Allinea il foro fotocamera in alto a sinistra e TOCCA la sagoma.", tool: "hands", action: "tap", focus: { kind: "slot", id: "backcover" }, done: (b) => has(b, "backcover") },
  { id: "g-camr", label: "Fotocamera posteriore", detail: "Il modulo sporge dal foro quadrato della cover: si posa a pressione.", tool: "hands", action: "tap", focus: { kind: "slot", id: "cameraRear" }, done: (b) => has(b, "cameraRear") },
  { id: "g-os", label: "Flash del sistema operativo", detail: "Apri il pannello SOFTWARE in alto a destra e scegli Android 9, Android 16 o un tuo OS.", focus: null, done: (b) => !!b.osId },
  { id: "g-power", label: "Prima accensione", detail: "TOCCA il tasto POWER sul fianco destro del telefono (quello più lungo).", focus: { kind: "button", id: "power" }, done: (b) => b.poweredOnce },
];

/* =====================================================================
   DEVICE & SETTINGS
   ===================================================================== */
export function detectDevice(): DeviceInfo {
  const mobile =
    /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent) ||
    (navigator.maxTouchPoints > 1 && window.innerWidth < 1000);
  const smallScreen = Math.min(window.innerWidth, window.innerHeight) < 420;
  const cores = navigator.hardwareConcurrency || 4;
  const dpr = window.devicePixelRatio || 1;
  const suggestedPreset: QualitySettings["preset"] =
    smallScreen || (mobile && cores <= 4) ? "bassa" : mobile ? "media" : cores >= 8 && dpr > 1 ? "ultra" : "alta";
  return {
    mobile,
    smallScreen,
    cores,
    dpr,
    suggestedPreset,
    label: mobile ? (smallScreen ? "Mobile · schermo HD" : "Mobile") : "PC Desktop",
  };
}

export const PRESETS: Record<QualitySettings["preset"], Pick<QualitySettings, "scale" | "shadows" | "particles" | "fx" | "texQuality">> = {
  bassa: { scale: 0.7, shadows: false, particles: false, fx: false, texQuality: "bassa" },
  media: { scale: 0.9, shadows: true, particles: false, fx: true, texQuality: "media" },
  alta: { scale: 1, shadows: true, particles: true, fx: true, texQuality: "alta" },
  ultra: { scale: 1.35, shadows: true, particles: true, fx: true, texQuality: "alta" },
};

export function defaultProfile(): Profile {
  const dev = detectDevice();
  return {
    company: "",
    phoneName: "ONE",
    settings: { preset: dev.suggestedPreset, ...PRESETS[dev.suggestedPreset], musicVol: 0.6, sfxVol: 0.8, resolution: "native" },
    customOS: [],
    customParts: [],
    build: emptyBuild(),
    benchHints: true,
  };
}

export function emptyBuild(): BuildState {
  return {
    installed: {},
    screwsOut: Object.fromEntries(SCREWS.map((s) => [s.id, s.group === "board" ? false : false])),
    screwsLoose: {},
    glueApplied: {},
    osId: null,
    poweredOnce: false,
  };
}

export const CATEGORY_LABELS: Record<Category, string> = {
  telaio: "Telai e scocche",
  schede: "Schede madri",
  processori: "Processori (SoC)",
  memorie: "RAM e memorie",
  display: "Display",
  vetro: "Vetri",
  batterie: "Batterie",
  fotocamere: "Fotocamere",
  audio: "Audio",
  porte: "Porte e connettori",
  raffreddamento: "Raffreddamento",
  moduli: "Moduli minori",
  consumabili: "Consumabili",
  custom: "Le tue creazioni",
};

export const TOOLS = [
  { id: "hands", name: "Mani", desc: "Installa e rimuovi i componenti a pressione.", key: "1" },
  { id: "screwdriver", name: "Cacciavite PH00", desc: "Avvita e svita le viti Phillips M1.6.", key: "2" },
  { id: "pick", name: "Plettro in metallo", desc: "Solleva display, cover e linguette incollate.", key: "3" },
  { id: "glue", name: "Colla B-7000", desc: "Colla specifica per smartphone: cordolo sui bordi.", key: "4" },
] as const;
