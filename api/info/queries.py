# -*- coding: utf-8 -*-

from api.models import Teacher

def get_all_teacher():
	teachers = Teacher.query.all()

	return teachers
