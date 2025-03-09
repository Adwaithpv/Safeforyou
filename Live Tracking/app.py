from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("live-location-2524d-firebase-adminsdk-fbsvc-1c76dc64d7.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://live-location-2524d-default-rtdb.firebaseio.com/'
})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
