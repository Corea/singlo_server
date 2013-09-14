# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request, render_template, current_app

from api.models import Lesson_Question, Lesson_Answer, Lesson_Answer_Image, Lesson_Evaluation
import api.lesson.queries as queries
import api.teacher.queries as teacher_queries
import api.auth.queries as auth_queries
from gcm import GCM

import os
import string
import random
import Image

mod = Blueprint('lesson', __name__, url_prefix='/lesson')


# FUNCTION START
def get_video_rotation(file_path):
	rotation = 0
	try:
		file_name = os.path.basename(file_path)[0]
		os.system('mediainfo %s | grep Rotation > /tmp/%s' % (file_path, file_name))
		f = open("/tmp/%s" % file_name, "r")
		rotation = f.read()
		f.close()
		rotation = int(rotation.split(' : ')[1].strip()[:-1])
	except Exception, e:
		rotation = 0
	return rotation

def get_recommend_by_cause(cause_id):
	if cause_id == 0:
		return [2, 4, 6, 10, 17, 23, 24, 42]
	elif cause_id == 1:
		return [6, 9, 26, 28, 44]
	elif cause_id == 2:
		return [3, 7, 8, 21, 27, 36, 41, 42]
	elif cause_id == 3:
		return [7, 22]
	elif cause_id == 4:
		return [5, 7, 12, 13, 29, 41, 42]
	elif cause_id == 5:
		return [22, 31, 35, 38, 40, 41]
	elif cause_id == 6:
		return [1, 18, 19, 20, 21, 32, 37, 38, 42, 51]
	elif cause_id == 7:
		return [15, 16, 19, 33, 34, 35, 41]
	elif cause_id == 8:
		return [3, 11, 23, 24, 39, 42, 45]
	elif cause_id == 9:
		return [8]
	elif cause_id == 10:
		return [14, 25, 30, 31, 35, 38, 43, 46, 47, 48, 49, 50]
	elif cause_id == 11:
		return [14, 14, 25, 43, 46, 46, 47]
	return [0]

def get_video_capture(file_path, current_time, target_name=None):
	if target_name is None:
		temp_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(50))
		temp_name += '.png'
	else:
		temp_name = target_name

	temp_path = os.path.join(current_app.config['CAPTURE_FOLDER'], temp_name)


	os.system('ffmpeg -i %s -ss %s -f image2 -vframes 1 %s' % (file_path, current_time, temp_path))

	image = Image.open(temp_path)
	width, height = image.size
	if width > 360: 
		height = int(height / (width / 360.))
		width = 360
		image = image.resize((width, height), Image.ANTIALIAS)
	image.save(temp_path)

	return temp_name

# FUNCTION END



@mod.route('/ask_fast', methods=['POST'])
def ask_fast():
	# 해당 기능 막아놓기로 하였음.
	return render_template('error.json')
	try:
		user_id = int(request.form['user_id'])
		teacher_id = None
		lesson_type = True
		video = None
		club_type = int(request.form['club_type'])
		question = request.form['question']

		lesson_question = Lesson_Question(
			user_id, teacher_id, False, lesson_type, 
			video, club_type, question)
		lesson_question = queries.add_lesson_question_video(lesson_question)

		#TODO: 파일 처리 완료 후 DB에 들어가게 설정

		temp_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
			'temp_' + lesson_question.video)
		file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], lesson_question.video)

		file = request.files['video']
		file.save(temp_file_path)
		os.system('/usr/local/bin/MP4Box -hint %s' % temp_file_path)
		rotation = get_video_rotation(temp_file_path)

		transpose = 0
		if rotation == 90:
			transpose = 1
		elif rotation == 180:
			transpose = 2
		elif rotation == 270:
			transpose = 3

		print transpose
		os.system("/usr/local/bin/ffmpeg -i %s -filter:v 'setpts=4.0*PTS,transpose=%s' %s" % (temp_file_path, transpose, file_path))
		try:
			with open(file_path): pass
		except:
			os.system("mv %s %s" % (temp_file_path, file_path))

		return render_template('success.json')
	except Exception:
		return render_template('error.json')

