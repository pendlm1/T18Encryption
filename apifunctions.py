import requests,json

web = " https://vpic.nhtsa.dot.gov/api"

#Get WMIs for Manufacturer
def getWMIsM(make):
    url = web + "/vehicles/GetWMIsForManufacturer/"+make+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get All Makes
def getAllMakes():
    url = web + "/vehicles/GetAllMakes?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Manufacturer Details
def getMan(make):
    url = web + "/vehicles/GetManufacturerDetails/"+make+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest


#Get Vehicle Variables List
def getVVL():
    url = web + "/vehicles/GetVehicleVariableList?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Makes for Manufacturer by Manufacturer Name and Year
def getMfMbMNaY(make, year):
    url = web + "/vehicles/GetMakesForManufacturerAndYear/"+make+"?year="+year+"&format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Makes for Vehicle Type by Vehicle Type Name
def getMVType(type):
    url = web + "/vehicles/GetMakesForVehicleType/"+type+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

def getAllModels(make):
    url = web + "/vehicles/GetModelsForMake/"+make+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest




def getResults(r,t):
    list = []
    for i in r:
        list.append(i[t])
    return list


#postRequests()
