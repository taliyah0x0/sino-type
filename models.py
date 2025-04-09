from app import db 

class Shanghainese(db.Model):
    hanzi = db.Column(db.String(3), primary_key=True)
    roman = db.Column(db.String(10), primary_key=True)

class Korean(db.Model):
    hanzi = db.Column(db.String(3), primary_key=True)
    roman = db.Column(db.String(10), primary_key=True)

class Taiwanese(db.Model):
    hanzi = db.Column(db.String(3), primary_key=True)
    roman = db.Column(db.String(10), primary_key=True)

class Vietnamese(db.Model):
    hanzi = db.Column(db.String(3), primary_key=True)
    roman = db.Column(db.String(10), primary_key=True)