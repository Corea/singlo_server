# -*- coding: utf-8 -*-

from god import db

from flask.ext.security import UserMixin, RoleMixin

from datetime import datetime



class Environment(db.Model):
	__tablename__ = 'singlo_environment'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	key = db.Column(db.String(128), nullable=False, primary_key=True)
	value = db.Column(db.String(128), nullable=False)

	def __init__(self):
		pass


# User & Teacher 
class User(db.Model):
	__tablename__ = 'singlo_user'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False)
	birthday = db.Column(db.String(31), nullable=False)
	phone = db.Column(db.String(31), nullable=False, unique=True)
	photo = db.Column(db.String(63), nullable=True)
	phone_model = db.Column(db.String(128), nullable=True, default=None)
	created_datetime = db.Column(db.DateTime, nullable=True, default=datetime.now)
	lastlogin_datetime = db.Column(db.DateTime, nullable=True, default=datetime.now)
	pushtoken = db.Column(db.String(200), nullable=True)
	active = db.Column(db.Boolean, nullable=False, default=True)
	point = db.Column(db.Integer, nullable=False, default=0)
	
	def __init__(self, name, birthday, phone, pushtoken, photo=None, phone_model=None):
		self.name = name
		self.birthday = birthday
		self.phone = phone
		self.pushtoken = pushtoken
		self.photo = photo
		self.phone_model = phone_model

	def set_password(password):
		pass

class Teacher(db.Model):
	__tablename__ = 'singlo_teacher'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False)
	birthday = db.Column(db.String(31), nullable=False)
	phone = db.Column(db.String(31), nullable=False, unique=True)
	photo = db.Column(db.String(63), nullable=True)
	company = db.Column(db.String(256), nullable=False)
	certification = db.Column(db.String(256), nullable=False)
	status = db.Column(db.Boolean, nullable=False, default=True)
	status_message = db.Column(db.String(255), nullable=False, default='')
	price = db.Column(db.Integer, nullable=False)
	profile = db.Column(db.Text, nullable=False)
	url = db.Column(db.String(127), nullable=False)
	active = db.Column(db.Boolean, nullable=False, default=True)
	phone_model = db.Column(db.String(128), nullable=True, default=None)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	lastlogin_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	pushtoken = db.Column(db.String(200), nullable=True)
	push_active = db.Column(db.Boolean, nullable=False, default=True)
	revenue = db.Column(db.Integer, nullable=False, default=0)

	def __init__(self):
		pass



class Event(db.Model):
	__tablename__ = 'singlo_event'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	image = db.Column(db.String(128), nullable=True)
	start_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	end_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

	def __init__(self):
		pass

class Blog_Article(db.Model):
	__tablename__ = 'singlo_blog_article'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}
	
	id = db.Column(db.Integer, primary_key=True)
	guid = db.Column(db.String(128), nullable=False, default='', unique=True)
	link = db.Column(db.String(128), nullable=False, default='')
	thumbnail = db.Column(db.String(256), nullable=False, default='')
	title = db.Column(db.Text, nullable=False, default='')
	tag = db.Column(db.Text, nullable=False, default='')
	description = db.Column(db.Text, nullable=False, default='')
	created_datetime = db.Column(db.DateTime, nullable=False)

	def __init__(self, article):
		self.guid = article.guid
		self.link = article.link
		self.title = article.title
		self.tag = article.tag
		self.description = article.description
		self.created_datetime = datetime.strptime(article.published, 
			'%a, %d %b %Y %H:%M:%S +0900')


# Golfbag
class Item(db.Model):
	__tablename__ = 'singlo_item'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False, default='')
	price = db.Column(db.Integer, nullable=False)
	count = db.Column(db.Integer, nullable=False)
	android_name = db.Column(db.String(128), nullable=False, default='')
	description = db.Column(db.String(512), nullable=False, default='')
	image = db.Column(db.String(128), nullable=False, default='')

	def __init__(self, title, price, count, android_name, description='', image=''):
		self.title = title
		self.price = price
		self.count = count
		self.android_name = android_name
		self.description = description
		self.image = image

class Purchase(db.Model):
	__tablename__ = 'singlo_purchase'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_user.id'), nullable=False)
	user = db.relationship('User')
	item_id = db.Column(db.Integer, 
		db.ForeignKey('singlo_item.id'), nullable=False)
	item = db.relationship('Item')
	token = db.Column(db.String(256), nullable=True, default=None)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	
	def __init__(self, user_id, item_id, token):
		self.user_id = user_id
		self.item_id = item_id
		self.token = token



# Board
class Notice(db.Model):
	__tablename__ = 'singlo_notice'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False)
	content = db.Column(db.Text, nullable=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	modified_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	
	def __init__(self, title, content):
		self.title = title
		self.content = content

class Qna(db.Model):
	__tablename__ = 'singlo_qna'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False)
	content = db.Column(db.Text, nullable=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	modified_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	
	def __init__(self, title, content):
		self.title = title
		self.content = content



# Teacher List
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



# Lesson
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
	thumbnail = db.Column(db.String(128), nullable=True, default=None)
	club_type = db.Column(db.Integer, nullable=False)
	question = db.Column(db.Text, nullable=False)
	evaluation_status = db.Column(db.Boolean, nullable=False, default=False)
	created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
	price = db.Column(db.Integer, nullable=False, default=0)

	def __init__(self, user_id, teacher_id, status, lesson_type, video, club_type, question, price=0):
		self.user_id = user_id
		self.teacher_id = teacher_id
		self.status = status
		self.lesson_type = lesson_type
		self.video = video
		self.club_type = club_type
		self.question = question
		self.price = price

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
	timing = db.Column(db.Integer, nullable=False)

	def __init__(self, number, answer_id, image, line, timing):
		self.number = number
		self.answer_id = answer_id
		self.image = image
		self.line = line
		self.timing = timing

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


# ADMIN
roles_users = db.Table('roles_users',
	db.Column('singlo_admin_id', db.Integer(), db.ForeignKey('singlo_admin.id')),
	db.Column('singlo_admin_role_id', db.Integer(), db.ForeignKey('singlo_admin_role.id')))

class Admin_Role(db.Model, RoleMixin):
	__tablename__ = 'singlo_admin_role'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

	
class Admin(db.Model, UserMixin):
	__tablename__ = 'singlo_admin'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	roles = db.relationship('Admin_Role', secondary=roles_users,
		backref=db.backref('users', lazy='dynamic'))

	def __str__(self):
		return '<User id=%s email=%s>' % (self.id, self.email)



