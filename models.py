from app import db 

class City:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    countrycode = db.Column(db.String(3), nullable=False)
    district = db.Column(db.String(20))
    population = db.Column(db.Integer)