import flask_sqlalchemy
import datetime

db = flask_sqlalchemy.SQLAlchemy()

##### The Tables for the Database ######

# Exchange Table
class Exchange(db.Model):
    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String, primary_key=True)
    code = db.Column(db.String)
    tax = db.Column(db.Float)
    tip = db.Column(db.Float)
    terminated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.name

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


# Items Table
class Items(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    split = db.Column(db.Integer)
    exchange_id = db.Column(db.Integer)


