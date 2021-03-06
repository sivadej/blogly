from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# Models/schema
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    img_url = db.Column(db.String(50), nullable=True)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def get_full_name(self):
        return(f'{self.first_name} {self.last_name}')
    
#    @classmethod
#    def get_users_by_last_name(cls):
#        return cls.query.order_by('last_name').all()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)