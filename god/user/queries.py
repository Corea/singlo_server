# -*- coding: utf-8 -*-

from god import db as god_db
from god.models import User, Lesson_Question

import urllib

def get_user(id):
	user = User.query.filter_by(id=id).first()
	
	return user

def get_active_user():
	users = User.query.filter_by(active=True)

	return users

def get_all_user():
	users = User.query.all()

	return users

def modify_user(user, name, birthday, phone):
	user.name = urllib.quote(name.encode('utf8'))
	user.birthday = urllib.quote(birthday.encode('utf8'))
	user.phone = urllib.quote(phone.encode('utf8'))
	god_db.session.commit()

	return user

def delete_photo(id):
	user = get_user(id)
	user.photo = None
	god_db.session.commit()
	
def delete_user(id):
	user = get_user(id)
	user.active = False
	god_db.session.commit()

def get_lesson_count(user_id):
	count = Lesson_Question.query.filter_by(
		user_id=user_id).count()

	return count

def get_lesson_answer_count(user_id):
	count = Lesson_Question.query.filter_by(
		user_id=user_id, status=True).count()

	return count
