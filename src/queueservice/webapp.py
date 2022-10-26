from request_handler import Handler
import configparser
from MongoDBProxy import MongoAPI
from flask import Flask, request
import json
from datetime import datetime

config = configparser.ConfigParser()
config.read_file('config/config.ini')

mdb = MongoAPI(config.get("mdb", "url"), config.get("mdb", "password"))
handler = Handler(mdb)

CT = {"Content-Type": "application/json"}

app = Flask(__name__)

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
        "time": datetime.now().isoformat()
    }


    resp, code = handler.enqueue(entry, cid)

    return resp, code, CT

if __name__ == '__main__':
    app.run(host='0.0.0.0')