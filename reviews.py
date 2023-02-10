from db import db
import users

def getreview(id):
    sql = "SELECT R.id, R.review, U.username, R.rating, R.created_at FROM reviews R, users U WHERE restaurant_id=:id AND R.user_id=U.id ORDER BY R.created_at DESC"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def addreview(restaurant_id, review, rating):
    try:
        user_id = users.user_id()
        if user_id == 0:
            return False
        sql = "INSERT INTO reviews (restaurant_id, user_id, review, rating, created_at) VALUES (:restaurant_id, :user_id, :review, :rating, NOW())"
        db.session.execute(sql, {"restaurant_id":restaurant_id,"user_id":user_id, "review":review, "rating":rating})
        db.session.commit()
    except:
        return False
    return True

def deletereview(id):
    try:
        user_role = users.user_role()
        if user_role == 0:
            return False
        sql = "DELETE FROM reviews WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True