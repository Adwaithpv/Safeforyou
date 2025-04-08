# Import necessary modules from Flask and Firebase Admin SDK
from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db

# Initialize a Flask app instance
app = Flask(__name__)

# ----------------- Firebase Initialization ------------------

# Load Firebase credentials from a JSON file (downloaded from Firebase Console)
cred = credentials.Certificate("live-location-2524d-firebase-adminsdk-fbsvc-1c76dc64d7.json")

# Initialize the Firebase app with the given credentials and set the Realtime Database URL
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://live-location-2524d-default-rtdb.firebaseio.com/'
})

# ----------------- Routes ------------------

# Define the default route (homepage)
@app.route('/')
def index():
    # Render the index.html file from the 'templates' directory
    return render_template('index.html')

# ----------------- App Runner ------------------

# Start the Flask development server
# debug=True enables hot-reloading and error debugging
if __name__ == '__main__':
    app.run(debug=True)
