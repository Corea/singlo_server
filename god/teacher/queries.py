# -*- coding: utf-8 -*-

from god import db
from api.models import Teacher

import urllib

def get_all_teacher():
	teachers = Teacher.query.all()

	return teachers

def add_teacher(name, birthday, phone, photo=None, company="", \
	certification="", lessons="", video_available=True, \
	price=0, profile="", url=""):
	teacher = Teacher()
	teacher.name = urllib.quote_plus(name.encode('utf8'))
	teacher.birthday = urllib.quote_plus(birthday.encode('utf8'))
	teacher.phone = urllib.quote_plus(phone.encode('utf8'))
	if teacher.photo is None:
		teacher.photo = None
	else:
		teacher.photo = urllib.quote_plus(photo.encode('utf8'))
	teacher.company = urllib.quote_plus(company.encode('utf8'))
	teacher.certification = urllib.quote_plus(certification.encode('utf8'))
	teacher.lessons = urllib.quote_plus(lessons.encode('utf8'))
	teacher.video_available = video_available
	teacher.price = price
	teacher.profile = urllib.quote_plus(profile.encode('utf8'))
	teacher.url = urllib.quote_plus(url.encode('utf8'))
	db.session.add(teacher)
	db.session.commit()


