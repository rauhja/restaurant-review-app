from db import db

def gettags():
    sql = "SELECT id, name FROM tags"
    result = db.session.execute(sql)
    return result.fetchall()

def getrestauranttag(id):
    sql = "SELECT R.id, R.name, T.name FROM restaurants R, tags T, restaurant_tags RT WHERE R.id=RT.restaurant_id AND T.id=RT.tag_id AND R.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def addtag(id, tag):
    try:
        print("id: " + str(id))
        sql = "INSERT INTO restaurant_tags (restaurant_id, tag_id) VALUES (:restaurant_id, :tag_id)"
        db.session.execute(sql, {"restaurant_id":id, "tag_id":tag})
        db.session.commit()
    except:
        return False
    return True