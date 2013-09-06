# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request
from flask import current_app
from flask.ext.security import login_required

import god.order.queries as queries
import god.teacher.queries as teacher_queries
from god import urldecode
from api.auth.func import get_timestamp

import os

mod = Blueprint('order', __name__, url_prefix='/order')




@mod.route('/')
@login_required
def list():
	lessons = queries.get_all_lessons()
	real_lessons = []
	for lesson in lessons:
#		try:
#		except:
#			pass
		real_lessons.append([lesson, teacher_queries.get_teacher(lesson.teacher_id)])
		
	return render_template('order.html', lessons=real_lessons)
