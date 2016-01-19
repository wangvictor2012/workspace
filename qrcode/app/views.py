# -*- coding: UTF-8 -*-
from flask import render_template, flash, redirect, request, url_for, g
from flask.ext.login import login_required, login_user, current_user, logout_user
from PIL import Image, ImageDraw, ImageFont
from forms import DcodeForm, UserForm, BomForm, BomForm_Edit
from app import app, login_manager, db, models, TypecodeIndex
from config import SQLSERVER_HOST, SQLSERVER_PORT, SQLSERVER_USER, SQLSERVER_PASS, SQLSERVER_DB, ImagefileSrc, JsTypecodeIndexSrc, JsMaterialSerialIndexSrc, JsERPinfoSrc
import qrcode
import MySQLdb
import datetime, time
import pymssql
import sys
import os
import shutil
import re

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def begin():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserForm()
    cursor = db.cursor()
    if form.validate_on_submit() or form.submit.data:
        if form.submit.data:
            username = form.username.data
            password = form.password.data
            user = models.User.query.filter_by(name = str(username)).first()
                
            if user:
                if str(password)=='123456':
                    
                    try:
                        src = ImagefileSrc
                        Material_serial_Index()
                        for item in os.listdir(src):
                            os.remove(src+item)
                        login_user(user)
                    except:
                        login_user(user)
                    return redirect(url_for('index', machinecode='+', flag_return=0,version_info='init', remark_info='x'))
                else:
                    flash(encodechinese("密码输入错误，请重新输入！"))
            else:
                flash(encodechinese("用户名输入错误，请重新输入！"))

    return render_template('login.html', form = form)


