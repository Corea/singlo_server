# -*- coding: utf-8 -*-

from god import db as god_db
from god.models import Notice
from api.auth.func import get_timestamp

from datetime import datetime

import urllib


def get_notice(notice_id):
	notice = Notice.query.filter_by(id=notice_id).first()

	return notice
def get_all_notices():
	notices = Notice.query.order_by(Notice.id)

	return notices

def add_notice(title, content):
	title = urllib.quote(title.encode('utf8'))
	content = urllib.quote(content.encode('utf8'))

	notice = Notice(title, content)
	god_db.session.add(notice)
	god_db.session.commit()

	return notice

def modify_notice(notice, title, content):
	notice.title = urllib.quote(title.encode('utf8'))
	notice.content = urllib.quote(content.encode('utf8'))
	notice.modified_datetime = datetime.now()
	god_db.session.commit()

	return notice
	
def delete_notice(notice_id):
	notice = get_notice(notice_id)
	god_db.session.delete(notice)
	god_db.session.commit()
