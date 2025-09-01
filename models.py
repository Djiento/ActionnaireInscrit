from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    whatsapp_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    city_country = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    investment_amount = db.Column(db.String(50), nullable=False)
    experience_level = db.Column(db.String(20), nullable=False)
    identity_document = db.Column(db.String(255))  # File path
    payment_method = db.Column(db.String(50), nullable=False)
    additional_remarks = db.Column(db.Text)
    terms_accepted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    whatsapp_invited = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Investor {self.full_name}>'

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    whatsapp_group_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
