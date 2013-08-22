# -*- coding: utf-8 -*-

from god import db

from flask.ext.security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
	db.Column('singlo_admin_id', db.Integer(), db.ForeignKey('singlo_admin.id')),
	db.Column('singlo_admin_role_id', db.Integer(), db.ForeignKey('singlo_admin_role.id')))

class Admin_Role(db.Model, RoleMixin):
	__tablename__ = 'singlo_admin_role'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

	
class Admin(db.Model, UserMixin):
	__tablename__ = 'singlo_admin'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8'}

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	roles = db.relationship('Admin_Role', secondary=roles_users,
		backref=db.backref('users', lazy='dynamic'))

	def __str__(self):
		return '<User id=%s email=%s>' % (self.id, self.email)



