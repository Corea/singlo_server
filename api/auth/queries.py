# -*- coding: utf-8 -*-

from api import db
from api.models import Version, User, Teacher, Lesson_Question, \
        Lesson_Answer, Lesson_Evaluation
import api.auth.func as func

from datetime import datetime

def get_version_android():
	version = Version.query.filter_by(app_name='singlo_android').first()

	return version

def add_user(name, birthday, phone, pushtoken, photo=None, phone_model=None):
	user = User(name, birthday, phone, pushtoken, phone_model)
	db.session.add(user)
	db.session.commit()
	if photo is not None:
		user.photo = func.get_user_photo_path(user.id)
		db.session.commit()

def get_user(user_id):
	user = User.query.filter_by(id=user_id).first()

	return user

def update_user_photo(user_id, photo_path):
	user = get_user(user_id)
	user.photo = photo_path
	db.session.commit()

def get_teacher(teacher_id):
	teacher = Teacher.query.filter_by(id=teacher_id).first()

	return teacher

def update_teacher_photo(teacher_id, photo_path):
	teacher = get_teacher(teacher_id)
	teacher.photo = photo_path
	db.session.commit()

def get_valid_user(name, birthday, phone):
	user = User.query.filter_by(
		name=name, birthday=birthday, phone=phone, active=True).first()
	if user is not None:
		user.lastlogin_datetime = datetime.now()
		db.session.commit()

	return user

def get_reg_id(user_id):
	user = get_user(user_id)

	return user.pushtoken

def update_pushtoken_user(user_id, pushtoken):
	user = get_user(user_id)
	user.pushtoken = pushtoken
	db.session.commit()                          

def update_pushtoken_teacher(teacher_id, pushtoken):
	teacher = get_teacher(teacher_id)
	teacher.pushtoken = pushtoken
	db.session.commit()

def update_phone_model_user(user_id, phone_model):
	user = get_user(user_id)
	user.phone_model = phone_model
	db.session.commit()                          

def update_phone_model_teacher(teacher_id, phone_model):
	teacher = get_teacher(teacher_id)
	teacher.phone_model = phone_model
	db.session.commit()


def get_valid_teacher(name, birthday, phone):
	teacher = Teacher.query.filter_by(
		name=name, birthday=birthday, phone=phone, active=True).first()
	if teacher is not None:
		teacher.lastlogin_datetime = datetime.now()
		db.session.commit()

	return teacher


def get_score_evaluation(teacher_id):
	questions = Lesson_Question.query.filter_by(
		teacher_id=teacher_id, status=True)

	count = 0
	speed = 0.
	accuracy = 0.
	price = 0.
	recommend = 0 
	for question in questions:
		try:
			evaluation = Lesson_Evaluation.query.filter_by(
				question_id=question.id, teacher_id=teacher_id).first()
			if evaluation is None:
				continue
			count += 1
			speed += evaluation.speed
			accuracy += evaluation.accuracy
			price += evaluation.price
			if evaluation.recommend:
				recommend += 1
		except:
			pass
	if count == 0: 
		average = 0
	else:
		average = (speed + accuracy + price + recommend * 5.) / float(count)
		average = average / 4.

	return { 'count': count, 'speed': speed, 'accuracy': accuracy,
		'price': price, 'recommend': recommend, 'average': average }
        
def count_unconfirm_question(user_id):
	questions = Lesson_Question.query.filter_by(
		user_id=user_id, status=True)
	count = 0

	for question in questions:
		answer = Lesson_Answer.query.filter_by(
			question_id=question.id).first()
		if answer.confirm_status == False:
			count += 1

	return count

def count_unanswer_question(teacher_id):
	count = Lesson_Question.query.filter_by(
		teacher_id=teacher_id, status=False).count()

	return count
