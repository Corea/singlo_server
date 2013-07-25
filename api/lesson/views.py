# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request, render_template, current_app

from api.models import Lesson_Question, Lesson_Answer, Lesson_Answer_Image
import api.lesson.queries as queries

import os

mod = Blueprint('lesson', __name__, url_prefix='/lesson')

@mod.route('/ask', methods=['POST'])
def ask():
	try:
		user_id = int(request.form['user_id'])
		teacher_id = None
		if 'teacher_id' in request.form and request.form['teacher_id'] is not None:
			teacher_id = int(request.form['teacher_id'])
		lesson_type = True
		video = None
		club_type = int(request.form['club_type'])
		question = request.form['question']

		lesson_question = Lesson_Question(
			user_id, teacher_id, False, lesson_type, 
			video, club_type, question)
		lesson_question = queries.add_lesson_question(lesson_question)
		file = request.files['video']
		file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], lesson_question.video)
		file.save(file_path)
		os.system('/usr/local/bin/MP4Box -hint %s' % file_path)

		return render_template('success.json')
	except Exception:
		return render_template('error.json')

@mod.route('/answer', methods=['POST'])
def answer():
	try:
		lesson_id = int(request.form['lesson_id'])
		teacher_id = int(request.form['teacher_id'])
		image_count = int(request.form['image_count'])
		score1 = int(request.form['score0'])
		score2 = int(request.form['score1'])
		score3 = int(request.form['score2'])
		score4 = int(request.form['score3'])
		score5 = int(request.form['score4'])
		score6 = int(request.form['score5'])
		score7 = int(request.form['score6'])
		score8 = int(request.form['score7'])
		cause = int(request.form['cause'])
		recommend1 = int(request.form['recommend1'])
		recommend2 = int(request.form['recommend2'])

		lesson_question = queries.get_lesson_question(lesson_id)

		# DB에 남아있는거 잘 업데이트하기 
		if lesson_question.teacher_id != None and lesson_question.teacher_id != teacher_id:
			return render_template('error.json')
		if lesson_question.status:
			return render_template('error.json')

		lesson_question.teacher_id = teacher_id
		lesson_question.status = True

		lesson_answer = Lesson_Answer(lesson_id, score1, score2, score3,
			score4, score5, score6, score7, score8, '', cause, recommend1, recommend2)
		queries.add_lesson_answer(lesson_answer)

		file = request.files['audio']
		file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
			lesson_answer.sound)
		file.save(file_path)

		for i in xrange(image_count):
			file = request.files['image' + str(i)]
			file_name = str(lesson_answer.id) + '_image_' + str(i) + '.png'
			file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
			file.save(file_path)
			
			line = request.form['line' + str(i)]
			lesson_answer_image = Lesson_Answer_Image(i, 
				lesson_answer.id, file_name, line)
			queries.add_lesson_answer_image(lesson_answer_image)
		return render_template('success.json')
	except Exception:
		return render_template('error.json')



@mod.route('/get_list', methods=['POST'])
def get_list():
	if request.method == 'POST':
		teacher_id = int(request.form['teacher_id'])
		lessons = queries.get_all_lesson(teacher_id)
		return render_template('get_lesson_list.json', lessons=lessons)
	else:
		return render_template('error.json')

@mod.route('/get_list_user', methods=['POST'])
def get_list_user():
	if request.method == 'POST':
		user_id = int(request.form['user_id'])
		lessons = queries.get_all_lesson_by_user(user_id)
		return render_template('get_lesson_list.json', lessons=lessons)
	else:
		return render_template('error.json')


@mod.route('/get_answer', methods=['POST'])
def get_answer():
	if request.method == 'POST':
		lesson_id = int(request.form['lesson_id'])
		lesson = queries.get_lesson_answer(lesson_id)
		images = queries.get_lesson_answer_image(lesson.id)
		return render_template('get_lesson_answer.json', lesson=lesson, images=images)
	else: 
		return render_template('error.json')


