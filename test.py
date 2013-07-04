# -*- coding: utf-8 -*-

from models import * 
from server import * 


user1 = User("고준희", "01098765432", "user1", "s")
user2 = User("강동원", "01098765432", "user2", "s")
user3 = User("정우성", "01098765432", "user3", "s")

teacher1 = Teacher()
teacher1.name = "이미림"
teacher1.phone = "01012345678"
teacher1.email = "teacher1"
teacher1.password = "s"
teacher1.photo = None
teacher1.company = "가리지스토리"
teacher1.certification = "Class A / LPGA"
teacher1.lessons = "롱게임"
teacher1.video_available = True
teacher1.price = 7800
teacher1.profile = ""
teacher1.url = ""

teacher2 = Teacher()
teacher2.name = "한효주"
teacher2.phone = "01012345678"
teacher2.email = "teacher2"
teacher2.password = "s"
teacher2.photo = None
teacher2.company = "가리지스토리"
teacher2.certification = "Class A / LPGA"
teacher2.lessons = "숏게임"
teacher2.video_available = True
teacher2.price = 9800
teacher2.profile = ""
teacher2.url = ""

teacher3 = Teacher()
teacher3.name = "이나영"
teacher3.phone = "01012345678"
teacher3.email = "teacher3"
teacher3.password = "s"
teacher3.photo = None
teacher3.company = "가리지스토리"
teacher3.certification = "Class A / LPGA"
teacher3.lessons = "숏게임"
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


