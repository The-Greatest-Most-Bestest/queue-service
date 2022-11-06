from request_handler import Handler
import configparser
from MongoDBProxy import MongoAPI
from flask import Flask, request
from flask_cors import CORS
import json
from datetime import datetime
from Notifications import NotificationPublisher

config = configparser.ConfigParser()
config.read_file(open('config/config.ini', 'r'))

mdb = MongoAPI(config.get("mdb", "url"), config.get("mdb", "password"))

publisher = NotificationPublisher(
    host=config.get("rmq", "host"),
    username=config.get("rmq", "username"),
    password=config.get("rmq", "password")
)

publisher.check()

handler = Handler(mdb, publisher)

CT = {"Content-Type": "application/json"}

app = Flask(__name__)
CORS(app)

@app.route('/add')
def enqueue():
    user = request.args.get('name')
    bid = request.args.get('uid')
    user_email = request.args.get('email')
    user_phone = request.args.get('phone')

    cid = request.args.get('id')

    if None in [user, bid, cid]:
        return json.dumps(
            {
                "response": 400,
                "message": "Missing required args"
            }
        ), 400, CT

    if user_email is None and user_phone is None:
        return json.dumps(
            {
                "response": 400,
                "message": "Missing required args; must provide contact info"
            }
        ), 400, CT

    # Do further validation here

    entry = {
        "id": bid,
        "name": user,
        "contact_info": {
            "phone": user_phone,
            "email": user_email
        },
        "time_added": datetime.now().isoformat()
    }


    resp, code = handler.enqueue(entry, cid)

    return resp, code, CT

@app.route('/status')
def status():
    cid = request.args.get('cid')
    uid = request.args.get('uid')

    resp, code = handler.status(cid, uid)

    return resp, code, CT

@app.route('/cancel')
def cancel():
    cid = request.args.get('cid')
    uid = request.args.get('uid')

    resp, code = handler.cancel(cid, uid)

    return resp, code, CT


@app.route('/check-in')
def checkin():
    item_id = request.args.get('id')

    resp, code = handler.checkin(item_id)

    return resp, code, CT

@app.route('/categories')
def categories():
    space = request.args.get('space')

    resp, code = handler.categories(space)

    return resp, code, CT

if __name__ == '__main__':
    app.run(host='0.0.0.0')