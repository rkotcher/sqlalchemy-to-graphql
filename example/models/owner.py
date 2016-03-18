class Owner(db.Model):
    __tablename__ = 'owner'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    cat = db.Column(db.Integer, db.ForeignKey('cat.id'))

