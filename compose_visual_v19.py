from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,hashlib,base64,io,collections
R=Path(__file__).parent;O=Path('/home/user/Configurazioni-V19');O.mkdir(exist_ok=True)
D=json.loads((R/'coordinates-v17.json').read_text());items=D['items'];by={i['file']:i for i in items};sku={i['sku']:i for i in items};boards={b['file']:b for b in D['boards']};old=json.loads((R/'finals/composition-manifest.json').read_text());cache={}
for i in items:
 if i.get('excludedFromFinals'):continue
 im=Image.open(R/('originals' if i['set']<=6 else 'generated')/i['file']).convert('RGBA').crop(i['crop']);cache[i['file']]=im
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(n):return ImageFont.truetype(F,n)
# This is a rendering-only editorial correction, not a new physical memory specification.
im=cache['set06-ram-16.png'];dd=ImageDraw.Draw(im);dd.rectangle((55,355,im.width-43,435),fill=(43,44,44,255));dd.text((83,377),'bin da verificare',font=font(32),fill=(192,194,190,255))
W,H=2800,1850;S=46;BG='#e9eff2';INK='#142e3a';BLUE='#186a8c';AMBER='#a96a15';RED='#b34354'
ramrules={'soc-x90':'LPDDR5X','soc-8e':'LPDDR5X','soc-7g2':'LPDDR5X','soc-8s':'LPDDR5X','soc-g99':'LPDDR4X','soc-d8300':'LPDDR5X','soc-d9400':'LPDDR5X','soc-dim95':'LPDDR5X','soc-ex2500':'LPDDR5X'}
# Normalized image-space bounds estimated after multimodal review; not dimensions of a manufactured part.
coverroi={'back-blue':(.06,.025,.42,.21),'back-glossy':(.06,.025,.44,.215),'back-matte':(.045,.025,.45,.22),'back-cer':(.06,.025,.40,.21),'back-green':(.055,.03,.44,.31),'back-alu':(.05,.025,.46,.22),'back-leather':(.065,.025,.45,.22),'back-red':(.04,.025,.49,.25),'back-black':(.055,.025,.42,.29),'back-white':(.05,.025,.32,.32),'back-carbon':(.04,.025,.46,.29),'back-wood':(.055,.025,.53,.26)}
records=[]
def drawtxt(dr,xy,t,n=18,c=INK):dr.text(xy,str(t),font=font(n),fill=c)
def wrap(dr,text,xy,width,n=17):
 x,y=xy;cur=''
 for w in text.split():
  t=(cur+' '+w).strip()
  if dr.textlength(t,font=font(n))>width and cur:drawtxt(dr,(x,y),cur,n);y+=n+6;cur=w
  else:cur=t
 if cur:drawtxt(dr,(x,y),cur,n);y+=n+6
 return y
