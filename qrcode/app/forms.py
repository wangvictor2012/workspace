# -*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, TextAreaField, PasswordField, IntegerField, BooleanField
from wtforms.validators import Required
import sys

def encodechinese(chinese):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    return chinese.encode('utf-8')

class DcodeForm(Form):
    inputpage = IntegerField('pagenum', validators = [Required()])
    remark = TextAreaField('remark')
    submit = SubmitField(encodechinese("提交"))
    register = SubmitField(encodechinese("注册 / 打印"))
    find = SubmitField(encodechinese("查询"))
    submitpage = SubmitField(encodechinese("确定"))
    print_button = SubmitField(encodechinese("打印"))


class UserForm(Form):
    submit = SubmitField(encodechinese("登录"))
    username = TextField('username', validators = [Required()])
    password = PasswordField('username', validators = [Required()])
    

class BomForm(Form):
    submit = SubmitField(encodechinese("查询"))
    calculate = SubmitField(encodechinese("物料汇总"))
    download = SubmitField(encodechinese("下载"))
    bomid = TextField('bomid', validators = [Required()])

class BomForm_Edit(Form):
    newbom = SubmitField(encodechinese("新建 BOM"))
    add = SubmitField(encodechinese("增加"))
    delete = SubmitField(encodechinese("删除"))
    commit = SubmitField(encodechinese("提交"))
    
