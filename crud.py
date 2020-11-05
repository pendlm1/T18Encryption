from database import db, Appointment

def getId(i):
    i = Appointment.query.get(i)
    print (i)
    return i

def dbDeleteID(id):
    db.session.delete(id)
    db.session.commit()
    print ("Deleted: ",id)
    return

def countItems():
    count = len(Appointment.query.all())
    print ("There are ",count," items in the database")
    return count

def get_db():
    all_Appointments =  Appointment.query.all()
    print (all_Appointments)
    return all_Appointments

def removeItems():
    print ("WARNING: You are permanently removing ALL items from the database ")
    ans = input("Continue Yes/No: ")
    if ans == "Yes" or ans == "yes" or ans == "YES":
        Appointment.query.delete()
        db.session.commit()
        all_Appointments =  Appointment.query.all()
        print("*************************************************")
        print("All items have been deleted from the database")
        print (all_Appointments)
    elif ans == "No" or ans == "no" or ans == "NO":
        return
    else:
        return removeItems()
