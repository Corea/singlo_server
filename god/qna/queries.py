# -*- coding: utf-8 -*-

from god import db as god_db
from god.models import Qna
from api.auth.func import get_timestamp

from datetime import datetime

import urllib


def get_qna(qna_id):
	qna = Qna.query.filter_by(id=qna_id).first()

	return qna
def get_all_qnas():
	qnas = Qna.query.order_by(Qna.id)

	return qnas

def add_qna(title, content):
	title = urllib.quote(title.encode('utf8'))
	content = urllib.quote(content.encode('utf8'))

	qna = Qna(title, content)
	god_db.session.add(qna)
	god_db.session.commit()

	return qna

def modify_qna(qna, title, content):
	qna.title = urllib.quote(title.encode('utf8'))
	qna.content = urllib.quote(content.encode('utf8'))
	qna.modified_datetime = datetime.now()
	god_db.session.commit()

	return qna
	
def delete_qna(qna_id):
	qna = get_qna(qna_id)
	god_db.session.delete(qna)
	god_db.session.commit()
