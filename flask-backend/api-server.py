from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# PyMongo Stuff
client = MongoClient("mongodb+srv://mfngoi:UUkHZnMzVW6x9jIo@cluster0.ltgs7ps.mongodb.net/?retryWrites=true&w=majority")
db = client.queues

# API Route
@app.route("/")
def home():
    return "Welcome to the Queue Service App"

@app.route("/team")
def team():
    return {"members": ["Matthew", "Brianna", "Lily", "Riley", "Leo"]}

@app.route("/queue")
def queue():
    return db.list_collection_names()

if __name__ == "__main__":
    app.run()