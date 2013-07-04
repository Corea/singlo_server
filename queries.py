# -*- coding: utf-8 -*-

from models import * 




def get_valid_user(email, password):
	user = User.query.filter_by(
		email=email, password=password).first()

	print user 

	if user is not None:
		user.lastlogin_datetime = datetime.now()
		db.session.commit()

	return user

def get_all_teacher():
	teachers = Teacher.query.all()

	return teachers
