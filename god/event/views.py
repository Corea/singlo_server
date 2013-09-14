# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request
from flask import current_app
from flask.ext.security import login_required

import god.event.queries as queries
from god import urldecode
from api.auth.func import get_timestamp

import os
from datetime import datetime

mod = Blueprint('event', __name__, url_prefix='/event')



@mod.route('/')
@login_required
def list():
	events = queries.get_all_event()
	return render_template('event.html', events=events)

@mod.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method == 'POST':
		start = request.form['start'].strip()
		end = request.form['end'].strip()

		errors = []

		format = "%Y-%m-%d %H:%M"

		try:
			start_datetime = datetime.strptime(start, format)
		except:
			errors.append('시작 시간이 잘못되었습니다.')

		try:
			end_datetime = datetime.strptime(end, format)
		except:
			errors.append('종료 시간이 잘못되었습니다.')

		if 'image' in request.files and request.files['image']:
			image = request.files['image']
		else:
			image = None
			errors.append('그림을 넣어주세요.')

		if len(errors) == 0: 
			event = queries.add_event(start_datetime, end_datetime, image)

			if image is not None:
				image_path = os.path.join(current_app.config['EVENT_FOLDER'], event.image)
				image.save(image_path)
			return redirect(url_for('event.list'))
	else:
		start = ''
		end = ''
		errors = []

	return render_template('event_add.html', 
		start=start, end=end, errors=errors)

@mod.route('/remove/<int:event_id>')
@login_required
def remove(event_id):
	queries.delete_event(event_id)
	return redirect(url_for('event.list'))


