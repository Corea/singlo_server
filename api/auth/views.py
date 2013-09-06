# -*- coding: utf-8 -*-
from flask import request, render_template, send_from_directory
from flask import Blueprint, current_app

import api.auth.queries as queries
import api.auth.func as func

import os


mod = Blueprint('auth', __name__, url_prefix='/auth')

@mod.route('/register', methods=['POST'])
def register():
	try:
		name = request.form['name']
		birthday = request.form['birthday']
		phone = request.form['phone']
		if len(name) > 128 or len(birthday) > 31 or len(phone) > 31:
			raise
		if 'pushtoken' in request.form:
			pushtoken = request.form['pushtoken']
		else:
			pushtoken = None

		if 'model' in request.form:
			phone_model = request.form['model']
		else:
			phone_model = None

		if 'profile' in request.files:
			profile = request.files['profile']
		else:
			profile = None
                
		user = queries.get_valid_user(name, birthday, phone)
		teacher = queries.get_valid_teacher(name, birthday, phone)
		if user is None and teacher is None:
			queries.add_user(name, birthday, phone, pushtoken, profile, phone_model)
			user = queries.get_valid_user(name, birthday, phone)
			if profile is not None:
				profile_path = os.path.join(current_app.config['PROFILE_FOLDER'], user.photo)
				profile.save(profile_path)
			return render_template('register.json', user=user)
		else:
			raise
	except Exception as e:
		print e
		return render_template('error.json')


@mod.route('/login', methods=['POST'])
def login():
	try:
		name = request.form['name']
		birthday = request.form['birthday']
		phone = request.form['phone']
                                                    
		user = queries.get_valid_user(name, birthday, phone)
                
		if user is None:
			teacher = queries.get_valid_teacher(name, birthday, phone)
			if teacher is None:
				raise
			else:
				if 'pushtoken' in request.form:
					queries.update_pushtoken_teacher(teacher.id, request.form['pushtoken'])
				if 'model' in request.form:
					queries.update_phone_model_teacher(teacher.id, request.form['model'])
				count = queries.count_unanswer_question(teacher.id)
				evaluation = queries.get_score_evaluation(teacher.id)
				return render_template('login_teacher.json', 
					teacher=teacher, count=count, evaluation=evaluation)
		else:
			if 'pushtoken' in request.form:
				queries.update_pushtoken_user(user.id, request.form['pushtoken'])
			if 'model' in request.form:
				queries.update_phone_model_user(user.id, request.form['model'])
			count = queries.count_unconfirm_question(user.id)
			return render_template('login.json', user=user, count=count)
	except Exception, e:
		print e
		return render_template('error.json')

@mod.route('/profile', methods=['POST'])
def profile():
	try:
		profile = request.files['profile']
		photo_path = ''
		if 'user_id' in request.form:
			user_id = request.form['user_id']
			user = queries.get_user(user_id)
			photo_path = func.get_user_photo_path(user_id)

			profile_path = os.path.join(current_app.config['PROFILE_FOLDER'], photo_path)
			profile.save(profile_path)
			queries.update_user_photo(user_id, photo_path)
		elif 'teacher_id' in request.form:
			teacher_id = request.form['teacher_id']
			teacher = queries.get_teacher(teacher_id)
			photo_path = func.get_teacher_photo_path(teacher_id)

			profile_path = os.path.join(current_app.config['PROFILE_FOLDER'], photo_path)
			profile.save(profile_path)
			queries.update_teacher_photo(teacher_id, photo_path)
		else:
			raise
		return render_template('profile.json', photo_path=photo_path)
	except Exception, e:
		print e
		return render_template('error.json')

@mod.route('/get_user_profile', methods=['POST'])
def get_user_profile():
	try:
		user_id = request.form['user_id']
		user = queries.get_user(user_id)
		return render_template('get_user_profile.json', user=user)
	except Exception, e:
		print e
		return render_template('error.json')
