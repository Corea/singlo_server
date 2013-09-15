# -*- coding: utf-8 -*-

from god import db as god_db
from god.models import Event
from api.auth.func import get_timestamp

import urllib

def get_all_event():
	events = Event.query.all()
	
	return events

def get_event(event_id):
	event = Event.query.filter_by(id=event_id).first()

	return event

def add_event(start_datetime, end_datetime, image):
	event = Event()
	event.start_datetime = start_datetime
	event.end_datetime = end_datetime
	god_db.session.add(event)
	god_db.session.commit()
	event.image = 'event_' + str(event.id) + '_' + str(get_timestamp()) + '.png'
	god_db.session.commit()

	return event

def modify_event(event, start_datetime, end_datetime, image=None):
	event.start_datetime = start_datetime
	event.end_datetime = end_datetime
	if image is not None:
		event.image = 'event_' + str(event.id) + '_' + str(get_timestamp()) + '.png'
	god_db.session.commit()

	return event

def delete_event(event_id):
	event = get_event(event_id)
	god_db.session.delete(event)
	god_db.session.commit()
