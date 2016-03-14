#!flask/bin/python

import sys
sys.path.insert(0, '/var/www/license_generator/')

from app import app as application
if __name__ == '__main__':
  application.run()
