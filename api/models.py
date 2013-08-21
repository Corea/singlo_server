# -*- coding: utf-8 -*-

from api import db

from datetime import datetime


class User(db.Model):
	__tablename__ = 'singlo_user'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(31), nullable=False)
	birthday = db.Column(db.String(31), nullable=False)
	phone = db.Column(db.String(31), nullable=False, unique=True)
	photo = db.Column(db.String(63), nullable=True)
	created_datetime = db.Column(db.DateTime, nullable=True, default=datetime.now)
	lastlogin_datetime = db.Column(db.DateTime, nullable=True, default=datetime.now)
	pushtoken = db.Column(db.String(200), nullable=True)
	
	def __init__(self, name, birthday, phone, photo=None, pushtoken=None,):
		self.name = name
		self.birthday = birthday
		self.phone = phone
		self.photo = photo
		self.pushtoken = pushtoken

	def set_password(password):
		pass


class Teacher(db.Model):
	__tablename__ = 'singlo_teacher'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(31), nullable=False)
	birthday = db.Column(db.String(31), nullable=False)
	phone = db.Column(db.String(31), nullable=False, unique=True)
	photo = db.Column(db.String(63), nullable=True)
	company = db.Column(db.String(63), nullable=False)
	certification = db.Column(db.String(63), nullable=False)
	status = db.Column(db.Boolean, nullable=False, default=True)
	status_message = db.Column(db.String(255), nullable=False, default='')
	price = db.Column(db.Integer, nullable=False)
	profile = db.Column(db.Text, nullable=False)
	url = db.Column(db.String(127), nullable=False)
	active = db.Column(db.Boolean, nullable=False, default=True)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	lastlogin_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	pushtoken = db.Column(db.String(200), nullable=True)

	def __init__(self):
		pass

class User_Teacher_Like(db.Model):
	__tablename__ = 'singlo_user_teacher_like'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	user_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_user.id'), primary_key=True)
	teacher_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_teacher.id'), primary_key=True)
	status = db.Column(db.Boolean, nullable=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

	def __init__(self, user_id, teacher_id, status):
		self.user_id = user_id
		self.teacher_id = teacher_id
		self.status = status


class Lesson_Training(db.Model):
	__tablename__ = 'singlo_lesson_training'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}
	
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(127), nullable=False)

class Lesson_Question(db.Model):
	__tablename__ = 'singlo_lesson_question'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}
	
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_user.id'), nullable=False)
	user = db.relationship('User')
	teacher_id = db.Column(db.Integer, nullable=True, default=None)
	status = db.Column(db.Boolean, nullable=False)
	lesson_type = db.Column(db.Boolean, nullable=False)
	video = db.Column(db.String(63), nullable=True, default=None)
	club_type = db.Column(db.Integer, nullable=False)
	question = db.Column(db.Text, nullable=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

	def __init__(self, user_id, teacher_id, status, lesson_type, video, club_type, question):
		self.user_id = user_id
		self.teacher_id = teacher_id
		self.status = status
		self.lesson_type = lesson_type
		self.video = video
		self.club_type = club_type
		self.question = question

class Lesson_Answer(db.Model):
	__tablename__ = 'singlo_lesson_answer'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	question_id = db.Column(db.Integer,
		db.ForeignKey('singlo_lesson_question.id'), nullable=False)
	question = db.relationship('Lesson_Question')
	score1 = db.Column(db.Integer, nullable=False, default=0)
	score2 = db.Column(db.Integer, nullable=False, default=0)
	score3 = db.Column(db.Integer, nullable=False, default=0)
	score4 = db.Column(db.Integer, nullable=False, default=0)
	score5 = db.Column(db.Integer, nullable=False, default=0)
	score6 = db.Column(db.Integer, nullable=False, default=0)
	score7 = db.Column(db.Integer, nullable=False, default=0)
	score8 = db.Column(db.Integer, nullable=False, default=0)
	sound = db.Column(db.String(63), nullable=False)
	cause = db.Column(db.Integer, nullable=False, default=0)
	recommend1 = db.Column(db.Integer, nullable=False, default=0)
	recommend2 = db.Column(db.Integer, nullable=False, default=0)
	confirm_status = db.Column(db.Boolean, nullable=False, default=False)
	evaluation_status = db.Column(db.Boolean, nullable=False, default=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

	def __init__(self, question_id, score1, score2, score3, score4, score5, 
		score6, score7, score8, sound, cause, recommend1, recommend2):
		self.question_id = question_id
		self.score1 = score1
		self.score2 = score2
		self.score3 = score3
		self.score4 = score4
		self.score5 = score5
		self.score6 = score6
		self.score7 = score7
		self.score8 = score8
		self.sound = sound
		self.cause = cause
		self.recommend1 = recommend1
		self.recommend2 = recommend2

class Lesson_Answer_Image(db.Model):
	__tablename__ = 'singlo_lesson_answer_image'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer, nullable=False)
	answer_id = db.Column(db.Integer,
		db.ForeignKey('singlo_lesson_answer.id'), nullable=False)
	answer = db.relationship('Lesson_Answer')
	image = db.Column(db.String(63), nullable=False)
	line = db.Column(db.Text, nullable=False, default='')

	def __init__(self, number, answer_id, image, line):
		self.number = number
		self.answer_id = answer_id
		self.image = image
		self.line = line

class Lesson_Evaluation(db.Model):
	__tablename__ = 'singlo_lesson_evaluation'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	question_id = db.Column(db.Integer,
		db.ForeignKey('singlo_lesson_question.id'), nullable=False)
	question = db.relationship('Lesson_Question')
	teacher_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_teacher.id'), nullable=False)
	teacher = db.relationship('Teacher')
	review = db.Column(db.Text, nullable=False)
	speed = db.Column(db.Float, nullable=False)
	accuracy = db.Column(db.Float, nullable=False)
	price = db.Column(db.Float, nullable=False)
	recommend = db.Column(db.Boolean, nullable=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

	def __init__(self, question_id, teacher_id, review, speed, accuracy, price, recommend):
		self.question_id = question_id
		self.teacher_id = teacher_id
		self.review = review
		self.speed = speed
		self.accuracy = accuracy
		self.price = price
		self.recommend = recommend
