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