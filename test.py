# -*- coding: utf-8 -*-

from models import * 
from server import * 
import urllib


user1 = User(urllib.quote("고준희"), "9", "9")
user2 = User(urllib.quote("강동원"), "8", "8")
user3 = User(urllib.quote("정우성"), "7", "7")

teacher1 = Teacher()
teacher1.name = urllib.quote("이미림")
teacher1.birthday = "0"
teacher1.phone = "0"
teacher1.photo = None
teacher1.company = urllib.quote("가리지스토리")
teacher1.certification = urllib.quote("Class A / LPGA")
teacher1.lessons = urllib.quote("롱게임")
teacher1.video_available = True
teacher1.price = 7800
teacher1.profile = ""
teacher1.url = ""

teacher2 = Teacher()
teacher2.name = urllib.quote("한효주")
teacher2.birthday = "1"
teacher2.phone = "1"
teacher2.photo = None
teacher2.company = urllib.quote("가리지스토리")
teacher2.certification = urllib.quote("Class A / LPGA")
teacher2.lessons = urllib.quote("숏게임")
teacher2.video_available = True
teacher2.price = 9800
teacher2.profile = ""
teacher2.url = ""

teacher3 = Teacher()
teacher3.name = urllib.quote("이나영")
teacher3.birthday = "2"
teacher3.phone = "2"
teacher3.photo = None
teacher3.company = urllib.quote("가리지스토리")
teacher3.certification = urllib.quote("Class A / LPGA")
teacher3.lessons = urllib.quote("숏게임")
teacher3.video_available = True
teacher3.price = 13800
teacher3.profile = ""
teacher3.url = ""


with app.app_context():
	db.session.add(user1)
	db.session.add(user2)
	db.session.add(user3)
	db.session.add(teacher1)
	db.session.add(teacher2)
	db.session.add(teacher3)
	db.session.commit()


