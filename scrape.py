import requests, json, re, os, time, apifunctions
from flask import Flask, render_template, url_for, session, redirect, request
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, RadioField,
SelectField, FloatField, TextField, TextAreaField, IntegerField)
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apifunctions import*
from crud import*

myData = ""
myQuery = ""
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.urandom(24)

#############################   Database   #########################################
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
################################  Forms   ##########################################
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

class appointmentForm(FlaskForm):
    years = []
    year = int(time.strftime("%Y"))
    for y in range (year +2,year -50,-1):
        years.append((y,y))
    years[0]=(("",""))
    firstname = StringField("First Name: ", validators=[DataRequired()])
    lastname = StringField("Last Name: ", validators=[DataRequired()])
    email = StringField("Email Address: ")
    phone = StringField("Phone Number: ")
    year = IntegerField("Vehicle Year: ")
    make = StringField("Vehicle Make: ")
    model = StringField("Vehicle Model: ")
    date = DateField("Appointment Date (yyyy-mm-dd): ",format= '%Y-%m-%d')
    submit = SubmitField("Submit")


################################## URLs  ###########################################

class cancelAppointment(FlaskForm):
    id = IntegerField("ID: ", validators=[DataRequired()])
    delete = SubmitField("Delete")

class searchDate(FlaskForm):
    firstname = StringField("First Name: ")
    lastname = StringField("Last Name: ")
    date = DateField("Appointment Date (yyyy-mm-dd): ",format= '%Y-%m-%d')
    search = SubmitField("Search")

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

#Get Data from the form using session
@app.route("/form", methods= ['GET','POST'])
def appointment():
    form = appointmentForm()
    if form.validate_on_submit():
        a = session["firstname"] = form.firstname.data
        b = session["lastname"] = form.lastname.data
        c = session["phone"] = form.phone.data
        d = session["email"] = form.email.data
        e = session["year"] = form.year.data
        f = session["make"] = form.make.data
        g = session["model"] = form.model.data
        h = session["date"] = form.date.data
        entry = Appointment(a,b,c,d,e,f,g,h)
        entry.add()
        return redirect(url_for("thankyou"))
    return render_template("appointment.html",form=form)

@app.route("/research")
def research():
    form = makeform()
    return render_template("research.html", form = form)

@app.route("/appointments")
def appointments():
    form = appointmentForm()
    items = Appointment.query.filter(Appointment.date)
    return render_template("customer.html",items = items, form=form)

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/customer")
def customer():
    items = get_db()
    return render_template("customer.html",items = items)

@app.route("/searchresults",methods= ['GET','POST'])
def searchresults():
    items = myQuery
    return render_template("searchresults.html",items=items)

@app.route("/cancelappointment", methods= ['GET','POST'])
def cancelappointment():
    form = cancelAppointment()
    if form.validate_on_submit()==True:
        a = form.id.data
        id = getId(a)
        dbDeleteID(id)
        return redirect(url_for("thankyou"))
    return render_template("cancelappointment.html", form = form)

@app.route("/search",methods= ['GET','POST'])
def search():
    form = searchDate()
    if form.validate_on_submit()==True:
        a = session["firstname"] = form.firstname.data
        b = session["lastname"] = form.lastname.data
        global myQuery
        if a and b:
            myQuery= Appointment.query.filter(Appointment.firstname == a, Appointment.lastname ==b)
        elif a:
            myQuery= Appointment.query.filter(Appointment.firstname == a)
        elif b:
            myQuery= Appointment.query.filter(Appointment.lastname ==b)
        return redirect(url_for("searchresults",form=form))
    return render_template("search.html",form=form)

@app.route('/location')
def location():
    mapbox_access_token = 'pk.eyJ1IjoibmF0aGFubGVkYmV0dGVyIiwiYSI6ImNrZGYyYjlkZzFuZXcyeGpxZWFkcWNrbWEifQ.2m7aP5cNYshVCAS_581d3g'
    return render_template("location.html", mapbox_access_token=mapbox_access_token)



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

if __name__ == '__main__':
    app.run(debug=True)
