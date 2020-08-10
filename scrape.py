import requests, json, re, os, time, apifunctions
from flask import Flask, render_template, url_for, session, redirect, request
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, RadioField,
SelectField, FloatField, TextField, TextAreaField, IntegerField)
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apifunctions import*

myData = ""
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
    "Get Makes for Vehicle Type by Vehicle Type Name","Get Vehicle Types for Make by Name",
    "Get Vehicle Types for Make by Id","Get Models for Make","Get Models for MakeId",
    "Get Models for Make and a combination of Year and Vehicle Type","Get Vehicle Variables List",
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
    wmiID = StringField("WMI ID: ")
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
    form = makeform()
    info = ""
    make = request.values.get("make")
    model = request.values.get("model")
    year = request.values.get("year")
    modelID = request.values.get("modelID")
    makeID = request.values.get("makeID")
    vin = request.values.get("vin")
    type = request.values.get("type")
    wmiID = request.values.get("wmiID")
    getRequest = request.values.get("getRequest")

    if myData == "Get All Makes":
        info = getAllMakes()
        return render_template("results8.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get WMIs for Manufacturer":
        info = getWMIsM(make)
        return render_template("results1.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Manufacturer Details":
        info = getMan(make)
        return render_template("results2.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    #coded but not included. I chose to make this one optional.
    elif myData == "Get Makes for Manufacturer by Manufacturer Name and Year":
        info = getMfMbMNaY(make, year)
        return render_template("results3.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Makes for Vehicle Type by Vehicle Type Name":
        info = getMVType(type)
        return render_template("results10.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Vehicle Types for Make by Name":
        info = getTypeMake(make)
        return render_template("results0.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Vehicle Types for Make by Id":
        info = getTypeMakeID(makeID)
        return render_template("results5.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Equipment Plant Codes":
        info = getEquipPlantCodes(year,typeNum,report)
        return render_template("results5.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Models for Make":
        info = getAllModels(make)
        return render_template("results4.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Models for MakeId":
        info = getAllModelsMI(makeID)
        return render_template("results6.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Models for Make and a combination of Year and Vehicle Type":
        if type == "" and year == "":
            info = getAllModels(make)
            return render_template("results4.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
        elif type == "":
            info = modelsbyMakeYear(make, year)
        elif year == "":
            info = modelsbyMakeType(make, type)
        else:
            info = modelsbyMakeTypeYear(make,year,type)
        return render_template("results4.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Get Vehicle Variables List":
         info = getVVL()
         return render_template("results7.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Decode VIN":
         info = decodeVin(vin,year)
         return render_template("results9.html",wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)
    elif myData == "Decode WMI":
        info = decodeWMI(wmiID)
    return render_template("results.html",form=form,wmiID=wmiID,type=type,make=make,model=model,year=year,makeID=makeID,modelID=modelID,vin=vin,getRequest=getRequest,info=info)

@app.route("/research0")
def research0():
    form = makeform()
    getRequest = request.values.get("getRequest")
    global myData
    myData = getRequest
    return render_template("research0.html",form = form,getRequest=getRequest)

@app.route("/research")
def research():
    form = makeform()
    return render_template("research.html", form = form)

if __name__ == '__main__':
    app.run(debug=True)