@mod.route('/ask_slow', methods=['POST'])
def ask_slow():
	gcm = GCM(current_app.config['GCM_APIKEY'])
	try:
		user_id = int(request.form['user_id'])
		teacher_id_list = request.form.getlist('teacher_id[]')
		lesson_type = False
		video = None
		thumbnail = None
		club_type = int(request.form['club_type'])
		question = request.form['question']

		if 'video' not in request.files or not request.files['video']:
			raise

		lesson_question_list = []
		for teacher_id in teacher_id_list:
			lesson_question = Lesson_Question(
				user_id, teacher_id, False, lesson_type, 
				video, club_type, question)

			if video is None:
				lesson_question = queries.add_lesson_question_video(lesson_question)
				video = lesson_question.video
				thumbnail = lesson_question.thumbnail
			else:
				lesson_question.thumbnail = thumbnail
				lesson_question = queries.add_lesson_question(lesson_question)

			lesson_question_list.append(lesson_question)
			reg_id = teacher_queries.get_teacher_reg_id(teacher_id)
			if reg_id is not None:
				gcm.plaintext_request(registration_id=reg_id, 
					data={'message':'새로운 레슨 신청이 들어왔습니다.'})

		#TODO: 파일 처리 완료 후 DB에 들어가게 설정

		temp_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
			'temp_' + lesson_question.video)
		file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], lesson_question.video)

		file = request.files['video']
		file.save(temp_file_path)
		os.system('/usr/local/bin/MP4Box -hint %s' % temp_file_path)
		rotation = get_video_rotation(temp_file_path)
		print rotation

		option = 'setpts=4.0*PTS,scale=iw/2:-1'
#		if rotation == 90:
#			option += ',transpose=1'
#		elif rotation == 180:
#			option += ',vflip,hflip'
#		elif rotation == 270:
#			option += ',transpose=2'

		os.system("/usr/local/bin/ffmpeg -i %s -vpre singlo -filter:v '%s' -an -f mp4 %s" % (temp_file_path, option, file_path))
		try:
			with open(file_path): pass
		except:
			os.system("mv %s %s" % (temp_file_path, file_path))

		get_video_capture(file_path, 0, thumbnail)

		return render_template('success.json')
	except Exception, e:
		print e
		return render_template('error.json')


@mod.route('/ask_slow_solo', methods=['POST'])
def ask_slow_solo():
	gcm = GCM(current_app.config['GCM_APIKEY'])
	try:
		user_id = int(request.form['user_id'])
		teacher_id = int(request.form['teacher_id'])
		lesson_type = False
		video = None
		club_type = int(request.form['club_type'])
		question = request.form['question']

		if 'lesson_id' in request.form:
			before_lesson = queries.get_lesson_question(request.form['lesson_id'])
			video = before_lesson.video
		elif 'video' not in request.files or not request.files['video']:
			raise

		lesson_question = Lesson_Question(
			user_id, teacher_id, False, lesson_type, 
			video, club_type, question)

		if video is None:
			lesson_question = queries.add_lesson_question_video(lesson_question)
		else:
			lesson_question = queries.add_lesson_question(lesson_question)

		# Push
		reg_id = teacher_queries.get_teacher_reg_id(teacher_id)
		if reg_id is not None:
			gcm.plaintext_request(registration_id=reg_id, 
				data={'message':'새로운 레슨 신청이 들어왔습니다.'})

		#TODO: 파일 처리 완료 후 DB에 들어가게 설정

		if video is None:
			# Video Processing
			temp_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
				'temp_' + lesson_question.video)
			file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], lesson_question.video)
			file = request.files['video']
			file.save(temp_file_path)

			try:
				os.system('/usr/local/bin/MP4Box -hint %s' % temp_file_path)
				rotation = get_video_rotation(temp_file_path)
				print rotation

				option = 'setpts=4.0*PTS'
				if rotation == 90:
					option += ',transpose=1'
				elif rotation == 180:
					option += ',vflip,hflip'
				elif rotation == 270:
					option += ',transpose=2'

				os.system("/usr/local/bin/ffmpeg -i %s -filter:v '%s' -y -an  -vpre singlo -f mp4 -threads 0 %s" % (temp_file_path, option, file_path))
			except:
				pass

			try:
				with open(file_path): pass
			except:
				os.system("mv %s %s" % (temp_file_path, file_path))

		return render_template('ask.json', lesson=lesson_question)
	except Exception, e:
		print e
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
		# recommend1 = int(request.form['recommend1'])
		# recommend2 = int(request.form['recommend2'])
		recommend1 = 0
		recommend2 = 0

		lesson_question = queries.get_lesson_question(lesson_id)

		# DB에 남아있는거 잘 업데이트하기 
		if lesson_question.teacher_id != None and lesson_question.teacher_id != teacher_id:
			return render_template('error.json')
		lesson_question.status = False
		if lesson_question.status:
			return render_template('error.json')

		# TODO: this rountines muste be in queries.py
		lesson_question.teacher_id = teacher_id
		lesson_question.status = True
		# END TODO

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
			timing = request.form['timing' + str(i)]

			lesson_answer_image = Lesson_Answer_Image(i, 
					lesson_answer.id, file_name, line, timing)
			queries.add_lesson_answer_image(lesson_answer_image)

		# 회원에게 레슨 처리됨을 푸시로 알리기
		gcm = GCM(current_app.config['GCM_APIKEY'])
		try:
			user_id = queries.get_lesson_user_id(lesson_id)
			reg_id = auth_queries.get_reg_id(user_id)
			if reg_id is not None and reg_id != '':
				gcm.plaintext_request(registration_id=reg_id, 
					data={'title':'싱글로', 'message':'신청한 레슨 강습이 완료되었습니다.'})
		except:
			pass

		return render_template('success.json')
	except Exception, e:
		print e
		return render_template('error.json')

