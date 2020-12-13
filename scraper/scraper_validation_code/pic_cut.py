import requests
from PIL import Image
from io import BytesIO
import time
import numpy as np

def cut_img(img,size):
     img2 = img.crop((0, 0, 30, 40))
     img2.show()
     return img2


f = [0,0]
e = [30,40]
t = tuple(f)+tuple(e)
url = "https://nportal.ntut.edu.tw/authImage.do"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'}
# print(r.content)
# r.encoding = 'ISO-8859-1'
for j in range(1): 
    try:
        r = requests.get(url , headers)
        i  = Image.open(BytesIO(r.content))
        imgname=''
        imgname=imgname.join(['canuse\img',str(j),'.jpg'])
        print(type(i))
        # i.save(imgname)
        for x in range(4):
            imgname=''
            print('here')
            imgname=imgname.join(['canuse\testimg',str(j),str(x),'.jpg'])
            print('here')
            n_img = Image.open(cut_img(i,t))
            f[0] = e
            e[0] = e[0]+30
            t = tuple(f)+tuple(e)
            print(type(n_img))
            n_img.save(imgname)

        time.sleep(2)
    except:
        print('something wrong')
        time.sleep(5)
