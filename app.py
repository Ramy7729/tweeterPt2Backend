from flask import Flask, request, Response
import dbhelpers
import json
import traceback
import sys
import secrets
import dbconnect

app = Flask(__name__)

@app.get("/api/users")
def get_users():
    try:
        user_id = int(request.args.get("userId", -1))
    except ValueError:
        return Response("userID must be a number.", mimetype="text/plain", status=400)
    
    if (user_id == -1):
        users_properties = dbhelpers.run_select_statement("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM user", [])
    else:
        users_properties = dbhelpers.run_select_statement("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM user WHERE id=?", [user_id])
    
    if (users_properties == None):
        return Response("Failed to GET users.", mimetype="text/plain", status=500)
    results = []
    for user_properties in users_properties:
        user = {
            "userId": user_properties[0],
            "email": user_properties[1],
            "username": user_properties[2],
            "bio": user_properties[3],
            "birthdate": user_properties[4],
            "imageUrl": user_properties[5],
            "bannerUrl":user_properties[6],
        }
        results.append(user)

    users_json = json.dumps(results, default=str)
    return Response(users_json, mimetype="application/json", status=200)

@app.post("/api/login")
def post_login():
    try:  
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        return Response("Please enter both username and password", mimetype="plain/text", status=400)
    
    if(username == "" or password == ""):
        return Response("Please enter a username or password", mimetype="plain/text", status=400)
   
    user = dbhelpers.run_select_statement("SELECT id FROM `user` WHERE username=? AND password=?", [username, password])
    if (len(user) != 1):
        return Response("Invalid username or password", mimetype="plain/text", status=401)

    token = secrets.token_urlsafe(70)
    user_token = dbhelpers.run_insert_statement("INSERT INTO user_session(token, user_id) VALUES(?,?)", [token, user[0][0]])
    if (user_token == None):
        return Response("Could not create loginToken", mimetype="plain/text", status=500)
    users_properties = dbhelpers.run_select_statement("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM `user` WHERE username=? AND password=?", 
                                                        [username, password])
    if (len(users_properties) != 1):
        return Response("Duplicate user found", mimetype="plain/text", status=500)
    logged_in_user = {
        "userId": users_properties[0][0],
        "email": users_properties[0][1],
        "username": users_properties[0][2],
        "bio": users_properties[0][3],
        "birthdate": users_properties[0][4],
        "imageUrl": users_properties[0][5],
        "bannerUrl": users_properties[0][6],
        "loginToken": token,
    }
    login_json = json.dumps(logged_in_user, default=str)
    return Response(login_json, mimetype="application/json", status=201)

app.run(debug=True)
