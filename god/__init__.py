# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import login_required
from flask.ext.security import Security, SQLAlchemyUserDatastore

from urllib import unquote

app = Flask(__name__)
app.config.from_object('god.config')

db = SQLAlchemy()
db.init_app(app)
with app.app_context():
	db.create_all()

import god.models as models

admin_datastore = SQLAlchemyUserDatastore(db, models.Admin, models.Admin_Role)
security = Security(app, admin_datastore)


@app.template_filter('decode')
def urldecode(text):
	try:
		text = unquote(text).decode('utf8')
	except:
		text = text.encode('ASCII')
		text = unquote(text).decode('utf8')
	return text

#@app.errorhandler(404)
#def not_found(error):
#	return render_template('404.html'), 404

@app.route("/")
@login_required
def god():
	versions = models.Version.query.all()

	return render_template('index.html', versions=versions)


from god.teacher.views import mod as teacherModule
from god.user.views import mod as userModule
from god.order.views import mod as orderModule
from god.event.views import mod as eventModule
from god.notice.views import mod as noticeModule
from god.qna.views import mod as qnaModule
app.register_blueprint(teacherModule)
app.register_blueprint(userModule)
app.register_blueprint(orderModule)
app.register_blueprint(eventModule)
app.register_blueprint(noticeModule)
app.register_blueprint(qnaModule)

