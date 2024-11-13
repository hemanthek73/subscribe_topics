from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # You can use other databases as well
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
with app.app_context():
    db.create_all()
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User registered successfully",
        "user_id": new_user.id
    })
@app.route('/topics', methods=['POST'])
def create_topic():
    topic_name = request.form.get('topic_name')
    if not topic_name:
        return jsonify({"error": "Topic name is required"}), 400
    
    new_topic = Topic(name=topic_name)
    db.session.add(new_topic)
    db.session.commit()
    
    return jsonify({
        "message": "Topic created successfully",
        "topic_id": new_topic.id
    })
@app.route('/subscribe', methods=['POST'])
def subscribe():
    user_id = request.form.get('user_id')
    topic_id = request.form.get('topic_id')
    
    if not user_id or not topic_id:
        return jsonify({"error": "User ID and Topic ID are required"}), 400
    
    # Check if subscription exists
    existing_subscription = Subscription.query.filter_by(user_id=user_id, topic_id=topic_id).first()
    
    if existing_subscription:
        return jsonify({"message": "User is already subscribed to this topic"}), 400
    
    # Create new subscription
    new_subscription = Subscription(user_id=user_id, topic_id=topic_id)
    db.session.add(new_subscription)
    db.session.commit()
    
    return jsonify({"message": "Subscription successful"})
@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    # Get all topic IDs the user is subscribed to
    subscribed_topic_ids = [sub.topic_id for sub in Subscription.query.filter_by(user_id=user_id).all()]
    
    # Get all topics not in the user's subscriptions
    new_topics = Topic.query.filter(Topic.id.notin_(subscribed_topic_ids)).all()
    
    return jsonify({
        "new_topics": [{"topic_id": topic.id, "name": topic.name} for topic in new_topics]
    })
@app.route('/subscriptions/<user_id>', methods=['GET'])
def get_subscriptions(user_id):
    # Get all topics the user is subscribed to
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    subscribed_topics = [{"topic_id": sub.topic_id, "name": Topic.query.get(sub.topic_id).name} for sub in subscriptions]
    
    return jsonify({"user_id": user_id, "subscribed_topics": subscribed_topics})



if __name__ == '__main__':
    app.run(debug=True)
