from PIL import Image
from pathlib import Path
import json,base64,io
meta=json.loads(Path('analysis/metadata.json').read_text()); items=[]
boards=['set01-pcb-bare.png','set03-board-pro.png','set05-board-lite.png']
# Coordinates measured visually in the alpha-cropped board raster; not physical dimensions.
slots={0:{'soc':(139,244,158,157),'ram':(129,449,174,114),'sto':(356,350,132,157)},1:{'soc':(520,203,226,239),'ram':(786,184,119,123),'sto':(786,342,119,121)},2:{'soc':(470,158,327,328)}}
for m in meta:
 name=m['file'];pair=(int(name[3:5])-1)//2; im=Image.open('originals/'+name).convert('RGBA'); crop=m['bbox']; note='Componente esterno: collocazione esplosa, connessione non determinabile dall’immagine.'
 if name=='set01-usb-flex.png':
  # Original includes two disconnected opaque white side panels; retain the central component only in preview.
  import numpy as np
  a=np.array(im); mask=(a[:,:,3]>0)&(a[:,:,:3].min(2)<210); ys,xs=np.where(mask); crop=[int(xs.min())-2,int(ys.min())-2,int(xs.max())+3,int(ys.max())+3];note+=' Ritaglio centrale: escluse bande bianche laterali; originale intatto.'
 im=im.crop(crop);cw,ch=im.size; im.thumbnail((1400,1400));b=io.BytesIO();im.save(b,format='WEBP',quality=90)
 role=next((r for r in ['soc','ram','sto'] if '-'+r+'-' in name),'external');board=name in boards
 item=dict(id=name,pair=pair,role='board' if board else role,sourceSize=m['size'],alphaBBox=m['bbox'],crop=crop,aspect=cw/ch,src='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode(),angle=0,z=10,visible=True,note=note)
 items.append(item)
for p in range(3):
 group=[i for i in items if i['pair']==p];board=next(i for i in group if i['role']=='board');bw=600 if p==0 else 850;bx=90;by=180 if p==0 else 300;bh=bw/board['aspect'];board.update(x=bx+bw/2,y=by+bh/2,w=bw,h=bh,z=0,note='Raster di riferimento: origine locale nel vertice superiore sinistro del ritaglio alpha.',status='riferimento')
 scale=bw/(board['crop'][2]-board['crop'][0]);idx=0
 for i in group:
  if i==board:continue
  role=i['role'];slot=slots[p].get(role)
  if slot:
   x,y,w,h=slot;fw=min(w,h*i['aspect']);fh=fw/i['aspect'];i.update(x=bx+(x+w/2)*scale,y=by+(y+h/2)*scale,w=fw*scale,h=fh*scale,z=20,slot=dict(x=x,y=y,w=w,h=h),status='allineamento visivo',note='Allineamento al centro della piazzola; scala uniforme, proporzioni conservate. Pinout e compatibilità non verificati.'+(' Assegnazione RAM/UFS ipotizzata: serigrafia di gruppo, non univoca.' if p==1 and role!='soc' else ''))
   if ('ram-12' in i['id'] or 'soc-7g2' in i['id']): i['visible']=False
  else:
   col=idx%4;row=idx//4;w=min(125,130*i['aspect']);h=w/i['aspect'];i.update(x=1050+col*190,y=200+row*210,w=w,h=h,status='esploso / non localizzato');idx+=1
   if p==2 and role in ['ram','sto']:i['note']='Nessuna piazzola RAM/UFS identificabile sul lato mostrato. Nessun posizionamento sulla motherboard deducibile.'
  if p==2 and 'soc-q6' in i['id']:i['visible']=False
  if 'set04-soc-8e' in i['id']:i['note']+=' Il raster riporta Snapdragon 8 Gen 3, non 8 Elite.'
  if 'set04-soc-7g2' in i['id']:i['note']+=' Il raster riporta 7+ Gen 3, non 7 Gen 2.'
  if 'set06-soc-vertv2' in i['id']:i['note']+=' Il raster riporta Exynos 2400.'
  if 'set06-soc-q6' in i['id']:i['note']+=' Il raster riporta MediaTek Dimensity 8300-Ultra.'
  if 'set03-camf-32' in i['id']:i['note']+=' La stampa visibile indica 52MP, diversa dal suffisso del file.'
clean=[{k:v for k,v in i.items() if k!='src'} for i in items]
Path('coordinates.json').write_text(json.dumps({'units':'pixel logici del viewer, non mm','canvas':[1800,1200],'anchor':'centro del ritaglio, rotazione oraria in gradi','boardLocalSlots':'pixel raster ritagliato; prima di scala e traslazione','precision':'stime visive, nessuna validazione meccanica o elettrica','items':clean},ensure_ascii=False,indent=2))
Path('payload.json').write_text(json.dumps(items,ensure_ascii=False))
