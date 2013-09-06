# -*- coding: utf-8 -*-

from god import db as god_db
from god.models import Lesson_Question
from api.auth.func import get_timestamp

import urllib

def get_all_lessons():
	lessons = Lesson_Question.query.all()

	return lessons

