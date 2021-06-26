from flask import request, Response
from application import app
import dbhelpers
import json
from users import get_users

@app.get("/api/follows")
def api_get_follows():
    try:
        user_id = int(request.args["userId"])
    except KeyError:
        return Response("Please ensure a userId is sent", mimetype="text/plain", status=400)
    except ValueError:
        return Response("userID must be a number", mimetype="text/plain", status=400)
    
    users = get_users("SELECT follow_id, email, username, bio, birthdate, image_url, banner_url FROM user u INNER JOIN follow f ON f.follow_id = u.id WHERE f.user_id=?", [user_id])
    if (len(users) == 0):
        users = get_users("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM user u WHERE u.id=?", [user_id])
        if (len(users) == 0):
            return Response("User not found", mimetype="text/plain", status=404)
        users = []
    
    users_json = json.dumps(users, default=str) 
    return Response(users_json, mimetype="application/json", status=200)

@app.post("/api/follows")
def api_post_follows():
    try: 
        login_token = request.json['loginToken']
        user_id = int(request.json["userId"])
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)
    except ValueError:
        return Response("userId must be a number", mimetype="text/plain", status=400)
    
    follow_user = dbhelpers.run_insert_statement("INSERT into follow(user_id, follow_id) SELECT user_session.user_id, ? FROM user_session WHERE user_session.token=?", [user_id, login_token])

    if (follow_user == None):
        users = get_users("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM user u WHERE u.id=?", [user_id])
        if (len(users) == 0):
            return Response("User not found", mimetype="text/plain", status= 404)
        return Response("User already followed.", mimetype="plain/text", status=500)
    return Response("", mimetype="text/plain", status=204)

@app.delete("/api/follows")
def api_delete_follows():
    try:
        login_token = request.json['loginToken']
        user_id = request.json['followId']
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)
    
    dbhelpers.run_delete_statement(
        "DELETE f from follow f INNER JOIN user_session us ON us.user_id = f.user_id where f.follow_id=? AND us.token=?", [user_id, login_token])
    
    return Response("", mimetype="text/plain", status=204)