def path(i):return str((Path('originals') if i['set']<=6 else Path('generated'))/i['file'])
for c in old['compositions']:
 pair=c['pair'];selected={role:by[Path(p).name] for role,p in c['selected'].items()};changes=[];soc=selected['soc']['sku'];ram=selected['ram'];required=ramrules.get(soc)
 if required and required not in ram['sku'] and required not in {'ram-4':'LPDDR4X','ram-6':'LPDDR4X','ram-12lp4':'LPDDR4X','ram-8':'LPDDR5'}.get(ram['sku'],'LPDDR5X'):
  candidates=[i for i in items if i['set'] in pair and i['slot']=='ram' and i['sku'] not in ['ram-4','ram-6','ram-12lp4','ram-8']]
  replacement=candidates[0] if candidates else sku['ram-12'];changes.append(f"RAM: {ram['sku']} -> {replacement['sku']} (tipo documentato; package non qualificato)");selected['ram']=replacement
 if soc=='soc-g99' and selected['storage']['sku']!='sto-64':changes.append('Storage G99: sto-1tb -> sto-64 (classe UFS 2.2; dispositivo da qualificare)');selected['storage']=sku['sto-64']
 owned=[i for i in items if i['set'] in pair and not i.get('excludedFromFinals')];selnames={i['file'] for i in selected.values()};inventory=[i for i in owned if i['file'] not in selnames and i['slot'] not in ['ram','storage']];borrowed=[i for i in selected.values() if i['set'] not in pair]
 can=Image.new('RGBA',(W,H),BG);dr=ImageDraw.Draw(can);places=[];notes=[]
 def put(i,box,kind,angle=0,detail=False):
  im=cache[i['file']].copy()
  if angle:im=im.rotate(-angle,expand=True,resample=Image.Resampling.BICUBIC)
  x,y,w,h=box;t=min(w/im.width,h/im.height);nw,nh=max(1,round(im.width*t)),max(1,round(im.height*t));px,py=round(x+(w-nw)/2),round(y+(h-nh)/2);can.alpha_composite(im.resize((nw,nh),Image.Resampling.LANCZOS),(px,py));places.append({'file':path(i),'sku':i['sku'],'plane':kind,'rectPx':[px,py,nw,nh],'clockwiseDegrees':angle,'borrowed':i['set'] not in pair,'detailOnly':detail,'placementEvidence':'VISUAL_ESTIMATE_NOT_MANUFACTURING_DATA','sourceCropPx':i['crop'],'pixelsPerRotatedSourcePixel':t,'renderLabelOverride':'bin da verificare' if i['sku']=='ram-16' else None});return [px,py,nw,nh]
 def label(i):return i['sku']+(' *' if i['set'] not in pair else '')
 def outline(cx,top):
  dr.rounded_rectangle((cx-7.4*S/2,top,cx+7.4*S/2,top+15.8*S),radius=22,outline='#b7c7ce',width=2)
  for z in [0,4,8,12,15.8]:dr.line((cx-7.4*S/2-5,top+z*S,cx-7.4*S/2,top+z*S),fill='#8ea4af',width=1)
 def local(i,cx,top,x,z,w,h,plane,angle=0):
  rect=put(i,(cx+(x-w/2)*S,top+(7.9+z-h/2)*S,w*S,h*S),plane,angle);places[-1]['nominalPlaneCenterCm']=[x,z];places[-1]['requestedEnvelopeCm']=[w,h];return rect
 dr.rectangle((0,0,W,11),fill=BLUE);drawtxt(dr,(50,35),'SET LAB  /  POSIZIONAMENTO DA IMMAGINI  /  V19',21,BLUE);drawtxt(dr,(50,78),f"SET {pair[0]:02d} + {pair[1]:02d}",48);drawtxt(dr,(630,93),f"VARIANTE {c['variant']:02d}/{c['variantCount']:02d}",25)
 drawtxt(dr,(50,148),'Proposta visiva a livelli • ingombri stimati • niente saldature o compatibilità dichiarate come collaudate',20,AMBER)
 drawtxt(dr,(50,188),f"{selected['soc']['sku']}  /  {selected['ram']['sku']}  /  {selected['storage']['sku']}",19)
 centers=[210,580,950,1320,1690,2060];tops=[435,395,355,315,275,235]
 titles=['01  COVER','02  RETRO / TERMICA','03  CONFRONTO TELAIO','04  BORDI / FLEX','05  DISPLAY','06  VETRO']
 for cx,top,title in zip(centers,tops,titles):drawtxt(dr,(cx-160,top-62),title,20,BLUE)
 # Cover anchor is determined from the visible aperture/island, not assumed globally identical.
 cover=selected['backcover'];sz=cover['size'];rect=put(cover,(centers[0]-sz[0]*S/2,tops[0],sz[0]*S,sz[2]*S),'cover',cover.get('angle') or 0);x,y,w,h=rect;u,v,uw,vh=coverroi[cover['sku']];roi=[x+u*w,y+v*h,uw*w,vh*h];dr.rounded_rectangle((roi[0],roi[1],roi[0]+roi[2],roi[1]+roi[3]),radius=10,outline=RED,width=3);drawtxt(dr,(centers[0]-158,tops[0]-32),label(cover),16)
 # Rear plane: module envelope associated with the cover's camera region. No claim of matching lenses.
 cx,top=centers[1],tops[1];outline(cx,top);normcx=u+uw/2;normcy=v+vh/2;rear=selected['cameraRear'];rx=(normcx-.5)*7.4;rz=normcy*15.8-7.9
 # Elongated periscopes preserved; do not squeeze entire modules into lens openings.
 if rear['sku'] in ['cam-peri2','cam-peri10','cam-uw']:cw,ch=5.7,2.0;rx=0;rz=-5.5;notes.append('Camera multipla/periscopio: gruppo separato; centri lente/aperture non coincidono automaticamente.')
 else:cw,ch=2.25,3.0
 local(rear,cx,top,rx,rz,cw,ch,'rear_camera_envelope');drawtxt(dr,(cx-155,top+180),label(rear),15)
 thermal=selected['thermal'];local(thermal,cx,top,0,-.5,6.0,4.4,'rear_thermal_proposal',thermal.get('angle') or 0);drawtxt(dr,(cx-155,top+440),label(thermal),15)
 drawtxt(dr,(cx-155,top+650),'Sagoma ≠ allineamento ottico',15,AMBER)
 # Main frame and core. Background frame is visible; PCB position derived from registered raster seats.
 cx,top=centers[2],tops[2];frame=selected['frame'];sz=frame['size'];put(frame,(cx-sz[0]*S/2,top,sz[0]*S,sz[2]*S),'frame',frame.get('angle') or 0);drawtxt(dr,(cx-155,top-32),label(frame),16)
 board=selected['motherboard'];b=boards[board['file']];sz=board['size'];br=local(board,cx,top,board['pos'][0],board['pos'][2],sz[0],sz[2],'board_visual',0);boardlayer=cache[board['file']].copy();ld=ImageDraw.Draw(boardlayer);mounted=[]
 for role in ['soc','ram','storage']:
  chip=selected[role];ok=role in b['slots'] and not(board['sku']=='board-pro' and role!='soc') and chip['sku']!='sto-32'
  if ok:
   ax,ay,aw,ah=b['slots'][role];sx,sy=br[2]/b['raster'][0],br[3]/b['raster'][1];put(chip,(br[0]+(ax+.05*aw)*sx,br[1]+(ay+.05*ah)*sy,aw*.9*sx,ah*.9*sy),'visual_footprint_'+role,chip.get('angle') or 0);mounted.append(role)
   im=cache[chip['file']].copy();im.thumbnail((round(aw*.9),round(ah*.9)));boardlayer.alpha_composite(im,(round(ax+(aw-im.width)/2),round(ay+(ah-im.height)/2)))
  else:notes.append(f"{chip['sku']}: fuori scheda, sede non dimostrata.")
 bat=selected['battery'];bs=bat.get('size') or [5.5,.4,6.8];bx=-1.0 if frame['sku']=='frame-flat' else 0;bw=4.0 if frame['sku']=='frame-flat' else min(bs[0],5.7);local(bat,cx,top,bx,2.35 if frame['sku']=='frame-flat' else 3.25,bw,min(bs[2],6.4),'battery_visual',bat.get('angle') or 0);drawtxt(dr,(cx-150,top+15.8*S+12),label(bat),16)
 # Perimeter plane gives proposed local coordinates for every selected peripheral instead of a bottom tray only.
 cx,top=centers[3],tops[3];outline(cx,top)
 layout={'antenna':(0,-6.55,6.5,.65),'cameraFront':(0,-7.05,.7,.65),'sim':(-3.1,-2.6,.65,2.1),'haptics':(2.25,4.2,1.5,1.0),'speaker':(1.85,6.55,2.6,.95),'usb':(0,7.15,1.8,.7),'mic':(-2.65,6.65,.65,.65)}
 for role,(lx,lz,lw,lh) in layout.items():
  i=selected[role]
  if role=='sim' and i['sku']=='sim-hybrid':lx,lz,lw,lh=-1.8,-2.6,2.4,1.0;notes.append('SIM ibrida: tre vani visivi; solo inviluppo, meccanismo non qualificato.')
  if role=='haptics' and i['sku']=='hap-dual':lx,lw=0,4.8
  rectp=local(i,cx,top,lx,lz,lw,lh,'perimeter_'+role,i.get('angle') or 0)
  # Non-overlapping textual key is below the view; small numbered dots identify items.
  k=list(layout).index(role)+1;px,py,ww,hh=rectp;dr.ellipse((px-14,py-14,px+10,py+10),fill=BLUE);drawtxt(dr,(px-9,py-14),str(k),14,'white')
 for j,role in enumerate(layout):drawtxt(dr,(cx-160,top+15.8*S+12+j*21),f'{j+1}  {label(selected[role])}',14)
 # Display and glass: center alignment only, preserve different silhouettes and holes.
 for role,cx,top in [('display',centers[4],tops[4]),('glass',centers[5],tops[5])]:
  i=selected[role];sz=i['size'];rectp=put(i,(cx-sz[0]*S/2,top,sz[0]*S,sz[2]*S),'front_'+role,i.get('angle') or 0);drawtxt(dr,(cx-155,top-32),label(i),16)
  xx,yy,ww,hh=rectp;anchor=(xx+ww*.5,yy+hh*.04);dr.ellipse((anchor[0]-8,anchor[1]-8,anchor[0]+8,anchor[1]+8),outline=RED,width=2)
  drawtxt(dr,(cx-155,top+sz[2]*S+18),'Asse centrato / foro da verificare',14,AMBER)
 # Sidebar inventories ensure the original pair's alternatives are never silently lost.
 dr.rounded_rectangle((2290,35,2765,1670),radius=18,fill='#d8e3e9');drawtxt(dr,(2315,62),'ALTERNATIVE / BANCO',22);drawtxt(dr,(2315,99),'Non montate simultaneamente',16,AMBER)
 rows=max(1,math.ceil(len(inventory)/2));rh=min(173,1500/rows)
 for j,i in enumerate(inventory):
  xx=2310+(j%2)*222;yy=140+(j//2)*rh;put(i,(xx+6,yy+2,200,rh-55),'inventory',detail=True);drawtxt(dr,(xx+3,yy+rh-48),i['sku'],15);drawtxt(dr,(xx+3,yy+rh-25),'consumabile / utensile' if i['sku'].startswith('cons-') else 'alternativa non qualificata',12,AMBER)
 # Native board close-up, separate from placement scale.
 dr.line((48,1290,2245,1290),fill=BLUE,width=2);drawtxt(dr,(50,1310),'LETTURA DEGLI INCASTRI',20,BLUE)
 fits=[]
 if frame['sku']=='frame-classic':fits.append('Telaio classic: vista frontale con tasto Home. Il confronto sovrapposto NON individua una vasca interna o fissaggi PCB.')
 elif frame['sku']=='frame-flat':fits.append('Telaio flat: vasca batteria stretta a sinistra e rail largo a destra. Il vecchio inviluppo centrato invadeva il rail; corretto il riquadro della vasca.')
 elif frame['sku']=='frame-mag':fits.append('Telaio magnetico: anello e traverse al centro; la sovrapposizione non dimostra spessore o piano di appoggio della batteria.')
 elif frame['sku']=='frame-ti':fits.append('Telaio titanio: solo cornice perimetrale. Il raster non mostra supporti interni per fissare motherboard e batteria.')
 else:fits.append('Vasca inferiore e zona PCB superiore distinguibili. Controllare traverse e sedi viti: una scheda rettangolare non dimostra un incastro sul telaio.')
 if selected['glass']['sku']=='glass-gg7':fits.append('Vetro 7i: foro alto decentrato a destra; il display selezionato ha camera alta centrale. Allineamento ottico non accettato.')
 elif selected['glass']['sku']=='glass-gg3':fits.append('Vetro GG3: apertura a fessura superiore; il display selezionato mostra notch/foro. Non sono aperture automaticamente equivalenti.')
 else:fits.append('Vetro: bordo e trasparenza non dimostrano quote o apertura camera. Foro e riscontro adesivo richiedono una vista specifica.')
 if cover['sku'] in ['back-green','back-red','back-black','back-white','back-carbon','back-wood']:fits.append('Cover con aperture multiple: il numero e la disposizione dei fori non corrispondono automaticamente al modulo camera. Nessun montaggio forzato.')
 else:fits.append('Cover con finestra unica: permette solo un confronto di sagoma del blocco camera, non la verifica di lenti, altezza e fissaggio.')
 yy=1350
 for t in fits:yy=wrap(dr,'• '+t,(50,yy),610,18)+14
  # The chips whose seats cannot be inferred are visible, not arbitrarily soldered.
 separate=[selected[k] for k in ['ram','storage'] if k not in mounted]
 drawtxt(dr,(710,1310),'COMPONENTI CON SEDE SOSPESA',20,BLUE)
 details=separate+[selected['cameraRear'],selected['cameraFront']]
 for j,i in enumerate(details):
  xx=710+(j%2)*255;yy=1350+(j//2)*150;put(i,(xx,yy,232,106),'detail_unmounted' if i in separate else 'detail_camera',detail=True);drawtxt(dr,(xx,yy+112),label(i),15)
 # Alignment findings, with no fake geometry repair.
 notes.insert(0,'Cover: finestra/isola visiva evidenziata in rosso; il modulo camera non prova la coincidenza delle lenti.')
 notes.insert(1,'Vetro/display: centri allineati, sagome e fori preservati; tolleranze e adesivi non verificati.')
 if frame['sku']=='frame-classic':notes.append('Telaio classic con tasto home: display di riferimento non specifico, accoppiamento sospeso.')
 notes+=changes
 yy=1347;drawtxt(dr,(1270,1310),'ESITO DEL POSIZIONAMENTO',20,BLUE)
 for note in notes:yy=wrap(dr,'• '+note,(1270,yy),970,17)+8
 drawtxt(dr,(50,1750),'* Presi da altri SET: '+', '.join(i['sku'] for i in borrowed) if borrowed else '* Nessun componente preso da altri SET.',15)
 drawtxt(dr,(50,1780),'Quote locali in JSON: stime nominali 74 × 158 mm, non tolleranze reali. PCB: fit visivo. Batteria/moduli: inviluppi proporzionali.',16,AMBER)
 drawtxt(dr,(50,1811),'NESSUN COLLAUDO FISICO • nessuna saldatura verificata • Fold e UTG dedicato esclusi • '+c['file'].replace('.png','-V19.png'),15)
 name=c['file'].replace('.png','-V19.png');can.convert('RGB').save(O/name,optimize=True)
 records.append({'file':name,'pair':pair,'variant':c['variant'],'selected':{role:path(i) for role,i in selected.items()},'selectionChanges':changes,'borrowed':[path(i) for i in borrowed],'placements':places,'coverRegionNormalized':coverroi[cover['sku']],'notes':notes,'multimodalFitFindings':fits,'electronicCompatibilityVerified':False,'physicalTestingPerformed':False,'visualReview':'PENDING','sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()});print(name,flush=True)
coverage={path(i):sum(any(p['file']==path(i) for p in c['placements']) for c in records if i['set'] in c['pair']) for i in items if not i.get('excludedFromFinals')};assert all(n>0 for p,n in coverage.items() if by[Path(p).name]['slot'] not in ['ram','storage'])
for c in records:
 for p in c['placements']:
  x,y,w,h=p['rectPx'];assert x>=0 and y>=0 and x+w<=W and y+h<=H,(c['file'],p)
manifest={'version':19,'basis':'Multimodal visual estimates; 5 PCB details and 4 shell/display/glass/frame atlases re-read. No engineering drawings inferred.','count':len(records),'canvas':[W,H],'nominalPixelsPerCm':S,'memoryPolicy':'Exactly one rendered RAM and exactly one rendered storage per image; no inventory alternatives or duplicate PCB zoom.','coverRegions':coverroi,'excludedSku':['disp-fold','glass-utg'],'activePairCoverage':coverage,'compositions':records};(O/'posizionamenti-v19.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# One rendering occurrence per selected memory; no hidden duplicate zooms.
for rec in records:
 for role in ['ram','storage']:
  occurrences=[p for p in rec['placements'] if by[Path(p['file']).name]['slot']==role]
  assert len(occurrences)==1,(rec['file'],role,occurrences)
# Render review sheets outside workspace deliverables.
for first in range(1,17,2):
 recs=[c for c in records if c['pair'][0]==first];tw,th=1050,694;sheet=Image.new('RGB',(tw*2,math.ceil(len(recs)/2)*(th+30)),BG);dd=ImageDraw.Draw(sheet)
 for j,c in enumerate(recs):
  im=Image.open(O/c['file']);im.thumbnail((tw,th));x,y=(j%2)*tw,(j//2)*(th+30);sheet.paste(im,(x,y));drawtxt(dd,(x+8,y+th),c['file'],17)
 sheet.save(R/f'analysis/v19-review-{first:02d}.jpg',quality=91)
# Self-contained preview, stored in workspace with images.
parts=[]
for c in records:
 im=Image.open(O/c['file']);im.thumbnail((1800,1200));bio=io.BytesIO();im.save(bio,'JPEG',quality=85);enc=base64.b64encode(bio.getvalue()).decode();parts.append(f'<article data-pair="{c["pair"][0]}"><h2>SET {c["pair"][0]:02d} + {c["pair"][1]:02d} — variante {c["variant"]}</h2><img src="data:image/jpeg;base64,{enc}" loading="lazy"><p>{c["file"]}</p></article>')
opts=''.join(f'<option value="{a}">SET {a:02d} + {a+1:02d}</option>' for a in range(1,17,2))
(O/'GALLERIA.html').write_text('''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SET Lab V19 — posizionamenti visivi</title><style>body{margin:0;background:#e9eff2;color:#142e3a;font:16px system-ui}header{padding:30px 4vw;background:#142e3a;color:white}header p{max-width:1000px;line-height:1.6}nav{padding:15px 4vw;position:sticky;top:0;background:#d8e3e9}select{font:inherit;padding:10px}main{padding:20px 3vw}article{margin-bottom:50px}img{width:100%;height:auto}h2{font-size:22px}</style><header><h1>29 proposte di posizionamento — V19</h1><p>Una sola RAM e una sola archiviazione per immagine. Sei livelli: cover, retro/termica, confronto telaio/PCB, bordi/flex, display e vetro. Posizioni stimate dalle immagini, non misure di fabbricazione. Nessun collaudo dichiarato. Nessuna memoria alternativa o ripetuta. Gli esiti degli incastri sono annotati nelle tavole; le altre alternative e gli utensili restano separati. PNG originali 2800×1850 nella stessa cartella.</p></header><nav><select id="p"><option value="all">Tutte le coppie</option>'''+opts+'''</select></nav><main>'''+''.join(parts)+'''</main><script>document.querySelector('#p').onchange=e=>document.querySelectorAll('article').forEach(a=>a.hidden=e.target.value!=='all'&&a.dataset.pair!==e.target.value);</script></html>''')
print('Done',len(records),'coverage',len(coverage))
