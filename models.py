from app import db

class Shanghainese(db.Model):
    hanzi = db.Column(db.String(3), primary_key=True)
    roman = db.Column(db.String(10), primary_key=True)

    def __init__(self, hanzi, roman):
        self.hanzi = hanzi 
        self.roman = roman

class Korean(db.Model):
    hanzi = db.Column(db.String(3), primary_key=True)
    roman = db.Column(db.String(10), primary_key=True)

    def __init__(self, hanzi, roman):
        self.hanzi = hanzi 
        self.roman = roman

class Taiwanese(db.Model):
    hanzi = db.Column(db.String(3), primary_key=True)
    roman = db.Column(db.String(10), primary_key=True)

    def __init__(self, hanzi, roman):
        self.hanzi = hanzi 
        self.roman = roman

class Vietnamese(db.Model):
    hanzi = db.Column(db.String(3), primary_key=True)
    roman = db.Column(db.String(10), primary_key=True)

    def __init__(self, hanzi, roman):
        self.hanzi = hanzi 
        self.roman = roman