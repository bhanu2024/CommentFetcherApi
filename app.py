from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    response = requests.get('https://dev.ylytic.com/ylytic/test')
    comments = response.json()

    return jsonify(comments)


@app.route('/search')
def search_comments():
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    response = requests.get('https://dev.ylytic.com/ylytic/test')
    data = response.json()

    if search_author or at_from or at_to or like_from or like_to or reply_from or reply_to or search_text:
        filtered_comments = []
        for comment in data["comments"]:
            if search_author and search_author.lower() not in comment['author'].lower():
                continue
            if at_from and datetime.strptime(comment['at'], "%a, %d %b %Y %H:%M:%S %Z") < datetime.strptime(at_from, "%d-%m-%Y"):
                continue
            if at_to and datetime.strptime(comment['at'], "%a, %d %b %Y %H:%M:%S %Z") > datetime.strptime(at_to, "%d-%m-%Y"):
                continue
            if like_from and comment['like'] < int(like_from):
                continue
            if like_to and comment['like'] > int(like_to):
                continue
            if reply_from and comment['reply'] < int(reply_from):
                continue
            if reply_to and comment['reply'] > int(reply_to):
                continue
            if search_text and search_text.lower() not in comment['text'].lower():
                continue
            filtered_comments.append(comment)
        return {'comments': filtered_comments}
    else:
        return {"output": "No parameters given to search",
                'comments': data["comments"]}



if __name__ == '__main__':
    app.run()