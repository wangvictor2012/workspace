# -*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms.fields.html5 import DateField
from wtforms import ValidationError
import sys

#datachoice = [('100010','Type ABCD'),('100100', 'Type G'),('100110', 'Type H')]

def encodechinese(chinese):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    return chinese.encode('utf-8')

class LicenseForm(Form):
    #datachoice = database_machinetype()
        
    featurecode = TextField('featurecode', validators = [Required()])
    remark = TextAreaField('remark')
    submit_cal = SubmitField(encodechinese("计 算"))
    submit_query = SubmitField(encodechinese("历史查询"))
    submit_download = SubmitField(encodechinese("下 载"))
    machinetype = SelectField('machinetype', validators=[Required()])    


class UserForm(Form):
    username = StringField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    sign_in = SubmitField(encodechinese("登 陆"))
    
    
class RegistrationForm(Form):
    #email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password',validators=[Required()])
    password2 = PasswordField('Condfirm password', validators = [Required()])
    submit = SubmitField(encodechinese("注 册"))

class UserManageForm(Form):
    username = StringField('username', validators = [Required()])
    search = SubmitField(encodechinese("查 询"))
    showallusers = SubmitField(encodechinese("所有用户"))
    change = SubmitField(encodechinese("更 改"))
    delete = SubmitField(encodechinese("删 除"))

class MachinetypeForm(Form):
    name = TextField('name',validators = [Required()])
    value = StringField('value', validators = [Required()])
    showallmachinetypes = SubmitField(encodechinese("所有设备类型"))
    add = SubmitField(encodechinese("增 加"))
    delete = SubmitField(encodechinese("删 除"))

class HistoryqueryForm(Form):
    datebegin = DateField(encodechinese("起始时间"))
    datestop = DateField(encodechinese("结束时间"))
    search = SubmitField(encodechinese("查 询"))

