from flask import request, Response
from application import app
from users import get_users
import dbhelpers
import json
import secrets
import hashlib

# Method that logs in a user.
@app.post("/api/login")
def api_post_login():
    try:  
        email = request.json['email']
        password = request.json['password']
    except KeyError:
        return Response("Please enter both email and password", mimetype="plain/text", status=400)
    except:
        return Response("Something went wrong please try again.", mimetype="text/plain", status=500)
    
    salt = get_salt_from_db(email)
    password = salt + password
    password = hashlib.sha512(password.encode()).hexdigest()
    
    if(email == "" or password == ""):
        return Response("Please enter a email or password", mimetype="plain/text", status=400)
   
    user = dbhelpers.run_select_statement("SELECT id FROM `user` WHERE email=? AND password=?", [email, password])
    if (len(user) != 1):
        return Response("Invalid email or password", mimetype="plain/text", status=401)

    token = secrets.token_urlsafe(70)
    user_token = dbhelpers.run_insert_statement("INSERT INTO user_session(token, user_id) VALUES(?,?)", [token, user[0][0]])
    if (user_token == None):
        return Response("Could not create loginToken", mimetype="plain/text", status=500)

    users = get_users("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM `user` WHERE email=? AND password=?", [email, password])

    if (len(users) != 1):
        return Response("Duplicate user found", mimetype="plain/text", status=500)
    users[0]["loginToken"] = token
    login_json = json.dumps(users[0], default=str)
    return Response(login_json, mimetype="application/json", status=201)

# Method that deletes a login (loginToken).
@app.delete("/api/login")
def api_delete_login():
    try:
        login_token = request.json['loginToken']
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)
    except:
        return Response("Something went wrong please try again.", mimetype="text/plain", status=500)
    
    user_rows = dbhelpers.run_delete_statement(
        "DELETE us FROM user_session us WHERE us.token=?", [login_token])
    # Checking to see the number of updated user rows.
    if(user_rows != 1):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    return Response(status=204)

# This function is to return salt based on the users email.
def get_salt_from_db(email):
    user = dbhelpers.run_select_statement("SELECT salt FROM `user` where email=?", [email,])
    if(len(user) == 1 ):
        return user[0][0]
    return ''
