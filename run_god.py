# -*- coding: utf-8 -*-

from god import app as god_app
from api import app as api_app

god_app.run(host='0.0.0.0', port=6500)