@app.route('/index/<version_info> <machinecode> <int:flag_return> <remark_info>', methods = ['GET', 'POST'])
@login_required
#flag_return: 0:查询按钮提交后结果（未选择产品） 1, 正常程序; 2, 询问是否注册，返回是; 3, 已注册返回标志
def index(version_info='init',machinecode='+', flag_return=0,  remark_info=''):
    form = DcodeForm()
    img = ''
    code = ''
    filenamex = '/static/img_system/main.jpg'
    user = ''
    code_input = ''
    flag_register = 0
    datainfo = [] 
    typedata = ''
    cursor = db.cursor()
    code_use = ''
    partname = ''

    rights = g.user.rights
    if '1' in str(rights):
        flag_edit = 'Yes'
    else:
        flag_edit = 'No'

    sql = "SELECT * FROM product_sub_partname"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        typedata = typedata + " " + str(row[0])
    
    if form.submit.data or machinecode != '+':
        
        code = str(request.form.get('select_info'))
        code_input = code
        if len(code) > 0 and code != 'None':
            machinecode_return = code
            searchname = '%'+code+'%'
            sql = "SELECT * FROM product_sub_partname \
                    WHERE sub_partname like '" + searchname + "'"
            cursor.execute(sql)
            results = cursor.fetchall()
        else:
            machinecode_return = machinecode

        if form.submit.data:
            return redirect(url_for('index',machinecode=machinecode_return, flag_return=0, version_info='init', remark_info='NULL'))

        elif machinecode != '+' and not form.submit.data and flag_return!=0:
            if len(code) > 0 and code != 'None':  
                machinecode = code_input
            else:
                code_input = machinecode

            sql = "SELECT * FROM product_sub_partname \
                    WHERE sub_partname = '%s'" % (machinecode)
            cursor.execute(sql)
            results_machine = cursor.fetchall()

            if len(results_machine)>0:

                #sqlx = "SELECT * FROM product_records order by product_produce_date desc limit 1"
                sqlx = "SELECT * FROM product_records order by product_serial desc limit 1" 
                cursor.execute(sqlx)
                list_date = cursor.fetchall()
                date_use = list_date[0][0]

                date_now = datetime.datetime.now()
                x=str(date_now).find(' ')
                now = str(date_now)[:x]
                now = now.replace('-','')
                now = now[2:]
                hex_now = hex(int(now))[2:].upper()
                if hex_now == date_use[:-3]:
                    if flag_return != 3:
                        num = hex(int(date_use[-3:],16)+1)
                    else:
                        num = hex(int(date_use[-3:],16))

                    if len(num)==3:
                        num_use='00'+num[2:]
                    elif len(num)==4:
                        num_use='0'+num[2:]
                    else:
                        num_use = num[2:]
                    code_use = str(machinecode)[-3:]+'-'+date_use[:-3]+num_use
                else:
                    code_use = str(machinecode)[-3:]+'-'+hex_now+'001'
                
                partname = findpartname(results_machine[0][2])
                code_use = code_use.upper()
                filenamex = TwoDimentionCode(code_use, partname)

                results = results_machine

            else:
                partname = "!ERROR!"
                code_use = "!WRONG_RESULT!"
                
        elif flag_return == 0:
            if machinecode != '+':
                code_input = machinecode
                searchname = '%'+machinecode+'%'
                sql = "SELECT * FROM product_sub_partname \
                        WHERE sub_partname like '" + searchname + "'"
                cursor.execute(sql)
                results = cursor.fetchall()
            
    if len(results)>0:
        i = 1
        for row in results:
            partnamex = findpartname(int(row[2]))
            sql = "SELECT * FROM bom_index \
                        WHERE subname = '%s'" %(row[0])
            cursor.execute(sql)
            results_bom = cursor.fetchall()

            if version_info == 'init' and flag_return == 0:
                if len(results_bom)>0:
                    for j in range(len(results_bom)):
                        mark = str(row[1]) + ' ## DIFFERENCE:  ' + str(results_bom[j][7])
                        info = [str(i), row[0], results_bom[j][2], partnamex, mark]
                        datainfo.insert(len(datainfo),info)
                        i+=1
                else:
                    info = [str(i), row[0], '1.0', partnamex, row[1]]
                    datainfo.insert(len(datainfo),info)
                    i+=1
            else:
                info = [str(i), row[0], version_info, partnamex, row[1]]
                datainfo.insert(len(datainfo),info)
                i+=1
    
    if request.form.get("register"):
        #print code_input, machinecode
        if filenamex == '/static/img_system/main.jpg' or flag_return==0:
            #flash(encodechinese("请在列表中选择您想注册的产品!"))
            flag_register = 4 # 示例照片，不能注册

        elif flag_return == 3:
            flag_register = 5 # 重复注册

        else:
            flag_register = 1 # 正常注册

    if flag_return == 2:
        try:
            sql = "INSERT INTO product_records(product_serial, product_subname, product_produce_date, product_producer, product_comment) \
                VALUES ('%s', '%s', '%s', '%d', '%s')" % (code_use[4:], machinecode, str(date_now)[:-7], int(g.user.id), encodechinese(remark_info[1:]))
            cursor.execute(sql)
            db.commit()
            flag_register = 2 # 注册成功，是否打印
        except:
            flag_register = 3 # 注册失败

    cursor.close()
        
    remark_use = encodechinese(form.remark.data)
    s = remark_use.splitlines()
    x = 'x'
    for line in s:
        x = x + line + ' ' 

    if version_info!='init' and flag_return<2:
        if x.find('xNULL')>=0:
            x = 'Version:'+version_info
        else:
            comp = 'Version:'+version_info
            re_find = re.findall(r"Version:[\d+]\.[\d+]",x)
            if len(re_find)>0:
                if re_find[0] != comp:
                    x = re.sub(r"Version:[\d+]\.[\d+]",comp, x)
            else:
                x = comp + "_" + x
        form.remark.data = x

    elif flag_return>=2:
        form.remark.data = remark_info
        x = remark_info[1:]
  
    return render_template('index.html', flag = "index", remark_info = x, partname = partname, code_use=code_use,
                           form = form, username = str(g.user.name), flag_edit = flag_edit, version_info = version_info,
                           img = 1, flag_register = flag_register,
                           filename = filenamex,typedata = typedata,
                           datainfo = datainfo, code_input = code_input)


def TwoDimentionCode(code_use, machinecode):
    #code_use = 'B06-24E5402F'
    #machinecode = 'F2500B'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=2,
        border=4)
    TDcode ="http://r.flcnc.com/" + str(machinecode) + "-" + code_use
    qr.add_data(TDcode)
    qr.make(fit=True)
    img = qr.make_image()
    
    filename = ImagefileSrc+code_use+".jpg"
    #filename = "D://Etudiant//Test//qrcode//app//static//img//"+code_use+".jpg"
    img.save(filename)

    filenamex = '/static/img/'+code_use+'.jpg'

    return filenamex

def encodechinese(chinese):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if len(str(chinese))>4:
        return chinese.encode('utf-8')
    else:
        return 'NULL'

