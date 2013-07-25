# -*- coding: utf-8 -*-

from api import db
from api.models import Teacher, User_Teacher_Like

def get_teacher(teacher_id):
	teacher = Teacher.query.filter_by(
		teacher_id=teacher_id).first()
	
def get_all_teacher():
	teachers = Teacher.query.all()

	return teachers

def get_user_teacher_like(user_id, teacher_id):
	user_teacher_like = User_Teacher_Like.query.filter_by(
		user_id=user_id, teacher_id=teacher_id).first()

	return user_teacher_like

def add_user_teacher_like(user_id, teacher_id, status):
	user_teacher_like = get_user_teacher_like(user_id, teacher_id)
	if user_teacher_like is None:
		user_teacher_like = User_Teacher_Like(
			user_id, teacher_id, status)
		db.session.add(user_teacher_like)
	else:
		user_teacher_like.status = status
	db.session.commit()

