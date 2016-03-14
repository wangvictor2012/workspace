import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

#MYSQL_HOST = '172.16.1.181'
#MYSQL_HOST = '172.16.17.23'
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_USER = 'root'
MYSQL_PASS = 'wang123456'
#MYSQL_USER = 'admin'
#MYSQL_PASS = 'fangling'
MYSQL_DB = 'internal'

SQLSERVER_HOST = 'kingdee-5'
SQLSERVER_PORT = '1433'
SQLSERVER_USER = 'sa'
SQLSERVER_PASS = '1Yuan$!!'
SQLSERVER_DB = 'AIS20140820155611'

''' 
SQLSERVER_HOST = 'localhost'
SQLSERVER_PORT = '1433'
SQLSERVER_USER = 'sa'
SQLSERVER_PASS = 'wang123456'
SQLSERVER_DB = 'test'
'''
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'user.sqlit')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#ImagefileSrc = '/var/www/qrcode/app/static/img/'
ImagefileSrc = 'D:\\Etudiant\\Test\\qrcode\\app\\static\\img\\'
#JsTypecodeIndexSrc = '/var/www/qrcode/app/static/js/TypecodeIndex.js'
JsTypecodeIndexSrc = 'D:\\Etudiant\\Test\\qrcode\\app\\static\\js\\TypecodeIndex.js'
#JsMaterialSerialIndexSrc = '/var/www/qrcode/app/static/js/Material_serial_Index.js'
JsMaterialSerialIndexSrc = 'D:\\Etudiant\\Test\\qrcode\\app\\static\\js\\Material_serial_Index.js'
#ErrorlogSrc = '/var/www/qrcode/tmp/error.log'
ErrorlogSrc = 'D:\\Etudiant\\Test\\qrcode\\tmp\\error.log'
#JsERPinfoSrc = '/var/www/qrcode/app/static/js/ERP_info.js'
JsERPinfoSrc = 'D:\\Etudiant\\Test\\qrcode\\app\\static\\js\\ERP_info.js'

ERPDownloadSrc = 'D:\\Etudiant\\Git_place\\qrcode\\app\\static\\files\\'
