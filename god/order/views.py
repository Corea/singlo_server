# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request
from flask import current_app
from flask.ext.security import login_required

import god.order.queries as queries
from god import urldecode
from api.auth.func import get_timestamp

import os

mod = Blueprint('order', __name__, url_prefix='/order')




@mod.route('/')
@login_required
def list():
	lessons = queries.get_all_lessons()
	return render_template('order.html', lessons=lessons)
