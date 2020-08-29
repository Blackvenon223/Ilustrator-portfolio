from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

class Artist(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = "Маргарита"
	phone_number = "+79293651902"
	email = "6061132@gmail.com"
	description = "Описание"
	password_hash = db.Column(db.String(128))
	username = "Illustrita"
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
		

		
	def __repr__(self):
		return '<Artist {}>'.format(self.username)
		
class Work(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64),index=True, unique=True)
	category = db.Column(db.String(64), index=True, unique=True)
	source =  db.Column(db.String(64), index=True, unique=True)
	
	def __repr__(self):
		return '<Work {}>'.format(self.name) 

@login.user_loader
def load_artist(id):
    return Artist.query.get(int(id))
