# Admin
from flask import Flask
app = Flask(__name__)
# To run this app: python C:\Users\Andrew\Documents\GitHub\\WebTool_Hermes\app.py

#
@app.route("/")
def home():
    return "Hello world! This is site is dedicated to the bestest and most supportive viewer in Southbank!"
