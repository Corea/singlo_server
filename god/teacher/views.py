# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request
from flask import current_app
from flask.ext.security import login_required

import god.teacher.queries as queries
from god import urldecode
from api.auth.func import get_timestamp

import urllib
import os

mod = Blueprint('teacher', __name__, url_prefix='/teacher')

@mod.route('/')
@login_required
def list():
	teachers = queries.get_active_teacher()
	return render_template('teacher.html', teachers=teachers)

@mod.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method == 'POST':
		name = request.form['name'].strip()
		birthday = request.form['birthday'].strip()
		phone = request.form['phone'].strip()
		company = request.form['company'].strip()
		certification = request.form['certification'].strip()
		price = request.form['price'].strip()
		profile = request.form['profile'].strip()
		url = request.form['url'].strip()

		errors = []

		if name == u'' or name == '':
			errors.append('이름이 빈칸입니다.')
		if birthday == u'' or birthday == '':
			errors.append('생일이 빈칸입니다.')
		if phone == u'' or phone == '':
			errors.append('전화번호가 빈칸입니다.')
		if company == u'' or company == '':
			errors.append('회사이름이 빈칸입니다.')
		if certification == u'' or certification == '':
			errors.append('자격증이 빈칸입니다.')

		try:
			price = int(price)
		except: 
			errors.append('금액은 정수여야합니다.')

		if 'photo' in request.files:
			photo = request.files['photo']
		else:
			photo = None


		if len(errors) == 0: 
			teacher = queries.add_teacher(name, birthday, phone, photo, company, \
				certification, True, price, profile, url)

			if photo is not None:
				photo_path = os.path.join(current_app.config['PROFILE_FOLDER'], teacher.photo)
				photo.save(photo_path)
			return redirect(url_for('teacher.list'))
	else:
		name = ''
		birthday = ''
		phone = ''
		company = ''
		certification = ''
		price = 0
		profile = ''
		url = ''
		errors = []
	return render_template('teacher_add.html', name=name,
		birthday=birthday, phone=phone, company=company,
		certification=certification, price=price, profile=profile, 
		url=url, errors=errors)

@mod.route('/modify/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def modify(teacher_id):
	try:
		teacher = queries.get_teacher(teacher_id)
		if teacher.active == False:
			raise

		if request.method == 'GET':
			name = urldecode(teacher.name)
			birthday = urldecode(teacher.birthday)
			phone = urldecode(teacher.phone)
			company = urldecode(teacher.company)
			certification = urldecode(teacher.certification)
			price = teacher.price
			photo = teacher.photo
			profile = urldecode(teacher.profile)
			url = urldecode(teacher.url)
			errors = []
		else:
			name = request.form['name'].strip()
			birthday = request.form['birthday'].strip()
			phone = request.form['phone'].strip()
			company = request.form['company'].strip()
			certification = request.form['certification'].strip()
			price = request.form['price'].strip()
			profile = request.form['profile'].strip()
			url = request.form['url'].strip()
			
			if 'photo' in request.files:
				photo = request.files['photo']
				photo_name = 'teacher_' + str(teacher_id) + '_' + str(get_timestamp()) + '.png'
				photo_path = os.path.join(current_app.config['PROFILE_FOLDER'], photo_name)
				photo.save(photo_path)
				photo = photo_name
			else:
				photo = None

			errors = []

			if name == u'' or name == '':
				errors.append('이름이 빈칸입니다.')
			if birthday == u'' or birthday == '':
				errors.append('생일이 빈칸입니다.')
			if phone == u'' or phone == '':
				errors.append('전화번호가 빈칸입니다.')
			if company == u'' or company == '':
				errors.append('회사이름이 빈칸입니다.')
			if certification == u'' or certification == '':
				errors.append('자격증이 빈칸입니다.')

			try:
				price = int(price)
			except: 
				errors.append('금액은 정수여야합니다.')


			if len(errors) == 0: 
				queries.modify_teacher(teacher, name, birthday, phone, photo, company, \
					certification, True, price, profile, url)
				return redirect(url_for('teacher.list'))

		return render_template('teacher_modify.html', name=name,
			birthday=birthday, phone=phone, company=company,
			certification=certification, price=price, profile=profile, 
			url=url, photo=photo, errors=errors, teacher_id=teacher_id)
	except:
		return redirect(url_for('teacher.list'))
	


@mod.route('/remove/<int:teacher_id>')
@login_required
def remove(teacher_id):
	queries.delete_teacher(teacher_id)
	return redirect(url_for('teacher.list'))

@mod.route('/remove_photo/<int:teacher_id>')
@login_required
def remove_photo(teacher_id):
	queries.delete_photo(teacher_id)
	return redirect(url_for('teacher.modify', teacher_id=teacher_id))

