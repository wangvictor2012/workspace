import qrcode
from PIL import Image
'''
def TwoDimentionCode(code_use, machinecode):
    qr1 = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0)
    qr2 = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=2)
    
    TDcode = str(machinecode) + " " + code_use
    qr1.add_data(TDcode)
    qr1.make(fit=True)
    img = qr1.make_image()

    
    w, h = img.size
    x_w = 55
    y_w = x_w*h/w  
    img = img.resize((x_w, y_w))
    
    
    filename = "D://"+code_use+"(3).jpg"
    img.save(filename)

    TDcode = str(machinecode) + " " + code_use
    qr2.add_data(TDcode)
    qr2.make(fit=True)
    img = qr2.make_image()

    
    filename = "D://"+code_use+"(4).jpg"
    img.save(filename)
'''

def TwoDimentionCode(code_use, machinecode):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=2,
        border=4)
    TDcode = "r.flcnc.com/" + str(machinecode) + "-" + code_use
    qr.add_data(TDcode)
    qr.make(fit=True)
    img = qr.make_image()
    '''
    w, h = img.size
    x_w = 56
    y_w = x_w*h/w  
    img = img.resize((x_w, y_w))
    '''
    #filename = "/var/www/qrcode/app/static/img/"+code_use+".jpg"
    filename = "D://"+code_use+".jpg"
    img.save(filename)

machinecode = 'F1100'
x=['1','2','3','4','5','6','7','9','A','B','C','D','E','F']
for i in x:
    #code_use = 'B02-24E5500' + i
    TwoDimentionCode('B01-100000010', 'F2100B')
