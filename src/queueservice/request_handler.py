from queueservice.MongoDBProxy import MongoDBProxy


class Handler:
    def __init__(self):
        self.proxy = MongoDBProxy('temp')

    def enqueue(self, user_id, asset_id):
        queue = self.proxy.query(f"id={asset_id}")

        queue.append(user_id)

        self.proxy.update(f"id={asset_id}", queue)

        return {'success': True, 'position': len(queue)}