#!flask/bin/python

import sys
sys.path.insert(0, '/var/www/qrcode/')

from app import app as application
if __name__ == '__main__':
  application.run()
