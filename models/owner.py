from server.models import db

class Owner(db.Model):
    __tablename__ = 'test_owner'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    cat = db.Column(db.Integer, db.ForeignKey('test_cat.id'))

