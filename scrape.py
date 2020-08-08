import requests, json, re, os, time, apifunctions
from flask import Flask, render_template, url_for, session, redirect, request
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, RadioField,
SelectField, FloatField, TextField, TextAreaField, IntegerField)
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apifunctions import*


app = Flask(__name__)
app.secret_key = os.urandom(24)

#Create the form visual with a class
class makeform(FlaskForm):
    list = []
    makes = getAllMakes()
    years = []
    gets = []
    getAPI = [
    "Decode VIN","Decode WMI","Get WMIs for Manufacturer","Get All Makes","Get Manufacturer Details",
    "Get Makes for Manufacturer by Manufacturer Name and Year","Get Makes for Vehicle Type by Vehicle Type Name",
    "Get Vehicle Types for Make by Name","Get Vehicle Types for Make by Id","Get Models for Make","Get Models for MakeId",
    "Get Models for Make and a combination of Year and Vehicle Type","Get Vehicle Variables List",
    "Get Vehicle Variable Values List","Get Canadian vehicle specifications"
    ]
    year = int(time.strftime("%Y"))
    for y in range (year +2,year -100,-1):
        years.append((y,y))
    years[0]=(("",""))
    for m in makes:
        list.append((m["Make_Name"],m["Make_Name"]))
    list = sorted (list,key=lambda l: l[1])
    for r in getAPI:
        gets.append((r,r))
    gets.sort()
    make = SelectField("Make: ", choices = list,validators=[DataRequired()])
    model = StringField("Model: ")
    year = SelectField("Year: ", choices = years)
    makeID = IntegerField("MakeID: ")
    modelID = IntegerField("ModelID: ")
    vin = TextField("Vin: ")
    getRequest = SelectField("Request: ", choices = gets)
    type = IntegerField("Type: ")
    submit = SubmitField("Submit")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/coupons')
def coupons():
    items = os.listdir('static/coupons/')
    return render_template("coupons.html",items = items)

@app.route('/repairs')
def repairs():
    return render_template("repairs.html")


@app.route('/reviews')
def reviews():
    return render_template("reviews.html")

@app.route("/tires")
def tires():
    return render_template("tires.html")

@app.route("/wheels")
def wheels():
    return render_template("wheels.html")

@app.route("/results", methods = ["GET","POST"])
def models():
    info = ""
    make = request.values.get("make")
    model = request.values.get("model")
    year = request.values.get("year")
    modelID = request.values.get("modelID")
    makeID = request.values.get("makeID")
    vin = request.values.get("vin")
    type = request.values.get("type")
    getRequest = request.values.get("getRequest")

    if getRequest == "Get All Makes":
        r = getAllMakes()
        t = "Make_Name"
        info = getResults(r,t)
    elif getRequest == "Get WMIs for Manufacturer":
        r = getWMIsM(make)
        t = "Name"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Manufacturer Details":
        r = getMan(make)
        t = "Mfr_Name"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Makes for Manufacturer by Manufacturer Name and Year":
        r = getMfMbMNaY(make, year)
        t = "MfrName"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Makes for Vehicle Type by Vehicle Type Name":
        r = getMVType(type)
        t = "MakeName"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Vehicle Types for Make by Name":
        r = getTypeMake(make)
        t = "VehicleTypeName"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Vehicle Types for Make by Id":
        r = getTypeMakeID(makeID)
        t = "VehicleTypeName"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Equipment Plant Codes":
        r = getEquipPlantCodes(year)
        t = "DOTCode"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Vehicle Types for Make by Id":
        r = getAllModels(makeID)
        t = "Model_Name"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Models for Make":
        r = getAllModels(make)
        t = "Model_Name"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Models for MakeId":
        r = getAllModelsMI(makeID)
        t = "Model_Name"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Models for Make and a combination of Year and Vehicle Type":
        if type == "" and year == "":
            r = getAllModels(make)
        elif type == "":
            r = modelsbyMakeYear(make, year)
        elif year == "":
            r = modelsbyMakeType(make, type)
        else:
            r = modelsbyMakeTypeYear(make,year,type)
        t = "Model_Name"
        info = getResults(r,t)
        info.sort()
    elif getRequest == "Get Vehicle Variables List":
         r = getVVL()
         t = "Name"
         info = getResults(r,t)
         info.sort()
    elif getRequest == "Decode VIN":
         r = decodeVin(vin,year)
         t = "Variable"
         info = getResults(r,t)
         info.sort()
    elif getRequest == "Decode WMI":
        r = decodeWMI(vin)
        t = "CommonName"
        info = getResults(r,t)
        info.sort()
    return render_template("results.html",type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)

@app.route("/shop")
def shop():
    form = makeform()
    if form.validate_on_submit():
        make = session["make"] = form.make.data
        model = session["model"] = form.model.data
        year = form.year.data
        return redirect(url_for("models",make=make,model=model,year=year))
    return render_template("shop.html", form = form)

if __name__ == '__main__':
    app.run(debug=True)