def findpartname(id):
    cursor = db.cursor()
    sql = "SELECT * FROM product_partname \
                    WHERE id = '%d'" % (int(id))
    cursor.execute(sql)
    partname = cursor.fetchall()
    cursor.close()
    if len(partname)>0:
        return partname[0][1]
    else:
        return 'ERROR!'

@app.route('/logout')
@login_required
def logout():
    try:
        cursor = db.cursor()
        typedata = ''
        #f=open('./app/static/js/TypecodeIndex.js','r+')
        f=open(JsTypecodeIndexSrc,'r+')
        cc = f.read()
        TypecodeIndex_num = cc.count(' ') - 3

        sql = "SELECT COUNT(*) FROM product_records"
        cursor.execute(sql)
        results = cursor.fetchall()

        Num_total = int(str(results[0])[1:-3])
        if Num_total > TypecodeIndex_num:
            num = Num_total - TypecodeIndex_num
            sql = "SELECT * FROM product_records LIMIT " + str(TypecodeIndex_num) + "," + str(num)
            
            cursor.execute(sql)
            results = cursor.fetchall()
            
            for row in results:
                typedata = typedata + " " + str(row[0])

            content = typedata + "';"
            
            f.seek(-2,2)
            f.write(content)
        f.close()
        logout_user()

    except:
        logout_user()

    return redirect(url_for('login'))



@app.route('/search/<machinecode> <int:page>', methods = ['GET', 'POST'])
@login_required
def search(machinecode, page=1):
    form = DcodeForm()
    img = ''
    code = ''
    filenamex = '/static/img_system/main.jpg'
    user = ''
    code_input = ''
    flag_register = 0
    flag_page = 0
    datainfo = []
    typedata = ''
    cursor = db.cursor()
    PAGE_NUM = 100
    page_total = 1   
    prev = False
    nextv = False
    partname = ''
    code_use = ''

    rights = g.user.rights
    if '1' in str(rights):
        flag_edit = 'Yes'
    else:
        flag_edit = 'No'

    f=open(JsTypecodeIndexSrc,'r')
    cc = f.read()
    TypecodeIndex_num = cc.count(' ') - 3
    f.close()

    sql = "SELECT COUNT(*) FROM product_records"
    cursor.execute(sql)
    resultsx = cursor.fetchall()
    Num_total = int(str(resultsx[0])[1:-3])
    
    if Num_total > TypecodeIndex_num:
        num = Num_total - TypecodeIndex_num
        sql = "SELECT * FROM product_records LIMIT " + str(TypecodeIndex_num) + "," + str(num)
        
        cursor.execute(sql)
        resultsx = cursor.fetchall()
        
        for row in resultsx:
            typedata = typedata + " " + str(row[0])

    if Num_total%PAGE_NUM == 0:
        page_max = Num_total/PAGE_NUM 
    else:
        page_max = Num_total/PAGE_NUM + 1

    page_total = page_max
    datastart = Num_total-page*PAGE_NUM
    if datastart>=0:
        sql = "SELECT * FROM product_records LIMIT " + str(datastart) + "," + str(PAGE_NUM)
    else:
        dataleft = Num_total%PAGE_NUM
        sql = "SELECT * FROM product_records LIMIT 0," + str(dataleft)

    cursor.execute(sql)
    results = cursor.fetchall()

    #print Num_total, TypecodeIndex_num, typedata

    if form.submit.data or machinecode != '+':
        code = str(request.form.get('select_info'))
        code_input = code
        if len(code) > 0 and code != 'None': 
    
            sql = "SELECT * FROM product_records \
                    WHERE product_serial = '%s'" %(code)

            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results)>0:
                subname = results[0][1]
                code_use = subname[-3:] + "-" + results[0][0]
                sql = "SELECT * FROM product_sub_partname \
                    WHERE sub_partname = '%s'" % (subname)
                cursor.execute(sql)
                spartname = cursor.fetchall()
                if len(results)>0:
                    partname = findpartname(spartname[0][2])    

            if form.submit.data:
                return redirect(url_for('search',machinecode=code, page=page))
        
        if machinecode != '+' and len(results)>0: 
            if form.submit.data and len(code) >0 and code != 'None': 
                machinecode = code
            
            sql = "SELECT * FROM product_records \
                    WHERE product_serial = '%s'" % (machinecode)
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results)>0:
                subname = results[0][1]
                code_use = subname[-3:] + "-" + results[0][0]
                sql = "SELECT * FROM product_sub_partname \
                        WHERE sub_partname = '%s'" % (subname)
                cursor.execute(sql)
                spartname = cursor.fetchall()
                if len(results)>0:
                    partname = findpartname(spartname[0][2])
                else:
                    partname = "TEST_ERROR"

                filenamex = TwoDimentionCode(code_use, partname)

            code_input = machinecode
            if form.submit.data:
                filenamex = '/static/img_system/main.jpg'
    

    if form.submitpage.data and form.inputpage.data:
        if form.inputpage.data <= page_max:
            return redirect(url_for('search', machinecode='+', page=form.inputpage.data))
        else:
            flag_page = 1#页码超过指定范围
               
    if len(results)>0:
        prev = True
        nextv = True
        if page==1:
            prev = False
            
        if page == page_total:
            nextv = False

        for x in range(len(results)):
            if len(results)==1:
                pp=1
            else:
                pp = Num_total -(page-1)*PAGE_NUM - x
            index = len(results)-x -1
            sql = "SELECT * FROM user_table \
                   WHERE id = '%d'" % (results[index][3])
            cursor.execute(sql)
            user_search = cursor.fetchall()
            info = [str(pp), results[index][0], results[index][1], user_search[0][1], results[index][2], results[index][4]]
            datainfo.insert(len(datainfo),info)

    if code != '':
        page_total = 1
        page = 1
        prev = False
        nextv = False

    if form.print_button.data:
        if filenamex == '/static/img_system/main.jpg':
            flag_register = 10
        else:
            flag_register = 11

    cursor.close()
    
    return render_template('index.html', flag = "search",partname = partname, code_use = code_use,
                           form = form, username = str(g.user.name), flag_edit = flag_edit,
                           img = 1, flag_register = flag_register,
                           filename = filenamex,typedata = typedata,
                           datainfo = datainfo, code_input = code_input,
                           page_total = page_total, prev = prev, nextv=nextv,
                           pagenow = page, flag_page = flag_page)


