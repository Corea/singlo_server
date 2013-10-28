# -*- coding: utf-8 -*-
from flask import request, render_template
from flask import Blueprint

import api.purchase.queries as queries
import api.auth.queries as auth_queries

mod = Blueprint('purchase', __name__, url_prefix='/purchase')

@mod.route('/shopItem', methods=['GET'])
def shop_item():
	try:
		start_id = int(request.args.get('startid', '0'))
		size = int(request.args.get('size', '10'))

		items = queries.get_items(start_id, size)

		return render_template('shop_item.json', items=items)
	except Exception, e:
		print e
		return render_template('error.json')

@mod.route('/itemPurchase', methods=['GET'])
def purchase_item():
	try:
		user_id = int(request.args.get('userId', '0'))
		item_id = int(request.args.get('itemId', '0'))
		token = request.args.get('receipt', '')
		if token == '':
			raise Exception("No Token")

		item = queries.get_item(item_id)
		user = auth_queries.get_user(user_id)

		if item is None:
			raise Exception("No Item")
		if user is None:
			raise Exception("No User")

		user = queries.add_purchase(user, item, token)
		return render_template('purchase_item.json', user=user)
	except Exception, e:
		print e
		return render_template('error.json')
@mod.route('/purchaseList', methods=['GET'])
def purchase_list():
	try:
		user_id = int(request.args.get('userId', '0'))
		start_id = int(request.args.get('startid', '0'))
		size = int(request.args.get('size', '10'))

		user = auth_queries.get_user(user_id)
		if user is None:
			raise Exception("No User")
		
		purchases = queries.get_purchase_list(user_id, start_id, size)
		
		return render_template('purchase_list.json', purchases=purchases)
	except Exception, e:
		print e
		return render_template('error.json')
