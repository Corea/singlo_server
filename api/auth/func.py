# -*- coding: utf-8 -*-

import time

def get_timestamp():
	return int(time.time())

def get_user_photo_path(user_id):
	return 'user_' + str(user_id) + '_' + str(get_timestamp()) + '.png'

def get_teacher_photo_path(teacher_id):
	return 'teacher_' + str(teacher_id) + '_' + str(get_timestamp()) + '.png'
