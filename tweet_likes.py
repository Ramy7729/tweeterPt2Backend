from flask import request, Response
from application import app
import dbhelpers
import json

@app.get("/api/tweet-likes")
def api_get_tweet_likes():
    try:
        tweet_id = int(request.args.get("tweetId", -1))
    except ValueError:
        return Response("tweetID must be a number.", mimetype="text/plain", status=400)
    
    if (tweet_id == -1):
        tweets_likes_info = dbhelpers.run_select_statement("SELECT tl.tweet_id, tl.user_id, u.username from tweet_like tl INNER JOIN `user` u on u.id = tl.user_id", [])
    else:
        tweets_likes_info = dbhelpers.run_select_statement("select tl.tweet_id, tl.user_id, u.username from tweet_like tl INNER join `user` u on u.id = tl.user_id where tl.tweet_id = ?", [tweet_id])

    if (tweets_likes_info == None):
        return Response("Failed to GET tweet likes.", mimetype="text/plain", status=500)

    if (len(tweets_likes_info) == 0):
        tweet = dbhelpers.run_select_statement("SELECT id FROM tweet WHERE id=?", [tweet_id])
        if (len(tweet) == 0):
            return Response("Tweet does not exist.", mimetype="text/plain", status=404)

    tweets_likes = []
    for tweet_like_info in tweets_likes_info:
        tweets_likes_dictionary = {
            "tweetId": tweet_like_info[0],
            "userId": tweet_like_info[1],
            "username": tweet_like_info[2]
        }
        tweets_likes.append(tweets_likes_dictionary)
    tweets_likes_json = json.dumps(tweets_likes, default=str)
    return Response(tweets_likes_json, mimetype="application/json", status=200)

@app.post("/api/tweet-likes")
def api_post_tweet_likes():
    try: 
        login_token = request.json['loginToken']
        tweet_id = int(request.json["tweetId"])
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)
    except ValueError:
        return Response("userId must be a number", mimetype="text/plain", status=400)
    
    tweet_like_id = dbhelpers.run_insert_statement("insert into tweet_like(user_id, tweet_id) select user_session.user_id, ? from user_session where user_session.token=?", [tweet_id, login_token])

    if (tweet_like_id == None):
        user_id = dbhelpers.run_select_statement("SELECT user_id FROM user_session us WHERE us.token =?", [login_token])
        if (user_id == None):
            return Response("Invalid loginToken", mimetype="plain/text", status=403)
        tweet_id_info = dbhelpers.run_select_statement("SELECT id FROM tweet t WHERE t.id =?", [tweet_id])
        if (tweet_id_info == None):
            return Response("Tweet does not exist", mimetype="plain/text", status=404)
        tweet_like = dbhelpers.run_select_statement("SELECT tl.id from tweet_like tl INNER JOIN user_session us on us.user_id = tl.user_id WHERE us.token=? and tl.tweet_id=?", [login_token, tweet_id])
        if (len(tweet_like) == 1):
            return Response("Tweet already liked", mimetype="plain/text", status=409)
        return Response("Could not like the tweet.", mimetype="plain/text", status=500)
    return Response("", mimetype="text/plain", status=201)
