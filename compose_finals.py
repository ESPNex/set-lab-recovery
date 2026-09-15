"""Reproducible non-fold illustrative exploded compositions, one family per SET pair.
Source PNGs are composited without image-model regeneration. Physical fit is not asserted.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,hashlib,base64,io,html,collections
R=Path(__file__).parent;O=R/'finals';O.mkdir(exist_ok=True)
D=json.loads((R/'coordinates-v17.json').read_text());items=D['items'];byfile={i['file']:i for i in items};boards={b['file']:b for b in D['boards']}
active=[i for i in items if not i.get('excludedFromFinals')]; cache={}
for i in active:
 p=R/('originals' if i['set']<=6 else 'generated')/i['file'];cache[i['file']]=Image.open(p).convert('RGBA').crop(i['crop'])
BG='#edf0eb';INK='#193329';GREEN='#297354';MUTED='#667970';ACC='#b9dd6d';W,H=2200,1600;S=41
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def f(n):return ImageFont.truetype(fontpath,n)
def txt(draw,xy,t,n=18,col=INK):draw.text(xy,str(t),font=f(n),fill=col)
def wrap(draw,t,x,y,width,n=17,line=24):
 words=t.split();cur=''
 for word in words:
  test=(cur+' '+word).strip()
  if draw.textlength(test,font=f(n))>width and cur:txt(draw,(x,y),cur,n);y+=line;cur=word
  else:cur=test
 if cur:txt(draw,(x,y),cur,n);y+=line
 return y
def source_path(i):return str((Path('originals') if i['set']<=6 else Path('generated'))/i['file'])
roles=['motherboard','soc','ram','storage','battery','frame','backcover','display','glass','cameraRear','cameraFront','antenna','speaker','usb','haptics','mic','sim','thermal']
countroles=['soc','ram','storage','battery','frame','backcover','display','glass','cameraRear','cameraFront']
def unique(seq):
 out=[];seen=set()
 for i in seq:
  if i['sku'] not in seen:out.append(i);seen.add(i['sku'])
 return out
fallback={role:next(i for i in active if i['slot']==role and i['set']<=2 and not i['sku'].startswith('cons-')) for role in roles}
records=[];allplacements=[];family=[]
for first in range(1,17,2):
 pair=[first,first+1];owned=[i for i in active if i['set'] in pair];groups={role:unique([i for i in owned if i['slot']==role and not i['sku'].startswith('cons-')]) for role in roles}
 n=max([len(groups[role]) for role in countroles]+[1]);family.append({'sets':pair,'count':n,'reason':'Maximum number of available distinct variants in a principal role; round-robin selection, not Cartesian or engineering compatibility.'})
 for v in range(n):
  selected={role:(groups[role][v%len(groups[role])] if groups[role] else fallback[role]) for role in roles}
  if first==11:selected['motherboard']=byfile['set03-board-pro.png']
  borrowed=[i for i in selected.values() if i['set'] not in pair];chosen={i['file'] for i in selected.values()};inventory=[i for i in owned if i['file'] not in chosen]
  name=f'pair-{first:02d}-{first+1:02d}-v{v+1:02d}.png';canvas=Image.new('RGBA',(W,H),BG);draw=ImageDraw.Draw(canvas);placements=[]
  def place(i,box,kind,angle=0,cm=False):
   im=cache[i['file']].copy()
   if angle:im=im.rotate(-angle,expand=True,resample=Image.Resampling.BICUBIC)
   x,y,bw,bh=box;scale=min(bw/im.width,bh/im.height);nw,nh=max(1,round(im.width*scale)),max(1,round(im.height*scale));im=im.resize((nw,nh),Image.Resampling.LANCZOS);px,py=round(x+(bw-nw)/2),round(y+(bh-nh)/2);canvas.alpha_composite(im,(px,py));placements.append({'file':source_path(i),'sku':i['sku'],'kind':kind,'borrowed':i['set'] not in pair,'rectPx':[px,py,nw,nh],'rotationClockwiseDeg':angle,'scalePxPerRotatedCropPixel':scale,'commonNominalCmScale':cm});return px,py,nw,nh
  draw.rectangle((0,0,W,12),fill=GREEN);txt(draw,(55,35),'SET LAB  /  ESPLOSI DI CATALOGO',20,GREEN)
  txt(draw,(55,76),f'SET {first:02d} + {first+1:02d}',49);txt(draw,(640,92),f'VARIANTE {v+1:02d} / {n:02d}',26)
  txt(draw,(55,147),f"{selected['soc']['sku']}  /  {selected['ram']['sku']}  /  {selected['storage']['sku']}  /  {selected['battery']['sku']}",20)
  txt(draw,(55,186),'Esploso 2D illustrativo • livelli separati • accoppiamenti fisici ed elettronici non certificati',17,MUTED)
  # Common nominal scale for five separated layers, no perspective distortion.
  centers=[205,535,865,1195,1525];tops=[455,405,355,305,255];layerroles=['backcover','frame',None,'display','glass'];titles=['01  SCOCCA','02  TELAIO','03  NUCLEO','04  DISPLAY','05  VETRO']
  for cx,top,role,title in zip(centers,tops,layerroles,titles):
   draw.line((cx,top-35,cx,1120),fill='#d1d8d0',width=1);txt(draw,(cx-145,top-88),title,19,GREEN)
   if role:
    i=selected[role];sz=i.get('size');ww,hh=(sz[0]*S,sz[2]*S) if sz else (7.4*S,15.8*S);ww,hh=min(ww,310),min(hh,700)
    place(i,(cx-ww/2,top,ww,hh),'separated_layer',i.get('angle') or 0,True)
    txt(draw,(cx-145,top-58),i['sku']+(' *' if i['set'] not in pair else ''),16)
   else:
    draw.rounded_rectangle((cx-7.4*S/2,top,cx+7.4*S/2,top+15.8*S),radius=22,outline='#b4c4b6',width=2)
    board=selected['motherboard'];b=boards[board['file']];sz=board['size'];bx=cx+(board['pos'][0])*S;by=top+(7.9+board['pos'][2])*S
    rect=place(board,(bx-sz[0]*S/2,by-sz[2]*S/2,sz[0]*S,sz[2]*S),'board_nominal',0,True);px,py,bw,bh=rect
    txt(draw,(cx-145,top-58),board['sku']+(' *' if board['set'] not in pair else ''),16)
    mounted=[]
    for role2 in ['soc','ram','storage']:
     chip=selected[role2]
     allowed=role2 in b['slots'] and not (board['sku']=='board-pro' and role2!='soc') and not(chip['sku']=='sto-32')
     if allowed:
      rx,ry,rw,rh=b['slots'][role2];sx,sy=bw/b['raster'][0],bh/b['raster'][1]
      place(chip,(px+(rx+rw*.05)*sx,py+(ry+rh*.05)*sy,rw*.9*sx,rh*.9*sy),'hypothetical_footprint_fit',chip.get('angle') or 0);mounted.append(role2)
    bat=selected['battery'];sz=bat.get('size');ww,hh=(sz[0]*S,sz[2]*S) if sz else (5.5*S,6.8*S);hh=min(hh,6.8*S);ww=min(ww,5.6*S)
    place(bat,(cx-ww/2,top+8.25*S,ww,hh),'battery_separated_below_board',bat.get('angle') or 0,False)
    txt(draw,(cx-140,top+15.8*S+12),bat['sku'],16)
  # Exploded-level order rail, not a supposed connector or electrical path.
  draw.line((60,1150,1675,1150),fill=GREEN,width=2);txt(draw,(60,1118),'Livelli esterni: scala nominale comune 41 px/cm • nucleo: sedi grafiche ipotetiche',16,MUTED)
  tray=[selected[role] for role in ['cameraRear','cameraFront','antenna','speaker','usb','haptics','mic','sim','thermal']]+[selected[role] for role in ['ram','storage'] if role not in mounted]
  txt(draw,(60,1170),'MODULI SEPARATI  /  ingrandimenti indipendenti, nessuna sede forzata',18,GREEN)
  cols=6;cw=266;rh=135
  for j,i in enumerate(tray):
   x=60+(j%cols)*cw;y=1208+(j//cols)*rh;draw.rounded_rectangle((x,y,x+cw-12,y+rh-10),radius=10,fill='#e0e6dd');place(i,(x+10,y+7,cw-32,85),'unmounted_module_detail',i.get('angle') or 0);txt(draw,(x+12,y+97),i['sku']+(' *' if i['set'] not in pair else ''),15)
  # All pair-owned alternatives and workshop tools remain visibly separated.
  draw.rounded_rectangle((1735,32,2168,1490),radius=18,fill='#dfe7da');txt(draw,(1757,59),'ALTERNATIVE & BANCO',21);txt(draw,(1757,92),'Della coppia • non montati insieme',15,MUTED)
  rows=max(1,math.ceil(len(inventory)/2));ch=min(158,1300/rows)
  for j,i in enumerate(inventory):
   x=1757+(j%2)*202;y=140+(j//2)*ch;place(i,(x+5,y+2,181,ch-53),'pair_inventory');txt(draw,(x,y+ch-47),i['sku'],14);txt(draw,(x,y+ch-26),'banco' if i['sku'].startswith('cons-') else 'alternativa',12,MUTED)
  if not inventory:txt(draw,(1757,145),'Nessuna alternativa residua.',16)
  txt(draw,(55,1504),'* Riferimenti da altri SET: '+(', '.join(i['sku'] for i in borrowed) if borrowed else 'nessuno'),14)
  txt(draw,(55,1533),'Fold e UTG dedicato esclusi. V17: etichette corrette editorialmente; nessun pinout o allineamento cover/camere certificato.',14,MUTED)
  txt(draw,(55,1560),name+'  •  coordinate e provenienza: composition-manifest.json',13,MUTED)
  canvas.convert('RGB').save(O/name,optimize=True)
  record={'file':name,'pair':pair,'variant':v+1,'variantCount':n,'selected':{k:source_path(i) for k,i in selected.items()},'borrowed':[source_path(i) for i in borrowed],'ownedInventory':[source_path(i) for i in inventory],'placements':placements,'physicalCompatibilityVerified':False,'visualReview':'PENDING','sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()};records.append(record)
  print(name,flush=True)
coverage={source_path(i):sum(any(p['file']==source_path(i) for p in rec['placements']) for rec in records if i['set'] in rec['pair']) for i in active}
assert all(coverage.values());assert not any(p['sku'] in ['disp-fold','glass-utg'] for rec in records for p in rec['placements'])
manifest={'version':17,'createdCount':len(records),'fixedCountRequirementSuperseded':8,'countPolicy':'Per pair, max distinct variants of a principal role. No Cartesian expansion; not a compatibility matrix.','families':family,'excludedSku':['disp-fold','glass-utg'],'activeSkuCount':len(set(i['sku'] for i in active)),'activeAssetCount':len(active),'pairOwnedCoverage':coverage,'compositions':records}
(O/'composition-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# Embedded offline gallery: all previews function in a network-disabled file viewer.
cards=[]
for rec in records:
 im=Image.open(O/rec['file']);im.thumbnail((1650,1200));bio=io.BytesIO();im.save(bio,'JPEG',quality=86);src='data:image/jpeg;base64,'+base64.b64encode(bio.getvalue()).decode()
 cards.append(f'<article data-pair="{rec["pair"][0]}"><h2>SET {rec["pair"][0]:02d} + {rec["pair"][1]:02d} · variante {rec["variant"]}/{rec["variantCount"]}</h2><img loading="lazy" src="{src}" alt="Esploso {rec["file"]}"><p>{rec["file"]} · PNG originale incluso nella cartella finals</p></article>')
options=''.join(f'<option value="{p["sets"][0]}">SET {p["sets"][0]:02d} + {p["sets"][1]:02d} ({p["count"]})</option>' for p in family)
page='''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SET Lab — composizioni V17</title><style>body{margin:0;background:#edf0eb;color:#193329;font:16px system-ui}header{padding:32px 5vw;background:#193329;color:#edf0eb}h1{font-size:38px;margin:12px 0}header p{max-width:1000px;line-height:1.6}nav{position:sticky;top:0;padding:15px 5vw;background:#dfe7da;z-index:2}select{font:inherit;padding:10px;border:1px solid #8c9e8b;border-radius:8px;background:#fff}main{padding:10px 3vw}article{margin:28px 0 44px}h2{font-size:21px}img{width:100%;height:auto;border-radius:10px}article p{font-size:13px;color:#667970}button{padding:10px;font:inherit;cursor:pointer}footer{padding:30px 5vw}</style><header><div>SET LAB / V17</div><h1>29 esplosi. Otto coppie, nessun totale imposto.</h1><p>Varianti determinate dai componenti di ogni coppia. Display fold e vetro UTG dedicato esclusi. 150 asset attivi / 147 SKU. Le alternative e i consumabili sono separati; i riferimenti presi da altri SET sono marcati con *. Composizioni illustrative, non telefoni collaudati.</p></header><nav><label>Coppia di SET <select id="filter"><option value="all">Tutte le coppie (29 immagini)</option>'''+options+'''</select></label></nav><main>'''+''.join(cards)+'''</main><footer>Coordinate pixel, rotazioni, provenienza e hash in composition-manifest.json. Correzioni V17 documentate in CONSEGNA-COMPOSIZIONI.md. I preview sono incorporati e funzionano offline.</footer><script>document.querySelector('#filter').addEventListener('change',e=>document.querySelectorAll('article').forEach(a=>a.hidden=e.target.value!=='all'&&a.dataset.pair!==e.target.value));</script></html>'''
(O/'viewer.html').write_text(page)
# Review contact sheets of the actual finished compositions, outside Git.
for fam in family:
 recs=[c for c in records if c['pair']==fam['sets']];cols=2;thumb=(880,640);sheet=Image.new('RGB',(cols*880,math.ceil(len(recs)/cols)*675),'#d5dcd2');dd=ImageDraw.Draw(sheet)
 for j,rec in enumerate(recs):
  im=Image.open(O/rec['file']);im.thumbnail(thumb);x=(j%cols)*880;y=(j//cols)*675;sheet.paste(im,(x,y));txt(dd,(x+10,y+642),rec['file'],18)
 sheet.save(R/f'analysis/finals-review-{fam["sets"][0]:02d}.jpg',quality=90)
print('TOTAL',len(records),'coverage',len(coverage),'active SKU',manifest['activeSkuCount'])
