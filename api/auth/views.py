# -*- coding: utf-8 -*-
from flask import request, render_template, send_from_directory
from flask import Blueprint, current_app

import api.auth.queries as queries

import os


mod = Blueprint('auth', __name__, url_prefix='/auth')

@mod.route('/register', methods=['POST'])
def register():
        try:
                name = request.form['name']
                birthday = request.form['birthday']
                phone = request.form['phone']
                if 'pushtoken' in request.form:
                        pushtoken = request.form['pushtoken']
                else:
                        pushtoken = None
                        
                if 'profile' in request.files:
                        profile = request.files['profile']
                else:
                        profile = None
                
                user = queries.get_valid_user(name, birthday, phone)
                teacher = queries.get_valid_teacher(name, birthday, phone)
                if user is None and teacher is None:
                        queries.add_user(name, birthday, phone, pushtoken, profile)
                        user = queries.get_valid_user(name, birthday, phone)
                        if profile is not None:
                                profile_path = os.path.join(current_app.config['PROFILE_FOLDER'], user.photo)
                                profile.save(profile_path)
                        return render_template('register.json', user=user)
                else:
                        raise
        except Exception as e:
                print e
                return render_template('error.json')


@mod.route('/login', methods=['POST'])
def login():
        try:
                name = request.form['name']
                birthday = request.form['birthday']
                phone = request.form['phone']
                                                    

                user = queries.get_valid_user(name, birthday, phone)
                if 'pushtoken' in request.form:
                        queries.update_pushtoken(user.id,request.form['pushtoken'])
                                               
                
                if user is None:
                        teacher = queries.get_valid_teacher(name, birthday, phone)
                        if teacher is None:
                                raise
                        else:
                                count = queries.count_unanswer_question(teacher.id)
                                evaluation = queries.get_score_evaluation(teacher.id)
                                return render_template('login_teacher.json', 
                                        teacher=teacher, count=count, evaluation=evaluation)
                else:
                        count = queries.count_unconfirm_question(user.id)
                        return render_template('login.json', user=user, count=count)
        except Exception, e:
                print e
                return render_template('error.json')


