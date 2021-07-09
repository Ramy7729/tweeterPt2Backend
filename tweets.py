from flask import request, Response
from application import app
import dbhelpers
import json

# Method that returns tweets.
@app.get("/api/tweets")
def api_get_tweets():
    try:
        user_id = int(request.args.get("userId", -1))
    except ValueError:
        return Response("userID must be a number.", mimetype="text/plain", status=400)
    except:
        return Response("Something went wrong please try again.", mimetype="text/plain", status=500)
    
    if (user_id == -1):
        tweets = get_tweets("SELECT t.id, t.user_id, u.username, t.content, t.created_at, u.image_url, t.image_url FROM user u INNER JOIN tweet t ON t.user_id = u.id", [])
    else:
        tweets = get_tweets("SELECT t.id, t.user_id, u.username, t.content, t.created_at, u.image_url, t.image_url FROM user u INNER JOIN tweet t ON t.user_id = u.id WHERE t.user_id=?", [user_id])
    
    if (tweets == None):
        return Response("Failed to GET tweets.", mimetype="text/plain", status=500)

    tweets_json = json.dumps(tweets, default=str)
    return Response(tweets_json, mimetype="application/json", status=200)

# Method that lets a user post a tweet.
@app.post("/api/tweets")
def api_post_tweets():
    try: 
        login_token = request.json['loginToken']
        content = request.json['content']
        image_url = request.json.get('imageUrl')
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)
    except:
        return Response("Something went wrong please try again.", mimetype="text/plain", status=500)
    # Conditional to check if the post is too long.
    if (len(content) > 377):
        return Response("Content too long", mimetype="text/plain", status=400)
    # Conditional that runs the insert statement if the user added an image url or not.
    if (image_url == None):
        user_tweet_id = dbhelpers.run_insert_statement("INSERT INTO tweet(content, user_id) SELECT ?, user_id FROM user_session us WHERE us.token =?", [content, login_token])
    else:
        user_tweet_id = dbhelpers.run_insert_statement("INSERT INTO tweet(content, image_url, user_id) SELECT ?, ?, user_id FROM user_session us WHERE us.token =?", [content, image_url, login_token])
    if (user_tweet_id == None):
        return Response("Invalid login token", mimetype="text/plain", status=400)
    # Sql statement to return specified data.   
    tweets = get_tweets("SELECT t.id, t.user_id, u.username, t.content, t.created_at, u.image_url user_image_url, t.image_url FROM tweet t INNER JOIN user_session us on us.user_id = t.user_id INNER JOIN `user` u on u.id = t.user_id where us.token =? AND t.id =?", [login_token, user_tweet_id])
    # Checks to see if we can get the tweet.
    if (tweets == None or len(tweets) != 1):
        return Response("Error fetching tweet", mimetype="text/plain", status=500)

    tweets_json = json.dumps(tweets[0], default=str) 
    return Response(tweets_json, mimetype="application/json", status=201)

# Method that allows the user to edit their tweet.
@app.patch("/api/tweets")
def api_patch_tweet():
    try:
        login_token = request.json['loginToken']
        tweet_id = int(request.json['tweetId'])
        content = request.json['content']
    except ValueError:
        return Response("tweetId must be a number", mimetype="text/plain", status=400)
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)
    except:
        return Response("Something went wrong please try again.", mimetype="text/plain", status=500)
    
    if (len(content) > 377):
        return Response("Content too long", mimetype="text/plain", status=400)
    
    number_of_tweets_updated = dbhelpers.run_update_statement("UPDATE tweet t INNER JOIN `user_session` us ON us.user_id = t.user_id SET content =? WHERE us.token = ? and t.id = ?", 
                                                    [content, login_token, tweet_id])
    if (number_of_tweets_updated != 1):
        return Response("Unable to update tweet.", mimetype="text/plain", status=403)
    tweet = {
        "tweetId": tweet_id,
        "content": content
    }
    tweet_json = json.dumps(tweet, default=str)
    return Response(tweet_json, mimetype="application/json", status=200)

# Method that lets a user delete their tweet.
@app.delete("/api/tweets")
def api_delete_tweets():
    try:
        login_token = request.json['loginToken']
        tweet_id = int(request.json['tweetId'])
    except ValueError:
        return Response("tweetId must be a number", mimetype="text/plain", status=400)
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)
    except:
        return Response("Something went wrong please try again.", mimetype="text/plain", status=500)
    number_of_tweets_deleted = dbhelpers.run_delete_statement(
        "DELETE t from tweet t INNER JOIN user_session us ON us.user_id = t.user_id where t.id=? AND us.token=?", [tweet_id, login_token])
    if (number_of_tweets_deleted != 1):
        return Response("Could not delete tweet", mimetype="text/plain", status=400)
    return Response("", mimetype="text/plain", status=204)

# This function returns tweets.
# Using a dictionary to get proper key values.
def get_tweets(sql_statement, sql_params):
    users_properties = dbhelpers.run_select_statement(sql_statement, sql_params)
    
    if (users_properties == None):
        return None
    users = []
    for user_properties in users_properties:
        user = {
            "tweetId": user_properties[0],
            "userId": user_properties[1],
            "username": user_properties[2],
            "content": user_properties[3],
            "createdAt": user_properties[4],
            "userImageUrl": user_properties[5],
            "tweetImageUrl":user_properties[6],
        }
        users.append(user)
    return users
