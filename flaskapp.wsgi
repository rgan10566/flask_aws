#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/flaskapp')

from newflaskapp import app as application
