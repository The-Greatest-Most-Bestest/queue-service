from MongoDBProxy import MongoAPI
from Notifications import NotificationPublisher
import json

class Handler:
    def __init__(self, mdb : MongoAPI, publisher : NotificationPublisher):
        self.proxy = mdb
        self.publisher = publisher

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
                        "message": f"An error occurred"
            }), 500


    @staticmethod
    def __find_in_queue(id, queue):
        for i, u in enumerate(queue):
            if u['id'] == id:
                return i

        return -1

    def status(self, cid, uid):
        queue = self.proxy.get_queue_for_category(cid)

        if queue is None:
            return json.dumps({
                "response": 400,
                "message": f"queue for {cid} not found"
            }), 400

        pos = self.__find_in_queue(uid, queue)

        if pos == -1:
            return json.dumps({
                "response": 400,
                "message": f"user {uid} not found in queue for {cid}"
            }), 400

        return json.dumps({
            "response": 200,
            "message": pos + 1
        }), 200

    def cancel(self, cid, uid):
        queue = self.proxy.get_queue_for_category(cid)

        if queue is None:
            return json.dumps({
                "response": 400,
                "message": f"queue for {cid} not found"
            }), 400

        pos = self.__find_in_queue(uid, queue)

        if pos == -1:
            return json.dumps({
                "response": 400,
                "message": f"user {uid} not found in queue for {cid}"
            }), 400

        entry = queue.pop(pos)

        self.proxy.append_history(entry, "CANCELLED")
        self.proxy.update_queue_for_category(cid, queue)

        return json.dumps({
            "response": 200,
            "message": "Successfully cancelled"
        }), 200

    def categories(self, space):
        cats = self.proxy.get_categories()

        cats = [{"id": c['id'], "name": c['name'], "space": c['space']} for c in cats]

        if space is None:
            return json.dumps({
                "response": 200,
                "categories": cats
            }), 200
        else:
            return json.dumps({
                "response": 200,
                "categories": [c for c in cats if c['space'] == space]
            }), 200

    def checkin(self, id) -> tuple[str, int]:
        cid = self.proxy.get_category_for_item(id)

        if cid is None:
            return json.dumps({
                "response": 400,
                "message": f"No category found for item {id}"
            }), 400

        queue = self.proxy.get_queue_for_category(cid)

        if queue is None:
            return json.dumps({
                "response": 500,
                "message": f"No queue found for category {cid}. This should not happen! Possible db inconsistency"
            }), 500

        if len(queue) == 0:
            return json.dumps({
                "response": 200,
                "message": "Checkin successful. Queue is empty so no notification is required"
            }), 200

        next_user = queue.pop(0)

        with self.publisher:
            self.publisher.publish(next_user)

        self.proxy.append_history(next_user, "NOTIFIED")
        self.proxy.update_queue_for_category(cid, queue)

        return json.dumps({
            "response": 200,
            "message": "Checkin successful. Notified next user"
        }), 200