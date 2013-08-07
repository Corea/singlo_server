# -*- coding: utf-8 -*-
from flask import request, render_template
from flask import Blueprint

import api.teacher.queries as queries

mod = Blueprint('teacher', __name__, url_prefix='/teacher')

@mod.route('/get_list', methods=['POST'])
def get_list():
	try:
		user_id = int(request.form['user_id'])
		teachers = queries.get_all_teacher()
		new_teachers = []
		for teacher in teachers: 
			new_teachers.append([teacher, 
				queries.get_user_teacher_like(user_id, teacher.id)])
			
		return render_template('get_teacher_list.json', teachers=new_teachers)
	except:
		return render_template('error.json')

@mod.route('/like', methods=['POST'])
def like():
	try:
		user_id = int(request.form['user_id'])
		teacher_id = int(request.form['teacher_id'])
		status = int(request.form['status'])
		queries.add_user_teacher_like(
			user_id, teacher_id, status == 1)
		print user_id, teacher_id, status 
		return render_template('success.json')
	except:
		return render_template('error.json')
		
