from flask_login import UserMixin

class Customer(UserMixin, db.Model):
    """
    Create a table for the users
    """
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

# set up user loaders
@lm.user_loader
def load_customer(id):
    return Customer.query.get(int(id))