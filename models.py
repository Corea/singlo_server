# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'singlo_user'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(31), nullable=False)
	phone = db.Column(db.String(31), nullable=False)
	email = db.Column(db.String(63), nullable=False, unique=True)
	password = db.Column(db.String(63), nullable=False, default=None)
	photo = db.Column(db.String(63), nullable=True)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	lastlogin_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	
	def __init__(self, name, phone, email, password, photo=None):
		self.name = name
		self.phone = phone
		self.email = email
		self.password = password
		self.photo = photo

	def set_password(password):
		pass


class Teacher(db.Model):
	__tablename__ = 'singlo_teacher'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(31), nullable=False)
	phone = db.Column(db.String(31), nullable=False)
	email = db.Column(db.String(63), nullable=False, unique=True)
	password = db.Column(db.String(63), nullable=False, default=None)
	photo = db.Column(db.String(63), nullable=True)
	company = db.Column(db.String(63), nullable=False)
	certification = db.Column(db.String(63), nullable=False)
	lessons = db.Column(db.String(63), nullable=False)
	video_available = db.Column(db.Boolean, nullable=False)
	price = db.Column(db.Integer, nullable=False)
	profile = db.Column(db.Text, nullable=False)
	url = db.Column(db.String(127), nullable=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	lastlogin_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

	def __init__(self):
		pass

class User_Teacher_Like(db.Model):
	__tablename__ = 'singlo_user_teacher_like'

	user_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_user.id'), primary_key=True)
	teacher_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_teacher.id'), primary_key=True)
	status = db.Column(db.Boolean, nullable=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Lesson_Symptom(db.Model):
	__tablename__ = 'singlo_lesson_symptom'
	
	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.String(127), nullable=False)
	title = db.Column(db.String(127), nullable=False)

class Lesson_Training(db.Model):
	__tablename__ = 'singlo_lesson_training'
	
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(127), nullable=False)

class Lesson_Question(db.Model):
	__tablename__ = 'singlo_lesson_question'
	
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_user.id'))
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

	
 


