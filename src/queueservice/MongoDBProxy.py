import re
import uuid
import json
from datetime import datetime
from pymongo import MongoClient

# Helper class for mongodb
class MongoAPI:

    # Creates client to connect to Mongo DB
    def __init__(self, url: str, password: str):
        
        # Load url with password
        cluster_key = re.sub("<password>", password, url)

        # Create client and connect to database 'queues'
        self.client = MongoClient(cluster_key)
        self.db = self.client.get_database('queue_service') # !!! Hardcoded Element !!!

    # Retrieve the queue_array with the specified uuid
    def get_queue_for_category(self, id: uuid) -> list:

        # Connect to queue table in the database
        queue = self.db.get_collection('queue') # !!! Hardcoded Element !!!
        
        # Retrive document (row) with specified id
        document = queue.find_one({"id": str(id)})

        # Check if document with id exists in table
        if document:
            return document["queue"]

        return None
    
    # Replace the queue in the specified uuid with the queue_array
    def update_queue_for_category(self, id: uuid, queue_array: list):

        # Connect to queue table in the database
        queue = self.db.get_collection('queue') # !!! Hardcoded Element !!!

        # Create new queue array to set in queue
        new_queue_array = {
            "queue": []
        }
        for profiles in queue_array:
            new_queue_array["queue"].append(profiles)
        # Apply mongo instruction
        set_queue_array = {"$set": new_queue_array}

        # Update the queue with specified id
        queue.update_one({"id": str(id)}, set_queue_array)

    # Searches through the entire collection of 'category' 
    # for the item with the same uuid and returns the uuid of the related category
    def get_category_for_item(self, id: uuid) -> uuid:
        # Connect to category table in the database
        category = self.db.get_collection('category') # !!! Hardcoded Element !!!

        # Search through entire category table
        data = category.find()
        if data:
            for document in data:
                category_uuid = document["id"]

                for item in document["items"]:
                    if item == str(id):
                        return category_uuid     
        
        return None

    def get_categories(self):
        data = self.db.get_collection('category').find()

        return list(data) if data else []

    # Creates a new document (row) in the queue table (collection) with an empty queue_array
    def create_queue_document(self, category_id: uuid, queue_name: str):
        # Connect to queue table in the database
        queue = self.db.get_collection('queue') # !!! Hardcoded Element !!!

        # Create new document to be inserted to queue collection
        document = {
            "id": str(category_id),
            "queue_name": queue_name,
            "queue": [],
        }
        # Perform insertion
        queue.insert_one(document)

    # Removes specified document in the queue table
    def remove_queue_document(self, id: uuid):
        # Connect to queue table in the database
        queue = self.db.get_collection('queue') # !!! Hardcoded Element !!!

        # Query for document to be deleted
        query = {"id": str(id)}
        queue.delete_one(query)

    # Creates a new document (row) in the category table with an empty item array
    def create_category_document(self, category_id: uuid, category_name: str, space: str):
        # Connect to queue table in the database
        category = self.db.get_collection('category') # !!! Hardcoded Element !!!

        # Create new document to be inserted to category collection
        id = str(category_id)
        date_time = datetime.now().isoformat(sep='T')
        document = {
            "id": id,
            "name": category_name,
            "space": space,
            "items": [],
            "description": "",
            "img": "",
            "added_on": date_time
        }
        # Perform insertion
        category.insert_one(document)

    # Removes specified document in the category table
    def remove_category_document(self, id: uuid):
        # Connect to queue table in the database
        category = self.db.get_collection('category') # !!! Hardcoded Element !!!

        # Query for document to be deleted
        query = {"id": str(id)}
        category.delete_one(query)

    def create_category(self, category_name, category_space):
        id = str(uuid.uuid4())

        self.create_category_document(id, category_name, category_space)
        self.create_queue_document(id, category_name)

        return id

    def update_category_metadata(self, category_id, description, img_url):
        pass # Not yet implemented

    def delete_category(self, id):
        id = str(uuid.uuid4())

        self.remove_category_document(id)
        self.remove_queue_document(id)

    def add_item(self, category_id, item_id=None):
        if item_id is None:
            item_id = str(uuid.uuid4())

        # Connect to category table in the database
        category = self.db.get_collection('category')  # !!! Hardcoded Element !!!

        doc = category.find_one({"id": str(category_id)})

        if not doc:
            return

        item_list = doc['items']

        item_list.append(str(item_id))

        set_cat_array = {"$set": {"items": item_list}}

        category.update_one({"id": str(category_id)}, set_cat_array)

        return str(item_id)

    def remove_item(self, category_id, item_id):
        # Connect to category table in the database
        category = self.db.get_collection('category')  # !!! Hardcoded Element !!!

        doc = category.find_one({"id": str(category_id)})

        if not doc:
            return

        item_list = doc['items']

        for i, iid in enumerate(item_list):
            if iid == str(item_id):
                item_list.pop(i)
                break

        set_cat_array = {"$set": {"items": item_list}}

        category.update_one({"id": str(category_id)}, set_cat_array)

    def append_history(self, entry, status : str):
        entry['status'] = status
        entry['time_exit'] = datetime.now().isoformat(sep='T')

        history = self.db.get_collection('history')  # !!! Hardcoded Element !!!
        history.insert_one(entry)