from flask import request, Response
from application import app
import json
from users import get_users

# Method that returns followers.
@app.get("/api/followers")
def api_get_followers():
    try:
        user_id = int(request.args["userId"])
    except KeyError:
        return Response("Please ensure a userId is sent", mimetype="text/plain", status=400)
    except ValueError:
        return Response("userID must be a number", mimetype="text/plain", status=400)
    except:
        return Response("Something went wrong please try again.", mimetype="text/plain", status=500)
    # Select statment to get the followers information.
    users = get_users("SELECT f.user_id, email, username, bio, birthdate, image_url, banner_url FROM user u INNER JOIN follow f ON f.user_id = u.id WHERE f.follow_id=?", [user_id])
    # Checks to see if a user exists.
    if (len(users) == 0):
        users = get_users("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM user u WHERE u.id=?", [user_id])
        # If user does not exist an error is returned.
        if (len(users) == 0):
            return Response("User not found", mimetype="text/plain", status=404)
        # Empty list to show that the user has no followers.
        users = []

    users_json = json.dumps(users, default=str) 
    return Response(users_json, mimetype="application/json", status=200)
