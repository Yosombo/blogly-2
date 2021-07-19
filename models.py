from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(
        db.String,
        nullable=False,
        default=
        'data:image/png;base64,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'
    )

    posts = db.relationship('Post',
                            backref=backref("user"),
                            cascade='all, delete, delete-orphan',
                            passive_deletes=True)

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='cascade'),
                        nullable=False)

    def __repr__(self):
        return f"<Post {self.id} {self.title}>"

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")