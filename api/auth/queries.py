# -*- coding: utf-8 -*-

from api import db
from api.models import User, Teacher, Lesson_Question, \
	Lesson_Answer, Lesson_Evaluation

from datetime import datetime

def add_user(name, birthday, phone, photo, pushtoken):
	db.session.add(user)
	db.session.commit()
	if photo is not None:
		user.photo = 'user_' + str(user.id) + '.png'
		db.session.commit()

def get_valid_user(name, birthday, phone):
	user = User.query.filter_by(
		name=name, birthday=birthday, phone=phone).first()
	if user is not None:
		user.lastlogin_datetime = datetime.now()
		db.session.commit()

	return user

def get_reg_id(user_id):
        user=User.query.filter_by(
                id=user_id).first()
        return user.pushtoken

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
