from db import db
import users

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

def get(id):
    sql = "SELECT * FROM restaurants WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def delete(id):
    try:
        user_role = users.user_role()
        if user_role == 0:
            return False
        sql = "DELETE FROM restaurants WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True

def search(query):
    sql = "SELECT r.id, r.name, r.city, r.website, AVG(rv.rating)::numeric(10,2) AS avg_rating FROM restaurants r LEFT JOIN reviews rv ON rv.restaurant_id = r.id WHERE r.name LIKE :query GROUP BY r.id, r.name ORDER BY avg_rating DESC NULLS LAST"
    result = db.session.execute(sql, {"query":"%" + query + "%"})
    return result.fetchall()

def listall():
    sql = "SELECT r.id, r.name, r.city, r.website, AVG(rv.rating)::numeric(10,2) AS avg_rating FROM restaurants r LEFT JOIN reviews rv ON rv.restaurant_id = r.id GROUP BY r.id, r.name ORDER BY avg_rating DESC NULLS LAST"
    result = db.session.execute(sql)
    return result.fetchall()
