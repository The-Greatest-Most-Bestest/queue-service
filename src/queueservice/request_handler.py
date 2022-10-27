from MongoDBProxy import MongoAPI
import json

class Handler:
    def __init__(self, mdb : MongoAPI):
        self.proxy = mdb

    def enqueue(self, user, id):
        try:
            queue = self.proxy.get_queue_for_category(id)

            for e in queue:
                if e['id'] == user['id']:
                    return json.dumps({
                        "response": 400,
                        "message": f"User {user['name']}({user['id']}) is already in this queue"
                    }), 400

            queue.append(user)
            self.proxy.update_queue_for_category(id, queue)

            return json.dumps({
                        "response": 200,
                        "message": f"User {user['name']}({user['id']}) successfully enqueued",
                        "position": len(queue)
            }), 200
        except:
            return json.dumps({
                        "response": 500,
                        "message": f"User {user['name']}({user['id']}) is already in this queue"
            }), 500

