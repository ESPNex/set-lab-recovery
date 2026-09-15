from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json
meta=[]
for f in sorted(Path('new_raw').glob('set10-*.png')):
 im=Image.open(f).convert('RGBA');a=np.array(im).astype(np.float32);rgb=a[:,:,:3];r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
 excess=np.minimum(r,b)-g
 eligible=(r>100)&(b>100)&(excess>35)
 t=np.clip((excess-35)/75,0,1);key=np.where(eligible,t*t*(3-2*t),0)
 alpha=a[:,:,3]*(1-key)
 # Reduce magenta spill at partially keyed edges only. Not flood fill or rembg.
 fringe=eligible&(alpha>0)&(alpha<254)
 rgb[:,:,0]=np.where(fringe,np.minimum(r,g+30),r)
 rgb[:,:,2]=np.where(fringe,np.minimum(b,g+30),b)
 a[:,:,3]=alpha;a[alpha<3,3]=0
 # Despill only within a 2px band next to transparent pixels; retain the existing alpha.
 edge=np.array(Image.fromarray(np.uint8((a[:,:,3]==0)*255)).filter(ImageFilter.MaxFilter(5)))>0
 pink=(np.minimum(a[:,:,0],a[:,:,2])-a[:,:,1]>15)&edge&(a[:,:,3]>0)
 spill=np.maximum(0,np.minimum(a[:,:,0],a[:,:,2])-a[:,:,1])
 a[:,:,0]=np.where(pink,a[:,:,0]-spill,a[:,:,0]);a[:,:,2]=np.where(pink,a[:,:,2]-spill,a[:,:,2])
 a[a[:,:,3]==0,:3]=0
 out=Image.fromarray(np.uint8(np.clip(a,0,255)),'RGBA');out.save('generated/'+f.name)
 bbox=out.getbbox();meta.append(dict(file=f.name,sourceSize=list(im.size),crop=list(bbox),alphaExtrema=list(out.getchannel('A').getextrema()),partialAlphaPixels=int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum()),transparentPixels=int((a[:,:,3]==0).sum()),method='global RGB chroma-key, smoothstep alpha, 2px edge despill; no rembg/flood-fill',provenance='AI-generated; alpha produced in postprocessing'))
sheet=Image.new('RGB',(1500,760),'#b6c2cc');d=ImageDraw.Draw(sheet)
for i,m in enumerate(meta):
 im=Image.open('generated/'+m['file']);im=im.crop(im.getbbox());im.thumbnail((280,320));x=(i%5)*300+(300-im.width)//2;y=(i//5)*380;sheet.paste(im,(x,y),im);d.text(((i%5)*300+5,y+340),m['file'],fill='black')
sheet.save('analysis/set10.jpg');Path('analysis/set10-metadata.json').write_text(json.dumps(meta,indent=2))
print(json.dumps(meta,indent=2))
