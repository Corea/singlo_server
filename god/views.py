# -*- coding: utf-8 -*-
from flask import Blueprint

mod = Blueprint('god', __name__, url_prefix='/god')


@mod.route("/user")
@login_required
def god_user():
	return render_template('god/user.html')


