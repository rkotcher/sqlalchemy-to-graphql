from server.models import db

class Cat(db.Model):
    __tablename__ = 'test_cat'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('test_owner.id'))

    #parent_id = db.Column(db.Integer, db.ForeignKey('test_cat.id'))
    #children = db.relationship('Cat', cascade='all, delete-orphan', backref=db.backref('parent', remote_side=id))

