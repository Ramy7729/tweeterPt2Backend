from flask import request, Response
from application import app
import dbhelpers
import json

@app.get("/api/comment-likes")
def api_get_comment_likes():
    try:
        comment_id = int(request.args.get("commentId", -1))
    except ValueError:
        return Response("commentID must be a number.", mimetype="text/plain", status=400)
    
    if (comment_id == -1):
        comments_likes_info = dbhelpers.run_select_statement("SELECT cl.comment_id, cl.user_id, u.username FROM comment_like cl INNER JOIN `user` u on u.id = cl.user_id", [])
    else:
        comments_likes_info = dbhelpers.run_select_statement("SELECT cl.comment_id, cl.user_id, u.username FROM comment_like cl INNER JOIN `user` u on u.id = cl.user_id where cl.comment_id =?", [comment_id])

    if (comments_likes_info == None):
        return Response("Failed to GET tweet likes.", mimetype="text/plain", status=500)

    if (len(comments_likes_info) == 0):
        tweet = dbhelpers.run_select_statement("SELECT id FROM comment WHERE id=?", [comment_id])
        if (len(tweet) == 0):
            return Response("Tweet does not exist.", mimetype="text/plain", status=404)

    comments_likes = []
    for comment_like_info in comments_likes_info:
        comments_likes_dictionary = {
            "commentId": comment_like_info[0],
            "userId": comment_like_info[1],
            "username": comment_like_info[2]
        }
        comments_likes.append(comments_likes_dictionary)
    comments_likes_json = json.dumps(comments_likes, default=str)
    return Response(comments_likes_json, mimetype="application/json", status=200)

@app.post("/api/comment-likes")
def api_post_comment_likes():
    try: 
        login_token = request.json['loginToken']
        comment_id = int(request.json["commentId"])
    except KeyError:
        return Response("Please ensure all required fields are sent", mimetype="text/plain", status=400)
    except ValueError:
        return Response("userId must be a number", mimetype="text/plain", status=400)
    
    comment_like_id = dbhelpers.run_insert_statement("INSERT INTO comment_like(user_id, comment_id) SELECT user_session.user_id, ? FROM user_session WHERE user_session.token =?", [comment_id, login_token])

    if (comment_like_id == None):
        user_id = dbhelpers.run_select_statement("SELECT user_id FROM user_session us WHERE us.token =?", [login_token])
        if (user_id == None):
            return Response("Invalid loginToken", mimetype="plain/text", status=403)
        comment_id_info = dbhelpers.run_select_statement("SELECT id FROM comment c WHERE c.id =?", [comment_id])
        if (comment_id_info == None):
            return Response("Comment does not exist", mimetype="plain/text", status=404)
        return Response("Comment already liked", mimetype="plain/text", status=409) 
    
    comments = dbhelpers.run_select_statement("SELECT cl.comment_id, cl.user_id, u.username from comment_like cl inner join `user` u ON cl.user_id = u.id where cl.comment_id =?", [comment_id,])
   
    if (comments == None or len(comments) != 1):
        return Response("Error fetching comment", mimetype="text/plain", status=500)
    
    comments_likes_dictionary = {
        "commentId": comments[0][0],
        "userId": comments[0][1],
        "username": comments[0][2],
    }
    comments_likes_json = json.dumps(comments_likes_dictionary, default=str)
    return Response(comments_likes_json, mimetype="application/json", status=201)
