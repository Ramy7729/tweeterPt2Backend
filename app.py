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

app.run(debug=True)
