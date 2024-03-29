# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config.from_object('api.config')

db = SQLAlchemy(app)
db.init_app(app)
#with app.app_context():
#	db.create_all()

#@app.errorhandler(404)
#def not_found(error):
#	return render_template('404.html'), 404

@app.route('/video/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/capture/<filename>')
def captured_file(filename):
	return send_from_directory(app.config['CAPTURE_FOLDER'], filename)

@app.route('/profile/<filename>')
def profile_file(filename):
	return send_from_directory(app.config['PROFILE_FOLDER'], filename)

@app.route('/event/<filename>')
def event_file(filename):
	return send_from_directory(app.config['EVENT_FOLDER'], filename)

from api.auth.views import mod as authModule
from api.teacher.views import mod as teacherModule
from api.lesson.views import mod as lessonModule
from api.purchase.views import mod as purchaseModule
app.register_blueprint(authModule)
app.register_blueprint(teacherModule)
app.register_blueprint(lessonModule)
app.register_blueprint(purchaseModule)


