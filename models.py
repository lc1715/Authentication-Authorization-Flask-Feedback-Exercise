from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedbacks = db.relationship('Feedback', backref='user', cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password):
        """To register a user and make a hashed password and return the user object.
        We get the users's username and password from the register form. """
        
        hashed_password = bcrypt.generate_password_hash(password)

        hashed_utf8_pwd_string = hashed_password.decode('utf8')
        
        return {username:username, password:hashed_utf8_pwd_string}
    
    @classmethod
    def authenticate(cls, username, password):
       """Validates that user exists and password is correct.
        Return user if valid, else return false. """

       user = User.query.filter_by(username=username).first()

       if user and bcrypt.check_password_hash(user.password, password):
           return user
       else:
           return False
       
class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))
    # user = db.relationship('User', backref='feedbacks')
    
