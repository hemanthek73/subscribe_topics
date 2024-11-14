
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = 'my_secret_key'  # Replace with a more secure key in production

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # You can use other databases as well
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#------------------creating a model---------------------------------------------->

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password =password # bcrypt.generate_password_hash(password).decode('utf-8')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100),nullable=False)
# Define the Topic model
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# Define the Subscription model
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

#------------------student register--------------------------------------------------

@app.route('/studentregister', methods=['POST'])
def studentregister():
    email = request.form['email']
    # Check if email already exists
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists. Please use a different email.")
        return redirect(url_for('register'))
    else:
        # Proceed with user registration
        password = request.form['password']
        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Users(email=email, password=password)#hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
#--------------- Route for login --------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.password != password:
        return jsonify({"error": "Invalid credentials"}), 400
    if user and password:
        print("the email and password matched")
    return jsonify({"success": True}), 200


#-----------------------user register for a topic---------------------------------

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

# -----------------Route for creating a new topic--------------------------------------

@app.route('/topics', methods=['POST'])
def create_topic():
    topic_name = request.form.get('topic_name')
    if not topic_name:
        return jsonify({"error": "Topic name is required"}), 400
    
    new_topic = Topic(name=topic_name)
    db.session.add(new_topic)
    db.session.commit()
    
    return jsonify({"message": "Topic created successfully", "topic_id": new_topic.id})

#---------------- Route for subscribing to a topic----------------------------------------

@app.route('/subscribe', methods=['POST'])
def subscribe():
    user_id = request.form.get('user_id')
    topic_id = request.form.get('topic_id')
    
    if not user_id or not topic_id:
        return jsonify({"error": "User ID and Topic ID are required"}), 400
    
    # Check if subscription already exists
    existing_subscription = Subscription.query.filter_by(user_id=user_id, topic_id=topic_id).first()
    if existing_subscription:
        return jsonify({"message": "User is already subscribed to this topic"}), 400
    
    # Create new subscription
    new_subscription = Subscription(user_id=user_id, topic_id=topic_id)
    db.session.add(new_subscription)
    db.session.commit()
    
    return jsonify({"message": "Subscription successful"})

# ---------Route for getting notifications (new topics)--------------------------------

@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    # Get all topic IDs the user is subscribed to
    subscribed_topic_ids = [sub.topic_id for sub in Subscription.query.filter_by(user_id=user_id).all()]
    
    # Get all topics not in the user's subscriptions
    new_topics = Topic.query.filter(Topic.id.notin_(subscribed_topic_ids)).all()
    
    return jsonify({
        "new_topics": [{"topic_id": topic.id, "name": topic.name} for topic in new_topics]
    })

# -----------Route for getting subscriptions-----------------------------------------

@app.route('/subscriptions/<user_id>', methods=['GET'])
def get_subscriptions(user_id):
    # Get all topics the user is subscribed to
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    subscribed_topics = [{"topic_id": sub.topic_id, "name": Topic.query.get(sub.topic_id).name} for sub in subscriptions]
    
    return jsonify({"user_id": user_id, "subscribed_topics": subscribed_topics})

#-----------logout page--------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
