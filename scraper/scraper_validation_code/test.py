import requests
from PIL import Image
from PIL import ImageOps
from io import BytesIO
import numpy as np
import os

# import Image

img_size=32,32

def cut_img(img,t):
     img2 = img.crop((t[0], t[1], t[2], t[3]))
     img = ImageOps.expand(img2,border = 5,fill =255)
     # print(size(img))
     img2 = img.crop((0, 5, 39, 44))
     return img2

for x in range(50):
     t=[3,0,34,40]
     src=''
     src=src.join(['photo\\img',str(x),'.jpg'])
     print(src)
     path=''
     path=path.join(['test\\testimg',str(x)])
     try:
          os.mkdir(path,777)
     except:
          pass
     img = Image.open(src)
     img_gray = img.convert('L')
     img_two = img_gray.point(lambda x: 255 if x > 140 else 0)
     # img_two.show()
     for y in range(4):
          # print(path)
          imgpath=''
          imgpath=imgpath.join([path,'\\',str(y),'.jpg'])
          print(imgpath)
          n_img = cut_img(img_two,t)
          t[0] = t[2]
          t[2] = t[2]+28
          n_img= n_img.resize(img_size)
          n_img.save(imgpath,"JPEG")