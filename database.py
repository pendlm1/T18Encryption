import os, time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField, RadioField, SelectField, FloatField, TextField, TextAreaField, IntegerField,DateTimeField
from wtforms.validators import DataRequired

#basedir is my current director try printing it
basedir = os.path.abspath(os.path.dirname(__file__))

#app prints as <Flask 'main'>
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(basedir,'data.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    phone = db.Column(db.Text)
    email = db.Column(db.Text)
    make = db.Column(db.Text)
    model = db.Column(db.Text)
    year = db.Column(db.Text)
    date = db.Column (db.Text)


    def __init__ (self, firstname, lastname, phone, email,year, make, model,date):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.year = year
        self.make = make
        self.model = model
        self.date = date

    def __repr__(self):
        return f"Appointment: {self.id} First Name:{self.firstname} Last Name:{self.lastname} Phone:{self.phone} Email Adress:{self.email} Year:{self.year} Make:{self.make} Model: {self.model} Service Date:{self.date} "
    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

db.create_all()
