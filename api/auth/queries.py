# -*- coding: utf-8 -*-

from api import db
from api.models import User, Teacher

from datetime import datetime

def add_user(name, birthday, phone, photo=None):
	user = User(name, birthday, phone)
	db.session.add(user)
	db.session.commit()
	if photo is not None:
		user.photo = str(user.id) + '.png'
		db.session.commit()

def get_valid_user(name, birthday, phone):
	user = User.query.filter_by(
		name=name, birthday=birthday, phone=phone).first()
	if user is not None:
		user.lastlogin_datetime = datetime.now()
		db.session.commit()

	return user

def get_valid_teacher(name, birthday, phone):
	teacher = Teacher.query.filter_by(
		name=name, birthday=birthday, phone=phone).first()
	if teacher is not None:
		teacher.lastlogin_datetime = datetime.now()
		db.session.commit()

	return teacher



