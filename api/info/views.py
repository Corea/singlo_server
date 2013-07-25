# -*- coding: utf-8 -*-
from flask import render_template
from flask import Blueprint

import api.info.queries as queries

mod = Blueprint('info', __name__, url_prefix='/info')

@mod.route('/get_teacher_list', methods=['GET', 'POST'])
def get_teacher_list():
	teachers = queries.get_all_teacher()
	return render_template('get_teacher_list.json', teachers=teachers)
