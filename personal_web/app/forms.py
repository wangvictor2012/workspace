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

class TwoDcodeForm(Form):
    #datachoice = database_machinetype()
    message_TwoDcode = TextAreaField('message', validators = [Required()])
    submit_commit = SubmitField(encodechinese("提 交"))
    submit_download = SubmitField(encodechinese("下 载"))
    submit_gethosts = SubmitField(encodechinese("下载最新Hosts"))
    



