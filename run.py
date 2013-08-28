# -*- coding: utf-8 -*-

from api import app as api_app

if __name__ == '__main__':
	api_app.debug = True
	api_app.run(host='0.0.0.0')
