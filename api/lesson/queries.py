# -*- coding: utf-8 -*-

from api import db
from api.models import Lesson_Question, Lesson_Answer, Lesson_Answer_Image, Lesson_Training

def add_lesson_question_video(lesson_question):
	db.session.add(lesson_question)
	db.session.commit()
	lesson_question.video = str(lesson_question.id) + '_question.avi'
	db.session.commit()

	return lesson_question

def add_lesson_question(lesson_question):
	db.session.add(lesson_question)
	db.session.commit()

	return lesson_question


def get_lesson_question(lesson_id):
	lesson = Lesson_Question.query.filter_by(
		id=lesson_id).first()

	return lesson

def get_lesson_user_id(lesson_id):
        lesson = Lesson_Question.query.filter_by(id=lesson_id).first()

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
		teacher_id=teacher_id).all()
	lessons2 = Lesson_Question.query.filter_by(
		teacher_id=None, status=False).all()

	lessons = lessons1 + lessons2 

	return lessons

def get_all_lesson_by_user(user_id):
	lessons = Lesson_Question.query.filter_by(
		user_id=user_id).all()

	return lessons


def add_lesson_evaluation(lesson_question, lesson_evaluation):
	lesson_question.evaluation_status = True
	db.session.add(lesson_evaluation)
	db.session.commit()
