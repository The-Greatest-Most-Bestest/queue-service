import re
import uuid
import json
from bson import ObjectId, json_util
from pymongo import MongoClient

# Helper class for mongodb
class MongoAPI:

    # Creates client to connect to Mongo DB
    def __init__(self, url: str, password: str):
        
        # Load url with password
        cluster_key = re.sub("<password>", password, url)

        # Create client and connect to database 'queues'
        self.client = MongoClient(cluster_key)
        self.db = self.client['test_queue_service']     # Refers to database name in MongoDB account

    def get_queue_for_category(self, id: uuid):

        # Connect to queue table (collection) in the database
        queue = self.db['queue']
        
        # Retrive queue with specified id
        data = queue.find_one({"id": id})

        # Check if queue exists in table
        if data:
            return data["queue"]

        return "Queue not found with specified id."
        
    def update_queue_for_category(self, id: uuid, new_queue_entry: list):

        # Connect to queue table (collection) in the database
        queue = self.db['queue']
        
        # Define new value to be pushed to queue array
        new_value = {"$push": new_queue_entry}

        # Update the queue with specified id
        queue.update_one({"id": id}, new_value)


    def get_category_for_item(self, id: str) -> uuid:

        catagory_uuid = 0

        # Connect to catagory table (collection) in the database
        queue = self.db['category']

        data = queue.find()

        if data:
            for doc in data:

                catagory_uuid = doc["id"]
                found_item = False

                for item in doc["items"]:
                    if item == id:
                        found_item = True
                        break
                        
                if found_item:
                    break

        return catagory_uuid