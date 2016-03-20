from example.models import db

class Cat(db.Model):
    __tablename__ = 'cat'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('owner.id'))

