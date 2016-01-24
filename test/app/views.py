from app import app
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
from forms import TwoDcodeForm
from config import src_TwoDcode, src_hosts, url_hosts
import qrcode
import datetime, time
import os
import urllib2
import re
from PIL import Image, ImageDraw, ImageFont


@app.route('/')
def index():
    return render_template('index.html');

@app.route('/Kun WANG')
def kun():
    return render_template('kun2.html', name="Kun WANG");

@app.route('/Shikun CHEN')
def shikun():
    return render_template('shikun2.html', name="Shikun CHEN");

@app.route('/Yu LOU')
def yu():
    return render_template('yu.html', name="Yu LOU");

@app.route('/Zhuoyu GUO')
def zhuoyu():
    return render_template('zhuoyu.html', name="Zhuoyu GUO");

@app.route('/daojishi')
def daojishi():
    return render_template('daojishi.html', name="Daojishi");

@app.route('/visit_google', methods = ['GET', 'POST'])
def google():
    form = TwoDcodeForm(csrf_enabled=False)
    if form.submit_gethosts.data:
        res = main_hosts(src_hosts)
        if res != 0:
            if res == -1:
                print "Invalid url!"
            elif res == -2:
                print "Hosts not found!"
        else:
            dirpath = src_hosts[:-5]
            return send_from_directory(dirpath, filename='hosts', as_attachment=True)

    return render_template('get_hosts.html', name="Change Hosts", form=form);

def write_hosts(f):
    '''Try to get hosts file content from the Internet.
returns -1 if url is no longer valid
        -2 if no hosts found
        -3 if open file error
         0 otherwise'''
    try:
        response = urllib2.urlopen(url_hosts)
    except:
        return -1
    
    start = False
    while True:
        line = response.readline()
        if line == '':
            return -2
        if start == False and "#google" in line and "hosts" in line:
            start = True
            f.write("#google hosts begin\n")
            continue
        if start == True:
            line = line.replace("&nbsp;", "")
            line = re.sub("<[^>]+>", "", line)
            f.write(line)
        if start == True and "#google" in line and "hosts" in line:
            start = False
            return 0
            
def main_hosts(f_name):
    lines = []
    try:
        with open(f_name, 'w') as f:
            for line in lines:
                f.write(line)
            return write_hosts(f)
    except:
        return -3


@app.route('/TwodimentionCode <imgname> <info_2dcode>' , methods = ['GET', 'POST'])
def TwodimentionCode(imgname="logo.png", info_2dcode=''):
    form = TwoDcodeForm(csrf_enabled=False)
    imgfile = "../static/img/TwoDcode/" + imgname

    if form.validate_on_submit():
        if form.submit_commit.data:
            message = form.message_TwoDcode.data
            date_now = datetime.datetime.now()
            data_time = str(date_now).replace(":","_")
            now = data_time.replace(" ","_")
            #now = now.replace('-','')
            filename = src_TwoDcode + now+".jpg"
            flag = TwoDcode_Generate(message, filename)
            if not flag:
                imgfile = "../static/img/TwoDcode/"+now+".jpg"
                imgname = now+".jpg"
            info_2dcode = message.replace('://','++')
            return redirect(url_for('TwodimentionCode',imgname = imgname, info_2dcode=info_2dcode))
    else:
        if info_2dcode == '*':
            form.message_TwoDcode.data = ''
        else:
            info_2dcode = info_2dcode.replace('++','://')
            form.message_TwoDcode.data = info_2dcode

    if form.submit_download.data:
        if imgname != "logo.png":
            return send_from_directory(src_TwoDcode, filename=imgname, as_attachment=True)
            
    return render_template('erweima.html', name="Two Dimention Code", form = form, 
                            imgfile=imgfile)



def TwoDcode_Generate(message, savepath):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=4)


        #qr.add_data("http://jump.baidu.com/")
        qr.add_data(str(message))

        qr.make(fit=True)
        img = qr.make_image()
        filename = savepath
        img.save(filename)  
        return 0
    
    except:
        return 1
    
