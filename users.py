from flask import request, Response
from application import app
import dbhelpers
import json
import traceback
import secrets
import string 
import random
import hashlib

@app.post("/api/users")
def api_create_user():
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        birthdate = request.json['birthdate']
        image_url = request.json.get('imageUrl', None)
        banner_url = request.json.get('bannerUrl', None)
    except:
        return Response("Please ensure all required fields are entered", mimetype="text/plain", status=400)

    salt = create_salt()
    password = salt + password
    password = hashlib.sha512(password.encode()).hexdigest()
    
    if (image_url != None):
        if (banner_url != None):
            new_user_id = dbhelpers.run_insert_statement(f"INSERT INTO user(username, email, password, bio, birthdate, image_url, banner_url, salt) VALUES (?,?,?,?,?,?,?,?)",
                                                [username, email, password, bio, birthdate, image_url, banner_url, salt])
        else:
            new_user_id = dbhelpers.run_insert_statement(f"INSERT INTO user(username, email, password, bio, birthdate, image_url, salt) VALUES (?,?,?,?,?,?,?)",
                                                [username, email, password, bio, birthdate, image_url, salt])
    else:
        if (banner_url != None):
            new_user_id = dbhelpers.run_insert_statement(f"INSERT INTO user(username, email, password, bio, birthdate, banner_url, salt) VALUES (?,?,?,?,?,?,?)",
                                                    [username, email, password, bio, birthdate, banner_url, salt])
        else:    
            new_user_id = dbhelpers.run_insert_statement(f"INSERT INTO user(username, email, password, bio, birthdate, salt) VALUES (?,?,?,?,?,?)",
                                                        [username, email, password, bio, birthdate, salt])
    
    if (new_user_id == None):
        return Response("User already exists", mimetype="text/plain", status=409)

    users = get_users("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM `user` WHERE username=? AND password=?", [username, password])
    
    if(len(users) != 1):
        return Response("Can't fetch created user", mimetype="text/plain", status=500)

    token = secrets.token_urlsafe(70)
    user_token = dbhelpers.run_insert_statement("INSERT INTO user_session(token, user_id) VALUES(?,?)", [token, users[0]["userId"]])

    if(user_token != None):
        users[0]["loginToken"] = token 
        user_json = json.dumps(users[0], default=str)
        return Response(user_json, mimetype="application/json", status=201)
    
    return Response("DB Error, Sorry!", mimetype="text/plain", status=500)

@app.get("/api/users")
def api_get_users():
    try:
        user_id = int(request.args.get("userId", -1))
    except ValueError:
        return Response("userID must be a number.", mimetype="text/plain", status=400)
    
    if (user_id == -1):
        users = get_users("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM user", [])
    else:
        users = get_users("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM user WHERE id=?", [user_id])
    
    if (users == None):
        return Response("Failed to GET users.", mimetype="text/plain", status=500)

    users_json = json.dumps(users, default=str)
    return Response(users_json, mimetype="application/json", status=200)

@app.patch("/api/users")
def api_update_user():
    try:
        login_token = request.json['loginToken']
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)

    users = get_users("SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.image_url, u.banner_url FROM user u inner join user_session us on us.user_id = u.id WHERE us.token = ?", [login_token,])
    if (users == None or len(users) != 1):
        return Response("Could not find user.", mimetype="text/plain", status=404)

    optional_params = {
        "username": request.json.get('username'),
        "email": request.json.get('email'),
        "bio": request.json.get('bio'),
        "birthdate": request.json.get('birthdate'),
        "image_url": request.json.get('imageUrl'),
        "banner_url": request.json.get('bannerUrl'),
    }

    if (optional_params['email'] == "" or optional_params['username'] == ""):
        return Response("Email and username can not be empty", mimetype="text/plain", status=400)

    users[0]['image_url'] = users[0]['imageUrl']
    users[0]['banner_url'] = users[0]['bannerUrl']

    new_optional_params = {}
    for key, value in optional_params.items():
        if (key == 'birthdate'):
            if (users[0][key].isoformat() != optional_params[key]):
                new_optional_params[key] = value
        elif (users[0][key] != optional_params[key]):
            new_optional_params[key] = value

    if (len(new_optional_params.keys()) == 0):
        del users[0]['image_url']
        del users[0]['banner_url']
        users_json = json.dumps(users[0], default=str)
        return Response(users_json, mimetype="application/json", status=200)

    try:
        sql_query_set_list = []
        set_params = []
        for param, value in new_optional_params.items():
            if (value != None):
                sql_query_set_list.append(f"{param}=?")
                set_params.append(value)

        sql_query_set = ', '.join(sql_query_set_list)
        set_params.append(login_token)
        
        number_of_users_updated = dbhelpers.run_update_statement(
            f"UPDATE `user` u INNER JOIN `user_session` us ON us.user_id = u.id SET {sql_query_set} WHERE us.token = ?", set_params)
        if (number_of_users_updated != 1):
            return Response("Unauthorized.", mimetype="text/plain", status=403)
        users = get_users("SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.image_url, u.banner_url FROM user u inner join user_session us on us.user_id = u.id WHERE us.token = ?", [login_token,])

    except:
        return Response("Error in running db query", mimetype="text/plain", status=400)

    if (users == None):
        return Response("Failed to GET user.", mimetype="text/plain", status=500)

    users_json = json.dumps(users[0], default=str)
    return Response(users_json, mimetype="application/json", status=200)

@app.delete("/api/users")
def api_delete_user():
    try:
        password = request.json['password']
        login_token = request.json['loginToken']
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")
        return Response("Data Error", mimetype="text/plain", status=400)
    
    user_rows = dbhelpers.run_delete_statement(
        "DELETE u, us from `user` u INNER JOIN user_session us ON us.user_id = u.id WHERE u.password=? AND us.token=?", [password, login_token])
    if(user_rows < 2):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    return Response("", mimetype="text/plain", status=204)

def get_users(sql_statement, sql_params):
    users_properties = dbhelpers.run_select_statement(sql_statement, sql_params)
    
    if (users_properties == None):
        return None
    users = []
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
        users.append(user)
    return users

def create_salt():
    letters_and_digits = string.ascii_letters + string.digits
    salt = ''.join(random.choice(letters_and_digits) for i in range(10))
    return salt
