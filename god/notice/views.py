# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, redirect, url_for, request
from flask import current_app
from flask.ext.security import login_required

import god.notice.queries as queries
from god import urldecode
from api.auth.func import get_timestamp

import os

mod = Blueprint('notice', __name__, url_prefix='/notice')


@mod.route('/')
@login_required
def list():
	notices = queries.get_all_notices()
	return render_template('notice.html', notices=notices)

@mod.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method == 'POST':
		title = request.form['title'].strip()
		content = request.form['content'].strip()
		
		errors = []

		if title == u'' or title == '':
			errors.append('제목이 없습니다.')
		if content == u'' or content == '':
			errors.append('내용이 없습니다.')
		
		if len(errors) == 0:
			queries.add_notice(title, content)
			return redirect(url_for('notice.list'))
	else:
		title = ''
		content = ''
		errors = []
	
	return render_template('notice_add.html', 
		title=title, content=content, errors=errors)
		
@mod.route('/modify/<int:notice_id>', methods=['GET', 'POST'])
@login_required
def modify(notice_id):
	try:
		notice = queries.get_notice(notice_id)
		if request.method == 'GET':
			title = urldecode(notice.title)
			content = urldecode(notice.content)
			errors = []
		else:
			title = request.form['title'].strip()
			content = request.form['content'].strip()
			
			errors = []

			if title == u'' or title == '':
				errors.append('제목이 없습니다.')
			if content == u'' or content == '':
				errors.append('내용이 없습니다.')
			
			if len(errors) == 0:
				queries.modify_notice(notice, title, content)
				return redirect(url_for('notice.list'))
		return render_template('notice_modify.html', notice_id=notice.id,
			title=title, content=content, errors=errors)
	except Exception, e:
		print e
		return redirect(url_for('notice.list'))


@mod.route('/remove/<int:notice_id>')
@login_required
def remove(notice_id):
	queries.delete_notice(notice_id)
	return redirect(url_for('notice.list'))


