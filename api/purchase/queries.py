# -*- coding: utf-8 -*-

from api import db
from api.models import Item, Purchase

def get_items(start_id, count):
	if start_id == 0: 
		items = Item.query.order_by(Item.id.desc()).limit(count)
	else:
		items = Item.query.filter(Item.id <= start_id).\
			order_by(Item.id.desc()).limit(count)
	
	return items

def get_item(item_id):
	item = Item.query.filter_by(id=item_id).first()

	return item


def add_purchase(user, item, token):
	purchase = Purchase(user.id, item.id, token)
	db.session.add(purchase)
	user.point += item.count
	db.session.commit()

	return user

def get_purchase_list(user_id, start_id, count):
	if start_id == 0: 
		purchases = Purchase.query.order_by(Purchase.id.desc()).limit(count)
	else:
		purchases = Purchase.query.filter(Purchase.id <= start_id).\
			order_by(Purchase.id.desc()).limit(count)

	return purchases

