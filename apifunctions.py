import requests,json

web = "https://vpic.nhtsa.dot.gov/api"

#Decode VIN
def decodeVin(vin,year):
    url = web +"/vehicles/DecodeVinExtended/"+vin+"?format=json&modelyear="+year+""
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Decode WMI
def decodeWMI(wmiID):
    url = web + "/vehicles/decodewmi/"+wmiID+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest


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

#Get Makes for Manufacturer by Manufacturer Name and Year (Available if needed)
def getMfMbMNaY(Mft, year):
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

#Get Vehicle Types for Make by Name
def getTypeMake(make):
    url = web + "/vehicles/GetVehicleTypesForMake/"+make+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Vehicle Types for Make by Id
def getTypeMakeID(id):
    url = web + "/vehicles/GetVehicleTypesForMakeId/"+id+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Models for Make
def getAllModels(make):
    url = web + "/vehicles/GetModelsForMake/"+make+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Models for MakeId
def getAllModelsMI(makeID):
    url = web + "/vehicles/GetModelsForMakeId/"+makeID+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Models for Make and a combination of Year and Vehicle Type
def modelsbyMakeYear(make, year):
    url = web + "/vehicles/GetModelsForMakeYear/make/"+make+"/modelyear/"+year+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest
def modelsbyMakeType(make, type):
    url = web + "/vehicles/GetModelsForMakeYear/make/"+make+"/vehicletype/"+type+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest
def modelsbyMakeTypeYear(make,year,type):
    url = web + "/vehicles/GetModelsForMakeYear/make/"+make+"/modelyear/"+year+"/vehicletype/"+type+"?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Vehicle Variables List
def getVVL():
    url = web + "/vehicles/getvehiclevariablelist?format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#Get Equipment Plant Codes (Available if needed year > 2016, typeNum = 1-4, report = [new, updated, closed, all])
def getEquipPlantCodes(year,typeNum,report):
    url = web +"/vehicles/GetEquipmentPlantCodes?year="+year+"&equipmentType="+typeNum+"&reportType="+report+"&format=json"
    r = requests.get(url).text
    dic = json.loads(r)
    myRequest = dic["Results"]
    return myRequest

#API Helper function
def getResults(r,t):
    list = []
    for i in r:
        list.append(i[t])
    return list
