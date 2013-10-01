# -*- coding: utf-8 -*-

from api import db
from api.models import Lesson_Question, Lesson_Answer, Lesson_Answer_Image,\
	Lesson_Training, Lesson_Evaluation

def add_lesson_question_video(lesson_question):
	db.session.add(lesson_question)
	db.session.commit()
	lesson_question.video = str(lesson_question.id) + '_question.mp4'
	lesson_question.thumbnail = str(lesson_question.id) + '_capture.png'
	db.session.commit()

	return lesson_question

def add_lesson_question(lesson_question):
	db.session.add(lesson_question)
	db.session.commit()

	return lesson_question


def set_lesson_purchase_token(lesson_question, token):
	lesson_question.purchase_token = token
	db.session.commit()

	return lesson_question

def get_lesson_question(lesson_id):
	lesson = Lesson_Question.query.filter_by(
		id=lesson_id).first()

	return lesson

def get_lesson_user_id(lesson_id):
	lesson = Lesson_Question.query.filter_by(
		id=lesson_id).first()

	return lesson.user_id

def add_lesson_answer(lesson_answer):
	db.session.add(lesson_answer)
	db.session.commit()
	lesson_answer.sound = str(lesson_answer.id) + '_answer_sound.wav'
	db.session.commit()

	return lesson_answer

def get_lesson_answer(lesson_id):
	answer = Lesson_Answer.query.filter_by(
		question_id=lesson_id).first()
	answer.confirm_status = True
	db.session.commit()

	return answer

def add_lesson_answer_image(lesson_answer_image):
	db.session.add(lesson_answer_image)
	db.session.commit()

def get_lesson_answer_image(answer_id):
	image = Lesson_Answer_Image.query.filter_by(
		answer_id=answer_id).all()

	return image

def get_all_lesson(teacher_id):
	lessons1 = Lesson_Question.query.filter_by(
		teacher_id=teacher_id).filter(
		Lesson_Question.purchase_token!=None).all()
	lessons2 = Lesson_Question.query.filter_by(
		teacher_id=None, status=False).filter(
		Lesson_Question.purchase_token!=None).all()

	lessons = lessons1 + lessons2 

	return lessons

def get_all_lesson_by_user(user_id):
	lessons = Lesson_Question.query.filter_by(
		user_id=user_id).filter(
		Lesson_Question.purchase_token!=None).all()

	return lessons


def add_lesson_evaluation(lesson_question, lesson_evaluation):
	lesson_question.evaluation_status = True
	db.session.add(lesson_evaluation)
	db.session.commit()

def get_all_evaluation(teacher_id):
	evaluations = Lesson_Evaluation.query.filter_by(
		teacher_id=teacher_id).order_by('-id').all()

	return evaluations
		

