import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
im=cv2.imread('/home/claude/trimion-site/tools/src/og.jpg')
x0,y0,x1,y1=388,490,600,535
reg=im[y0:y1,x0:x1]
g=cv2.cvtColor(reg,cv2.COLOR_BGR2GRAY)
m=(g>90).astype(np.uint8)*255
m=cv2.dilate(m,np.ones((5,5),np.uint8))
mask=np.zeros(im.shape[:2],np.uint8);mask[y0:y1,x0:x1]=m
out=cv2.inpaint(im,mask,6,cv2.INPAINT_TELEA)
pil=Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGR2RGB))
d=ImageDraw.Draw(pil)
F='/usr/share/fonts/truetype/google-fonts/Poppins-'
fb=ImageFont.truetype(F+'Bold.ttf',19);fm=ImageFont.truetype(F+'Medium.ttf',17)
d.text((398,487),'R150 delivery',font=fb,fill=(255,255,255))
d.text((398,512),'1-year warranty',font=fb,fill=(248,183,63))
pil.save('/home/claude/trimion-site/tools/og-full.jpg',quality=88,optimize=True,progressive=True)
pil.crop((0,380,800,630)).save('og_check.png')
import os;print(os.path.getsize('/home/claude/trimion-site/tools/og-full.jpg'))