@app.route('/bominfo <product_flag> <code_search>', methods = ['GET', 'POST'])
@login_required
def bominfo(product_flag='#', code_search='+'):
    form = BomForm()
    cursor = db.cursor()
    table_product = []
    table_product_bom = []
    table_material = {}
    table_product_name = {}
    code_input = ''
    code = ''

    rights = g.user.rights
    if '1' in str(rights):
        flag_edit = 'Yes'
    else:
        flag_edit = 'No'

    conn=pymssql.connect(host=SQLSERVER_HOST,user=SQLSERVER_USER, password=SQLSERVER_PASS, database=SQLSERVER_DB, port=SQLSERVER_PORT, charset="UTF-8")
    cou=conn.cursor()
    if code_search != '+' and code_search != ' ':
        code = code_search
        code_input = code
    #产品列表初始化
    codex = str(request.form.get('select_info'))
    if not form.submit.data or (form.submit.data and (len(codex) ==0 or codex == 'None')):
        sql = "SELECT * FROM bom_index "
        cursor.execute(sql)
        results = cursor.fetchall()
        i = 1
        for rows in results:
            if rows[6] == 1:
                info_product = [i, rows[1], rows[2], rows[3], rows[5], rows[7], rows[0]]
                table_product.insert(len(table_product),info_product)
                i = i + 1
                name = rows[1]+'_'+rows[2]
                table = BomTabbleInfo(name, rows[4], rows[5], rows[0],cursor)
                table_product_name = dict(table_product_name.items()+table.items())
                bom_info = ERP_bomsearch(rows[0], cursor, cou)
                table_material=dict(table_material.items()+bom_info.items())
    #搜索产品
    if form.submit.data or code != '':
        if form.submit.data:
            code = str(request.form.get('select_info'))

        if len(code) > 0 and code != 'None':
            code_input = code
            table_product = [] 
            if '.' in code:
                sql = "SELECT * FROM bom_index \
                        WHERE erp_serial = '%s'" %(code)
            else:
                sql = "SELECT * FROM bom_index \
                        WHERE subname = '%s'" %(code)

            cursor.execute(sql)
            results = cursor.fetchall()
            i = 1
            for rows in results:
                if rows[6] == 1:
                    info_product = [i, rows[1], rows[2], rows[3], rows[5], rows[7], rows[0]]
                    table_product.insert(len(table_product),info_product)
                    i = i + 1
                    name = rows[1]+'_'+rows[2]
                    table = BomTabbleInfo(name, rows[4], rows[5], rows[0], cursor)
                    table_product_name = dict(table_product_name.items()+table.items())
                    bom_info = ERP_bomsearch(rows[0], cursor, cou)
                    table_material=dict(table_material.items()+bom_info.items())
        

    if code_input == '':
        code_input = ' '

    cursor.close()
    conn.close()
    return render_template('bominfo.html', flag = 'bominfo', form = form, flag_edit = flag_edit,
                            username = str(g.user.name), code_input = code_input, 
                            table_product = table_product, table_product_bom = table_product_bom,
                            table_product_name = table_product_name, table_material = table_material)

