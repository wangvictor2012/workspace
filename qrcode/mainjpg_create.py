# -*- coding: utf-8 -*-
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=15,
    border=1)

qr.add_data("*010-24DE900B*")
qr.make(fit=True)
img = qr.make_image()
filename = "main.jpg"
#size = 200 * 92
'''
w, h = img.size  
img = img.resize((w/5, h/5))
im = Image.new("RGBA", (300,140), (256,256,256))
txt1 = "上海方菱"
txt2 = "型  号: F3500"
txt3 = "序列号: *010-24DE900B*"
font1 = ImageFont.truetype('simsun.ttc',20)
font2 = ImageFont.truetype('simsun.ttc',25)
draw = ImageDraw.Draw(im)
draw.ink = 0 + 0 * 256 + 0 * 256 * 256
draw.text((30,20), unicode(txt1,'UTF-8'), font = font2)
draw.text((30,60), unicode(txt2,'UTF-8'), font = font1)
draw.text((30,100), unicode(txt3,'UTF-8'), font = font1)
del draw
im.paste(img,(200,20), mask=None)
'''
im = Image.new("RGBA", (900,450), (256,256,256))
txt1 = "上海方菱"
txt2 = "型  号: "
txt3 = "序列号:  "
font1 = ImageFont.truetype('msyh.ttc',65)
font2 = ImageFont.truetype('msyh.ttc',75)
draw = ImageDraw.Draw(im)
draw.ink = 0 + 0 * 256 + 0 * 256 * 256
draw.text((90,60), unicode(txt1,'UTF-8'), font = font2)
draw.text((90,175), unicode(txt2,'UTF-8'), font = font1)
draw.text((90,290), unicode(txt3,'UTF-8'), font = font1)
del draw

w, h = img.size  
img = img.resize((w/2, h/2))

#im.paste(img,(590,70), mask=None)

im.save(filename) 
#im.show()

