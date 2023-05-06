from datetime import datetime
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_name = db.Column(db.Text(50), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='static/profile_pics/default.jpg')
    decription = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f"Post('{self.author}', '{self.date_posted}')"