def BomTabbleInfo(name, producer, date, id, cursor):
    table_info = {}     
    sql = "SELECT * FROM user_table \
                    WHERE id = '%d'" %(int(producer))
    cursor.execute(sql)
    results = cursor.fetchall()
    table = [name, producer, date]
    for rows in results:
        table[1] = rows[1]
    table_info[id] = table

    return table_info

def ERP_bomsearch(x, cursor, cou):
    table_material = {}     
    sql = "SELECT * FROM bom_detail \
                    WHERE product_index = '%d' order by erp_material" %(int(x))
    cursor.execute(sql)
    results = cursor.fetchall()
    j = 1
    table_material_copy = []
    for rows in results:
        '''
        material = [j, rows[1], '', '', rows[2]]
        table_material_copy.insert(len(table_material_copy), material)
        j = j + 1
        '''
        sql="select * from dbo.t_ICItemCore where FNumber = '%s'" %(str(rows[1]).strip())
        cou.execute(sql)
        resultsx = cou.fetchall()
        if len(resultsx)>0:
            if (type(resultsx[0][2]) != type(None) and type(resultsx[0][1]) != type(None)):
                bom_info = [resultsx[0][2].encode('latin1').decode('gbk'), resultsx[0][1].encode('latin1').decode('gbk')]
            elif (type(resultsx[0][1]) != type(None) and type(resultsx[0][2]) == type(None)):
               bom_info = [' ', resultsx[0][1].encode('latin1').decode('gbk')]
            elif (type(resultsx[0][2]) != type(None) and type(resultsx[0][1]) == type(None)):
                bom_info = [resultsx[0][2].encode('latin1').decode('gbk'), ' ']
            else:
                bom_info = [' ', ' ']
            material = [j,rows[1], bom_info[0], bom_info[1],rows[4], rows[2]]
        else:
            material = [j,rows[1], '', '',rows[4], rows[2]]

        table_material_copy.insert(len(table_material_copy), material)
        j = j + 1
    
    table_material[x] = table_material_copy
    return table_material

