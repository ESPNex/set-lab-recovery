from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
r=Path(__file__).parent;d=json.loads((r/'coordinates-v16.json').read_text());changes=[]
def font(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
for name in ['set03-camf-32.png','set06-ram-16.png','set10-th-gr2.png','set12-soc-d8300.png']:
 i=next(i for i in d['items'] if i['file']==name);p=r/('originals' if i['set']<=6 else 'generated')/name;oldhash=hashlib.sha256(p.read_bytes()).hexdigest();im=Image.open(p).convert('RGBA');x,y,xx,yy=i['crop'];c=im.crop((x,y,xx,yy));dr=ImageDraw.Draw(c)
 if 'camf' in name:
  dr.rectangle((54,231,148,250),fill=(99,62,23,255));dr.text((57,232),'32 MP AF',font=font(16),fill=(240,231,210,255))
 elif 'ram-16' in name:
  dr.rounded_rectangle((48, 60,c.width-40,c.height-35),radius=12,fill=(43,44,44,255))
  for text,cy,n in [('SK hynix',100,48),('16 GB',190,44),('LPDDR5X',275,42),('9600 MHz',365,38)]:
   f=font(n);box=dr.textbbox((0,0),text,font=f);dr.text(((c.width-(box[2]-box[0]))/2,cy),text,font=f,fill=(192,194,190,255))
 elif 'th-gr2' in name:
  # Remove only the upper protruding third panel; retain rear-left/bottom and front panel.
  c.paste((0,0,0,0),(0,0,c.width,60))
 else:
  sample=c.crop((90,90,230,120))
  for box in [(330,51,453,87),(196,319,450,429)]:c.paste(sample.resize((box[2]-box[0],box[3]-box[1])),box[:2])
 im.paste(c,(x,y));im.save(p);oldcrop=i['crop'];bbox=im.getchannel('A').getbbox();i['crop']=list(bbox)
 if list(bbox)!=oldcrop and i.get('size'):
  w,h=bbox[2]-bbox[0],bbox[3]-bbox[1];prev=i['size'];s=min(prev[0]/w,prev[2]/h);i['size']=[w*s,prev[1],h*s]
 i['editorialCorrection']='Deterministic visible label/panel correction V17; AI source identity preserved; not manufacturer artwork.';changes.append({'file':str(p.relative_to(r)),'previousSha256':oldhash,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':i['editorialCorrection']})
for i in d['items']:
 if i['sku'] in ['disp-fold','glass-utg']:i['excludedFromFinals']=True;i['exclusionReason']='User removed fold configuration; UTG dedicated companion excluded.'
d['version']=17;d['status']='ACTIVE_NON_FOLD_COMPOSITIONS';(r/'coordinates-v17.json').write_text(json.dumps(d,ensure_ascii=False,indent=2));manifest={str((Path('originals') if i['set']<=6 else Path('generated'))/i['file']):hashlib.sha256((r/('originals' if i['set']<=6 else 'generated')/i['file']).read_bytes()).hexdigest() for i in d['items']};(r/'asset-sha256-v17.json').write_text(json.dumps(manifest,indent=2));(r/'analysis/v17-editorial-corrections.json').write_text(json.dumps(changes,indent=2))
# Review composite against neutral background.
canvas=Image.new('RGB',(1400,580),(232,234,232));dr=ImageDraw.Draw(canvas)
for k,c in enumerate(changes):
 i=next(i for i in d['items'] if i['file']==Path(c['file']).name);im=Image.open(r/c['file']).crop(i['crop']);im.thumbnail((330,500));canvas.paste(im,(k*350+(350-im.width)//2,60),im);dr.text((k*350+8,20),i['file'],font=font(16),fill='black')
canvas.save(r/'analysis/v17-corrections-review.jpg')
