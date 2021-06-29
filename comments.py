from flask import request, Response
from application import app
import dbhelpers
import json

@app.get("/api/comments")
def api_get_comments():
    try:
        tweet_id = int(request.args.get("tweetId", -1))
    except ValueError:
        return Response("tweetID must be a number.", mimetype="text/plain", status=400)
    
    if (tweet_id == -1):
        comments_info = get_comments("SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at FROM comment c inner join `user` u on u.id = c.user_id", [])
    else:
        comments_info = get_comments("SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at FROM comment c inner join `user` u on u.id = c.user_id where c.tweet_id = ?", [tweet_id])

    if (comments_info == None):
        return Response("Failed to GET comments.", mimetype="text/plain", status=500)

    if (len(comments_info) == 0):
        comment = get_comments("SELECT id FROM tweet WHERE id=?", [tweet_id])
        if (len(comment) == 0):
            return Response("Tweet does not exist.", mimetype="text/plain", status=404)

    comments_json = json.dumps(comments_info, default=str)
    return Response(comments_json, mimetype="application/json", status=200)

def get_comments(sql_statement, sql_params):
    comments_properties = dbhelpers.run_select_statement(sql_statement, sql_params)
    
    if (comments_properties == None):
        return None
    comments = []
    for comment_properties in comments_properties:
        comment = {
            "commentId": comment_properties[0],
            "tweetId": comment_properties[1],
            "userId": comment_properties[2],
            "username": comment_properties[3],
            "content": comment_properties[4],
            "createdAt": comment_properties[5],
        }
        comments.append(comment)
    return comments