@app.route('/bomcalculate/<product_flag> <code_search> <product_id>', methods = ['GET', 'POST'])
@login_required
def bomcalculate(product_flag = '#', code_search = '+', product_id='#'):
    form = BomForm()
    cursor = db.cursor()
    table_product = [] 
    table_product_bom = [] #table of product bom info, in order to calculate and print the sum of materials
    table_material = {}
    table_product_name = {}
    table_material_print = []#the print table info
    table_material_print_use = []
    table_material_print_head = ''
    code_input = ''
    code = ''
    flag_print = 'No'
    place_id = []

    rights = g.user.rights
    if '1' in str(rights):
        flag_edit = 'Yes'
    else:
        flag_edit = 'No'

    conn=pymssql.connect(host=SQLSERVER_HOST,user=SQLSERVER_USER, password=SQLSERVER_PASS, database=SQLSERVER_DB, port=SQLSERVER_PORT, charset="UTF-8")
    cou=conn.cursor()
    if code_search != '+' and code_search != ' ':
        code = code_search
        code_input = code
    #产品列表初始化
    codex = str(request.form.get('select_info'))
    if not form.submit.data or (form.submit.data and (len(codex) ==0 or codex == 'None')):
        sql = "SELECT * FROM bom_index "
        cursor.execute(sql)
        results = cursor.fetchall()
        i = 1
        for rows in results:
            if rows[6] ==1:
                info_product = [i, rows[1], rows[2], rows[3], rows[5], rows[7], rows[0]]
                table_product.insert(len(table_product),info_product)
                i = i + 1
    #搜索产品
    if form.submit.data or code != '':
        if form.submit.data:
            code = str(request.form.get('select_info'))

        if len(code) > 0 and code != 'None':
            code_input = code
            table_product = [] 
            if '.' in code:
                sql = "SELECT * FROM bom_index \
                        WHERE erp_serial = '%s'" %(code)
            else:
                sql = "SELECT * FROM bom_index \
                        WHERE subname = '%s'" %(code)

            cursor.execute(sql)
            results = cursor.fetchall()
            i = 1
            for rows in results:
                if rows[6] == 1:
                    info_product = [i, rows[1], rows[2], rows[3], rows[5], rows[7], rows[0]]
                    table_product.insert(len(table_product),info_product)
                    i = i + 1
    # 物料汇总表信息
    if product_flag != '#':
        product_id = product_id + '#' + str(product_flag)
        i = 1
        flag_same_product = ''
        if product_id!='#':
            id = product_id.split('#')
            for x in id:
                if x !='':
                    y = '#' + x
                    if not(y in flag_same_product):

                        flag_same_product = flag_same_product + '#' + x 
                        sql = "SELECT * FROM bom_index \
                                    WHERE id = '%d'" %(int(x))
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        for rows in results:
                            info_product = [i, rows[1], rows[2], rows[3], x]
                            table_product_bom.insert(len(table_product),info_product)
                            i = i + 1 
                            name = rows[1]+'_'+rows[2]
                            table_product_name[x] = name

                        place_id.insert(len(place_id),x)

                        sql = "SELECT * FROM bom_detail \
                                        WHERE product_index = '%d' order by erp_material" %(int(x))
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        j = 1
                        table_material_copy = []
                        for rows in results:

                            '''
                            material = [j, rows[1], '', '', rows[2]]
                            table_material_copy.insert(len(table_material_copy), material)
                            j = j + 1
                            '''
                            sql="select * from dbo.t_ICItemCore where FNumber = '%s'" %(str(rows[1]).strip())
                            cou.execute(sql)
                            resultsx = cou.fetchall()
                            if len(resultsx)>0:
                                bom_info = [resultsx[0][2].encode('latin1').decode('gbk'), resultsx[0][1].encode('latin1').decode('gbk')]
                                material = [j,rows[1], bom_info[0], bom_info[1],rows[4], rows[2]]
                            else:
                                material = [j,rows[1], '', '', rows[4], rows[2]]
                            table_material_copy.insert(len(table_material_copy), material)
                            j = j + 1
                            
                        table_material_print.insert(len(table_material_print), table_material_copy)
                        table_material[x] = table_material_copy
                        
        product_id = flag_same_product
    else:
        product_id = '#'

    #打印物料表单信息
    flag = True
    counts = 0
    if form.calculate.data:
        flag_print = 'Yes'
        #print table_material_print
        for x in table_material_print:
            place_id_info = 'select_info' + place_id[counts]
            num = str(request.form.get(place_id_info))
            t_print_info = str(table_product_bom[counts][1]) + "_" + str(table_product_bom[counts][2]) + "_" + str(num)
            table_material_print_head = table_material_print_head + ";" + t_print_info
            counts = counts + 1
            for z in x:
                z[-1] = z[-1] * int(num)
                for y in table_material_print_use:
                    if z[1] == y[1]:
                        y[-1] = int(y[-1]) + int(z[-1])
                        flag = False
                        break
                    else:
                        flag = True
                if flag:
                    z[0] = len(table_material_print_use) + 1
                    table_material_print_use.insert(len(table_material_print_use),z)

    table_material_print_use_x = ''
    for x in table_material_print_use:
        for y in x:
            table_material_print_use_x = table_material_print_use_x + '+#' + str(y).strip() 
    table_material_print_use_x = table_material_print_use_x[1:]  

    if code_input == '':
        code_input = ' '

    cursor.close()
    conn.close()
    return render_template('bomcalculate.html', flag = 'bomcalculate', form = form, flag_edit = flag_edit,
                            username = str(g.user.name), code_input = code_input, product_id = product_id,
                            table_product = table_product, table_product_bom = table_product_bom,
                            table_product_name = table_product_name, table_material = table_material,
                            table_material_print_use = table_material_print_use_x, flag_print = flag_print,
                            table_material_print_head=table_material_print_head)


