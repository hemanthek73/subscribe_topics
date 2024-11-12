from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
users = {}
topics = {}
user_subscriptions = {}
user_id_counter = 1
topic_id_counter = 1


# -----------------Register the user with username ---------------------------------------------------------
 
@app.route('/register', methods=['POST'])
def register():
    global user_id_counter
    username = request.form.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user_id = str(user_id_counter)
    users[user_id] = {"username": username}
    user_id_counter += 1 # every new user the user_id will incrimented by 1

    return jsonify({
        "message": "User registered successfully",
        "user_id": user_id
    })
    

# ----------------adding the topics by topic_name -------------------------------------------------------

@app.route('/topics', methods=['POST'])
def create_topic():
    global topic_id_counter
    topic_name = request.form.get('topic_name')
    if not topic_name:
        return jsonify({"error": "Topic name is required"}), 400

    topic_id = str(topic_id_counter)
    topics[topic_id] = {"name": topic_name}
    topic_id_counter += 1 # every new topic the topic id also incriments
    return jsonify({
        "message": "Topic created successfully",
        "topic_id": topic_id
    })

# ----------------subscrbe the topic by topic id and user id --------------------------------------------

@app.route('/subscribe', methods=['POST'])
def subscribe():
    user_id = request.form.get('user_id')
    topic_id = request.form.get('topic_id')
    print("topic_id",topic_id)
    print("user_id",user_id)
    if not user_id or not topic_id:
        return jsonify({"error": "User ID and Topic ID are required"}), 400

    # Check if the user is already subscribed to the topic
    if user_id not in user_subscriptions:
        user_subscriptions[user_id] = []

    if topic_id not in user_subscriptions[user_id]:
        user_subscriptions[user_id].append(topic_id)
        print("user subsciption:",user_subscriptions)
        return jsonify({"message": f"User ID {user_id} subscribed to topic ID {topic_id}"}), 200
    else:
        return jsonify({"message": f"User {user_id} is already subscribed to topic {topic_id}"}), 400

# ----------------Notify the topic in a topic list other than he subscribed ------------------------------

@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    print(f"Checking notifications for user: {user_id}")
    
# Get the topic the user is already subscibed
    subscribed_topics = user_subscriptions.get(user_id, [])
    print(f"Subscribed topics for {user_id}: {subscribed_topics}")
    
# Identify topics the user not subscribed
    new_topics = []
    for tid, topic in topics.items():
        if tid not in subscribed_topics:  # Only include topics the user not subscribed 
            print(f"Adding un-subscribed topic: {topic['name']} with id: {tid}")
            new_topics.append({"topic_id": tid, "name": topic["name"]})

    print("Un-subscribed topics for notification:", new_topics)
    return jsonify({"new_topics": new_topics})

#----------------- get the subcribed topicname and topic id of user -------------------------------------

@app.route('/subscriptions/<user_id>', methods=['GET'])
def get_subscriptions(user_id):
    print(f"Checking subscriptions for user: {user_id}")
    if user_id not in user_subscriptions:
        return jsonify({"user_id": user_id, "subscribed_topics": []})

    subscribed_topics = []
    for tid in user_subscriptions[user_id]:
        topic = topics.get(tid)  
        print("topic:",topic)
        if topic:
            print(f"Adding topic: {topic['name']} with id: {tid}")
            subscribed_topics.append({"topic_id": tid, "name": topic["name"]})

    print(f"Subscribed topics for {user_id}: {subscribed_topics}")
    return jsonify({"user_id": user_id, "subscribed_topics": subscribed_topics})


if __name__ == '__main__':
    app.run(debug=True)
