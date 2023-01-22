from db import db

def add(name, address, postnumber, city, latitude, longitude, website):
    try:
        sql = "INSERT INTO restaurants (name, address, postnumber, city, latitude, longitude, website) VALUES (:name, :address, :postnumber, :city, :latitude, :longitude, :website)"
        db.session.execute(sql, {"name":name, "address":address, "postnumber":postnumber, "city":city, "latitude":latitude, "longitude":longitude, "website":website})
        db.session.commit()
    except:
        return False
    return True

def list():
    sql = "SELECT * FROM restaurants ORDER BY name"
    result = db.session.execute(sql)
    return result.fetchall() 