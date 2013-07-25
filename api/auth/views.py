# -*- coding: utf-8 -*-
from flask import request, render_template, send_from_directory
from flask import Blueprint

import api.auth.queries as queries

mod = Blueprint('auth', __name__, url_prefix='/auth')


@mod.route('/register', methods=['POST'])
def register():
	try:
		name = request.form['name']
		birthday = request.form['birthday']
		phone = request.form['phone']
		
		user = queries.get_valid_user(name, birthday, phone)
		teacher = queries.get_valid_teacher(name, birthday, phone)
		if user is None and teacher is None:
			queries.add_user(name, birthday, phone)
			user = queries.get_valid_user(name, birthday, phone)
			return render_template('register.json', user=user)
		else:
			raise
	except Exception as e:
		return render_template('error.json')


@mod.route('/login', methods=['POST'])
def login():
	try:
		name = request.form['name']
		birthday = request.form['birthday']
		phone = request.form['phone']

		user = queries.get_valid_user(name, birthday, phone)
		if user is None:
			teacher = queries.get_valid_teacher(
				name, birthday, phone)
			if teacher is None:
				raise
			else:
				return render_template('login_teacher.json', teacher=teacher)
		else:
			return render_template('login.json', user=user)
	except:
		return render_template('error.json')


