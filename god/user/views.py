# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request
from flask import current_app
from flask.ext.security import login_required

import god.user.queries as queries
from god import urldecode

mod = Blueprint('user', __name__, url_prefix='/user')

@mod.route('/')
@login_required
def list():
	users = queries.get_active_user()
	real_users = []
	for user in users:
		real_users.append([user, 
			queries.get_lesson_count(user.id),
			queries.get_lesson_answer_count(user.id)])
		
	return render_template('user.html', users=real_users)

@mod.route('/modify/<int:user_id>', methods=['GET', 'POST'])
@login_required
def modify(user_id):
	try:
		user = queries.get_user(user_id)
		if user.active == False:
			raise

		if request.method == 'GET':
			name = urldecode(user.name)
			birthday = urldecode(user.birthday)
			phone = urldecode(user.phone)
			point = user.point
			photo = user.photo
			errors = []
		else:
			name = request.form['name'].strip()
			birthday = request.form['birthday'].strip()
			phone = request.form['phone'].strip()
			point = request.form['point'].strip()
			photo = user.photo

			errors = []

			if name == u'' or name == '':
				errors.append('이름이 빈칸입니다.')
			if birthday == u'' or birthday == '':
				errors.append('생일이 빈칸입니다.')
			if phone == u'' or phone == '':
				errors.append('전화번호가 빈칸입니다.')
			try:
				point = int(point)
			except: 
				errors.append('골프공의 수는 정수여야합니다.')

			if len(errors) == 0: 
				queries.modify_user(user, name, birthday, phone, point)
				return redirect(url_for('user.list'))
		return render_template('user_modify.html', name=name,
			birthday=birthday, phone=phone, point=point, photo=photo, 
			user_id=user_id, errors=errors)
	except Exception, e:
		print e
		return redirect(url_for('user.list'))

@mod.route('/remove/<int:user_id>')
@login_required
def remove(user_id):
	queries.delete_user(user_id)
	return redirect(url_for('user.list'))

@mod.route('/remove_photo/<int:user_id>')
@login_required
def remove_photo(user_id):
	queries.delete_photo(user_id)
	return redirect(url_for('user.modify', user_id=user_id))