@app.route('/bomedit/<int:num_rows> <table_detail>', methods = ['GET', 'POST'])
@login_required
def bomedit(num_rows=3, table_detail='#'):
    form = BomForm_Edit()
    flag_edit = 'Yes'
    flag_register = 1
    typedata = ''
    bom_copy_info = ['','','','','']
    table_detail_html = []
    table_detailname_html = []
    cursor = db.cursor()

    conn=pymssql.connect(host=SQLSERVER_HOST,user=SQLSERVER_USER, password=SQLSERVER_PASS, database=SQLSERVER_DB, port=SQLSERVER_PORT, charset="UTF-8")
    cou=conn.cursor()

    sql = "SELECT * FROM product_sub_partname"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        typedata = typedata + " " + str(row[0])

    input_subname = ''
    input_version = '1.0'
    
    if table_detail != '#':
        res = table_detail.split('$')
        input_subname = res[0]
        input_version = res[1]
        sql = "SELECT * FROM bom_index \
                    WHERE subname = '%s' and version = '%s'" %(input_subname, input_version)
        cursor.execute(sql)
        results = cursor.fetchall()

        if len(results)>0:
            input_id = results[0][0]
            bom_copy_info = [input_subname, input_version, results[0][3], results[0][6], results[0][7]]

            sql = "SELECT * FROM bom_detail \
                        WHERE product_index = '%d' order by erp_material" %(input_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            num_rows = len(results)

            for x in results:
                erp_serial = str(x[1])
                erp_serial = erp_serial.strip()
                
                sql="select * from dbo.t_ICItemCore where FNumber = '%s'" %(str(erp_serial))
                cou.execute(sql)
                resultsx = cou.fetchall()
                material_info = [resultsx[0][2].encode('latin1').decode('gbk'), resultsx[0][1].encode('latin1').decode('gbk')]
                info = ['', erp_serial, material_info[0], material_info[1], x[2], x[4]]
                
                #info = ['', erp_serial, '', '', x[2], x[4]]
                table_detail_html.insert(len(table_detail_html), info)
 

    if form.newbom.data:
        input_subname = ''
        input_version = '1.0'
        bom_copy_info = ['','','','1','']
        table_detail_html = []
        num_rows = 3


    if str(request.form.get('commit_flag')) == 'YES_COMMIT':
        table_detail_html = []
        get_subname = str(request.form.get('subname_vice'))
        get_version = str(request.form.get('version_vice'))
        get_erp_serial = str(request.form.get('erp_serial'))
        get_status = str(request.form.get('status'))
        get_comments = str(request.form.get('comments'))
        #print get_comments, get_status, get_version, get_subname, get_erp_serial
        material_check = request.form.getlist('material_check')
        material_check = checked_get(material_check)
        material_serial = request.form.getlist('material_serial')
        material_name = request.form.getlist('material_name')
        material_model = request.form.getlist('material_model')
        material_quantity = request.form.getlist('material_quantity')
        material_comment = request.form.getlist('material_comment')
        
        num_rows = len(material_serial)
        for i in range(num_rows):
            info = ['',material_serial[i],material_name[i],material_model[i],material_quantity[i],material_comment[i]]
            table_detail_html.insert(len(table_detail_html),info)
        #print table_detail_html    
        bom_copy_info = [get_subname,get_version,get_erp_serial,get_status,get_comments]

        #print material_check, len(material_check)
        date_now = str(datetime.datetime.now())
        
        sql = "SELECT * FROM bom_index \
                WHERE subname = '%s' and version = '%s' and erp_serial = '%s'" % (get_subname, get_version, get_erp_serial)
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results)>0):
            flag_register = 20 #已经被注册
        else:
            try:
                sql = "INSERT INTO bom_index(subname, version, erp_serial, user, date, status, comments) \
                    VALUES ('%s', '%s', '%s', '%d', '%s', '%d', '%s')" % (get_subname, get_version, get_erp_serial, int(g.user.id),date_now[:-7], int(get_status), get_comments)
                cursor.execute(sql)
                db.commit()
                flag_register = 21#bom_indx注册成功
            except:
                flag_register = 30#bom_indx注册失败
            
            if flag_register == 21:
                try:
                    sql = "SELECT * FROM bom_index \
                            WHERE subname = '%s' and version = '%s' and erp_serial = '%s'" % (get_subname, get_version, get_erp_serial)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    
                    if len(results)>0:
                        id_register = results[0][0]
                        for i in range(num_rows):
                            if material_serial[i]:
                                sql = "INSERT INTO bom_detail(erp_material, quantity, product_index, comments) \
                                    VALUES ('%s', '%d', '%d', '%s')" % (material_serial[i], int(material_quantity[i]), id_register, material_comment[i])
                                cursor.execute(sql)
                        db.commit()
                    flag_register = 22#bom_detail 注册成功
                except:
                    flag_register = 31#bom_detail 注册失败
                    try:
                        sql = "DELETE FROM bom_index \
                                WHERE subname = '%s' and version = '%s' and erp_serial = '%s'" % (get_subname, get_version, get_erp_serial)
                        cursor.execute(sql);
                    except:
                        flag_register = 32

    if len(table_detail_html)!=num_rows:
        for i in range(num_rows-len(table_detail_html)):
            info = ['','','','','1','']
            table_detail_html.insert(len(table_detail_html),info)

    material_table_info = place_name_create(num_rows)

    #print flag_register
    cursor.close()
    cou.close()
    return render_template('bomedit.html', flag = 'bomedit', flag_edit = flag_edit, username = str(g.user.name), flag_register = flag_register,
                            form=form, typedatax = typedata, num_rows = num_rows, 
                            bom_copy_info = bom_copy_info, table_detail=table_detail_html, material_table_info = material_table_info)

  
