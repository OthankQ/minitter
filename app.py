from flask import Flask, request, jsonify

app = Flask(__name__)
app.id_count = 1
app.users = {}
app.tweets = []


@app.route("/ping", methods=['GET'])
def ping():
    return "Pong"

# Sign-up
@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count += 1

    return jsonify(new_user)

# 300 Letter limited tweet
@app.route("/tweet", methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return 'Non existent user', 400

    if len(tweet) > 300:
        return 'Tweet is too long', 400

    app.tweets.append({
        'user_id': user_id,
        'tweet': tweet
    })

    return 'Your tweet has been submitted', 200

# follow other users
@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload["id"])
    user_to_follow = int(payload["follow"])

    if user_id not in app.users or user_to_follow not in app.users:
        return 'User with that id does not exist', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_to_follow)

    return jsonify(user)

# unfollow other users
@app.route("/unfollow", methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload["id"])
    user_to_unfollow = int(payload["unfollow"])
