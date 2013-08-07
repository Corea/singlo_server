# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request
from flask.ext.security import login_required

import god.teacher.queries as queries

mod = Blueprint('teacher', __name__, url_prefix='/teacher')

@mod.route('/')
@login_required
def list():
	teachers = queries.get_all_teacher()
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
		lessons = request.form['lessons'].strip()
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
		if lessons == u'' or lessons == '':
			errors.append('추천 강좌가 빈칸입니다.')

		try:
			price = int(price)
		except: 
			errors.append('금액은 정수여야합니다.')

		if len(errors) == 0: 
			queries.add_teacher(name, birthday, phone, None, company, certification, \
				lessons, True, price, profile, url)
			return redirect(url_for('teacher.list'))
	else:
		name = ''
		birthday = ''
		phone = ''
		company = ''
		certification = ''
		lessons = ''
		price = 0
		profile = ''
		url = ''
		errors = []
	return render_template('teacher_add.html', name=name,
		birthday=birthday, phone=phone, company=company,
		certification=certification, lessons=lessons,
		price=price, profile=profile, url=url, errors=errors)
