from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import openai
import logging
from flask_migrate import Migrate



# Add this line at the beginning of your app.py file to configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

migrate = Migrate(app, db)

from flask import request


@app.route('/delete_account', methods=['POST', 'DELETE'])
@login_required
def delete_account():
    if request.method == 'POST' or request.method == 'DELETE':
        # Check if the current user is authenticated
        if current_user.is_authenticated:
            # Delete the user record
            db.session.delete(current_user)
            db.session.commit()
            logout_user()  # Logout the user after deleting the account
            return redirect(url_for('index'))  # Redirect to the home page after successful deletion
    # If the user is not authenticated or the method is not POST or DELETE, return an error response
    return jsonify({'error': 'Unauthorized access'}), 403



@app.route('/delete_data', methods=['POST'])
@login_required
def delete_data():
    if request.method == 'POST':
        # Check if the current user is authenticated
        if current_user.is_authenticated:
            # Delete all past conversations associated with the current user
            PastConversation.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            return redirect(url_for('settings'))
    return render_template('error.html', error='Unauthorized access'), 403


# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")


# Define SQLAlchemy models
class PastConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_message = db.Column(db.String(255))
    chatbot_response = db.Column(db.String(255))
    user = db.relationship('User', backref='past_conversations')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Define routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return render_template('register.html', error='Username already exists')
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_input = request.json['message']
        chatbot_response, api_response = get_chatbot_response(user_input)

        # Store conversation in the database
        if current_user.is_authenticated:
            conversation = PastConversation(
                user_id=current_user.id,
                user_message=user_input,
                chatbot_response=chatbot_response
            )
            db.session.add(conversation)
            db.session.commit()

        return jsonify({'response': chatbot_response, 'api_response': api_response})
    except Exception as e:
        return jsonify({'error': str(e)})

# Define function to get chatbot response
# def get_chatbot_response(message):
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are chatting with a medical chatbot."},
#                 {"role": "user", "content": message}
#             ],
#             temperature=0.7,
#             max_tokens=500
#         )
#         api_response = response.to_dict()
#         chatbot_message = response.choices[0].message.content
        
#         if not chatbot_message:
#             chatbot_message = "I'm sorry, but I couldn't generate a complete response. Could you please provide more details or try asking a more specific question?"
        
#         return chatbot_message, api_response
#     except Exception as e:
#         return str(e), None

if __name__ == '__main__':
    app.run(debug=True)
