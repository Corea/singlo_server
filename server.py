# -*- coding: utf-8 -*-

from models import * 
import queries 

from flask import Flask
from flask import request
from flask import render_template

import urllib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:singlogolf@34@localhost/garagestory'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'video')

app.debug = True

db.init_app(app)
with app.app_context():
	db.create_all()

@app.route('/login', methods=['POST'])
def hello():
	if request.method == 'POST':
		user = queries.get_valid_user(
				request.form['email'],
				request.form['password'])
		if user is None:
			return render_template('error.json')
		else:
			return render_template('login.json', user=user)
	else:
		return render_template('error.json')

@app.route('/get_teacher_list', methods=['GET', 'POST'])
def get_teacher_list():
	teachers = queries.get_all_teacher()
	return render_template('get_teacher_list.json', teachers=teachers)

@app.route('/ask_lesson_question', methods=['POST'])
def ask_lesson_question():
	if request.method == 'POST':
		try:
			user_id = int(request.form['user_id'])
			teacher_id = None
			if 'teacher_id' in request.form and request.form['teacher_id'] is not None:
				teacher_id = int(request.form['teacher_id'])
			lesson_type = True
			video = None
			club_type = int(request.form['club_type'])

			try:
				question = urllib.unquote(request.form['question'])
			except Exception:
				question = request.form['question']

			lesson_question = Lesson_Question(user_id, teacher_id, False, lesson_type, video, club_type, question)
			db.session.add(lesson_question)
			db.session.commit()
			
			lesson_question.video = str(lesson_question.id) + '_question'
			db.session.commit()
			file = request.files['video']
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], lesson_question.video))

			return render_template('success.json')
		except Exception:
			return render_template('error.json')
	else: 
		return render_template('eror.json')

if __name__ == "__main__":
	app.run(host='0.0.0.0')