@mod.route('/get_list', methods=['POST'])
def get_list():
	teacher_id = int(request.form['teacher_id'])
	lessons = queries.get_all_lesson(teacher_id)
	return render_template('get_lesson_list.json', lessons=lessons)

@mod.route('/get_list_user', methods=['POST'])
def get_list_user():
	user_id = int(request.form['user_id'])
	lessons = queries.get_all_lesson_by_user(user_id)
	return render_template('get_lesson_list.json', lessons=lessons)


@mod.route('/get_answer', methods=['POST'])
def get_answer():
	lesson_id = int(request.form['lesson_id'])
	lesson = queries.get_lesson_answer(lesson_id)
	images = queries.get_lesson_answer_image(lesson.id)
	recommends = get_recommend_by_cause(lesson.cause)
	return render_template('get_lesson_answer.json', 
		lesson=lesson, images=images, recommends=recommends)

@mod.route('/get_video_capture', methods=['POST'])
def post_get_video_capture():
	try:
		lesson_id = int(request.form['lesson_id'])
		current_position = int(request.form['current_position'])
		current_time = "%s:%s:%s.%s" % (current_position / 10000000,
			(current_position / 100000) % 100, 
			(current_position / 1000) % 100, current_position % 1000)

		lesson_question = queries.get_lesson_question(lesson_id)
		file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], lesson_question.video)
		
		temp_name = get_video_capture(file_path, current_time)
		return render_template('get_video_capture.json', path=temp_name)
	except Exception, e:
		print e
		return render_template('error.json')

@mod.route('/evaluation', methods=['POST'])
def evaluation():
	try:
		user_id = int(request.form['user_id'])
		lesson_id = int(request.form['lesson_id'])
		review = request.form['review']
		speed = float(request.form['speed'])
		accuracy = float(request.form['accuracy'])
		price = float(request.form['price'])
		recommend = int(request.form['recommend'])
		if recommend == 1: 
			recommend = True
		else:
			recommend = False

		lesson_question = queries.get_lesson_question(lesson_id)
		if lesson_question.evaluation_status:
			raise

		lesson_evaluation = Lesson_Evaluation(lesson_question.id, 
			lesson_question.teacher_id, review, speed, accuracy, price, recommend)
		queries.add_lesson_evaluation(lesson_question, lesson_evaluation)

		return render_template('success.json')
	except Exception, e:
		print e
		return render_template('error.json')

@mod.route('/get_unconfirm_count', methods=['POST'])
def get_unconfirm_count():
	try:
		user_id = int(request.form['user_id'])
		count = auth_queries.count_unconfirm_question(user_id)
		return render_template('count.json', count=count)
	except Exception, e:
		print e
		return render_template('error.json')

@mod.route('/get_evaluation', methods=['GET'])
def get_evaluation():
	try:
		teacher_id = int(request.args.get('teacher_id', 0))
		evaluations = queries.get_all_evaluation(teacher_id)
		return render_template('get_evaluation.json', evaluations=evaluations)
	except Exception, e:
		print e
		return render_template('error.json')
