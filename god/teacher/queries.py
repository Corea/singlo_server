# -*- coding: utf-8 -*-

from api import db as api_db
from god import db as god_db
from api.models import Teacher
from api.auth.func import get_timestamp

import urllib

def get_all_teacher():
	teachers = Teacher.query.all()

	return teachers

def get_active_teacher():
	teachers = Teacher.query.filter_by(active=True)

	return teachers

def get_teacher(id):
	teacher = Teacher.query.filter_by(id=id).first()

	return teacher

def add_teacher(name, birthday, phone, photo=None, company="", \
	certification="", video_available=True, price=0, profile="", url=""):
	teacher = Teacher()
	teacher.name = urllib.quote(name.encode('utf8'))
	teacher.birthday = urllib.quote(birthday.encode('utf8'))
	teacher.phone = urllib.quote(phone.encode('utf8'))
	teacher.photo = None
	teacher.pushtoken = None
	teacher.company = urllib.quote(company.encode('utf8'))
	teacher.certification = urllib.quote(certification.encode('utf8'))
	teacher.video_available = video_available
	teacher.price = price
	teacher.profile = urllib.quote(profile.encode('utf8'))
	teacher.url = urllib.quote(url.encode('utf8'))
	api_db.session.add(teacher)
	api_db.session.commit()
	if photo is not None:
		teacher.photo = 'teacher_' + str(teacher.id) + '_' + str(get_timestamp()) + '.png'
	api_db.session.commit()

	return teacher

def modify_teacher(teacher, name, birthday, phone, photo=None, \
	company="", certification="", video_available=True, price=0, profile="", url=""):
	teacher.name = urllib.quote(name.encode('utf8'))
	teacher.birthday = urllib.quote(birthday.encode('utf8'))
	teacher.phone = urllib.quote(phone.encode('utf8'))
	teacher.company = urllib.quote(company.encode('utf8'))
	teacher.certification = urllib.quote(certification.encode('utf8'))
	teacher.video_available = video_available
	teacher.price = price
	teacher.profile = urllib.quote(profile.encode('utf8'))
	teacher.url = urllib.quote(url.encode('utf8'))
	if photo is not None:
		teacher.photo = urllib.quote(photo.encode('utf8'))
	api_db.session.commit()

	return teacher

def delete_teacher(id):
	teacher = get_teacher(id)
	teacher.active = False
	api_db.session.commit()

def delete_photo(id):
	teacher = get_teacher(id)
	teacher.photo = None
	api_db.session.commit()