def input_get(num_rows):
    table_detail_html = []
    for i in range(num_rows):
        place_name=['check'+str(i)+'0', 'serial'+str(i)+'1','place'+str(i)+'2','model'+str(i)+'3','number'+str(i)+'4','comment'+str(i)+'5']
        info = []
        for x in range(6):
            cotents = str(request.form.get(place_name[x]))
            info.insert(len(info),cotents)
        table_detail_html.insert(len(table_detail_html),info)

    return table_detail_html
   
def place_name_create(num_rows):
    material_serial_name = []
    material_name_name = []
    material_model_name = []
    for i in range(num_rows):
        name = 'Material_Serial_Input' + str(i)
        material_serial_name.insert(len(material_serial_name),name)
        name = 'Material_Name_Input' + str(i)
        material_name_name.insert(len(material_name_name),name)
        name = 'Material_Model_Input' + str(i)
        material_model_name.insert(len(material_model_name),name)
        
    material = [material_serial_name,material_name_name, material_model_name]
    return material 

def checked_get(check):
    status = ''
    for i in check:
        status = status + i

    val = status.split("NO")
    val.pop(0)#删除首项

    return val


def Material_serial_Index():
    conn=pymssql.connect(host=SQLSERVER_HOST,user=SQLSERVER_USER, password=SQLSERVER_PASS, database=SQLSERVER_DB, port=SQLSERVER_PORT, charset="UTF-8")
    cou=conn.cursor()
    f1 = open(JsMaterialSerialIndexSrc,'w')
    f2 = open(JsERPinfoSrc,'w')
    Material_serial_Index = "var Material_serial_Index = '"   
    erpinfo = "var material_info = {"    
    sql="select * from dbo.t_ICItemCore" 
    cou.execute(sql)
    for x in cou.fetchall():
        Material_serial_Index = Material_serial_Index + " " + str(x[6])
        if (type(x[1]) != type(None) and type(x[2]) != type(None)):
            erpinfo = erpinfo + "'" + str(x[6]) + "':['" + x[2].encode('latin1') + "','" + x[1].encode('latin1') + "'],"
        elif (type(x[1]) != type(None) and type(x[2]) == type(None)):
            erpinfo = erpinfo + "'" + str(x[6]) + "':[' ','" + x[1].encode('latin1') + "'],"
        elif (type(x[1]) == type(None) and type(x[2]) != type(None)):
            erpinfo = erpinfo + "'" + str(x[6]) + "':['" + x[2].encode('latin1') + "',' '],"
        else:
            erpinfo = erpinfo + "'" + str(x[6]) + "':[' ',' '],"
             
    Material_serial_Index += "';"
    erpinfo = erpinfo[:-1] + "};"
    erpinfo = erpinfo.decode('gbk').encode('utf8')
    f1.write(Material_serial_Index)
    f2.write(erpinfo)
    f1.close()
    f2.close()
    conn.close()
