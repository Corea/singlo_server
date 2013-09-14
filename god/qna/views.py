# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, redirect, url_for, request
from flask import current_app
from flask.ext.security import login_required

import god.qna.queries as queries
from god import urldecode
from api.auth.func import get_timestamp

import os

mod = Blueprint('qna', __name__, url_prefix='/qna')


@mod.route('/')
@login_required
def list():
	qnas = queries.get_all_qnas()
	return render_template('qna.html', qnas=qnas)

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
			queries.add_qna(title, content)
			return redirect(url_for('qna.list'))
	else:
		title = ''
		content = ''
		errors = []
	
	return render_template('qna_add.html', 
		title=title, content=content, errors=errors)
		
@mod.route('/modify/<int:qna_id>', methods=['GET', 'POST'])
@login_required
def modify(qna_id):
	try:
		qna = queries.get_qna(qna_id)
		if request.method == 'GET':
			title = urldecode(qna.title)
			content = urldecode(qna.content)
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
				queries.modify_qna(qna, title, content)
				return redirect(url_for('qna.list'))
		return render_template('qna_modify.html', qna_id=qna.id,
			title=title, content=content, errors=errors)
	except Exception, e:
		print e
		return redirect(url_for('qna.list'))


@mod.route('/remove/<int:qna_id>')
@login_required
def remove(qna_id):
	queries.delete_qna(qna_id)
	return redirect(url_for('qna.list'))


