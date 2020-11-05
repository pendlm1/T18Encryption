import requests, json, re, os, time, apifunctions
from flask import Flask, render_template, url_for, session, redirect, request
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, RadioField,
SelectField, FloatField, TextField, TextAreaField, IntegerField)
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from apifunctions import*

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

if __name__ == '__main__':
    app.run(debug=True)

