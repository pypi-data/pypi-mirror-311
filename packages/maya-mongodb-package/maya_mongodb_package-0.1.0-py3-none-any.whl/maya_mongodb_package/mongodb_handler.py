import logging
import pymongo

# Initialize logging
logger = logging.getLogger(__name__)

# MongoDB handler class for connecting to MongoDB
class MongoDBHandler:
    def __init__(self, mongodb_uri, db_name, collection_name: str):
        try:
            self.client = pymongo.MongoClient(mongodb_uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def find_document(self, capture_id : str):
        try:
            return self.collection.find_one({"_id": capture_id})
        except Exception as e:
            logger.error(f"Failed to find document in MongoDB: {e}")
            raise

    def upsert_capture(self, message: dict):
        try:
            print("message going to store in db\n",message)
            self.collection.insert_one(message)
            logger.info(f"Message stored in MongoDB: {message}")
        except Exception as e:
            logger.error(f"Failed to store message in MongoDB: {e}")
            raise

    def update_document(self, capture_id: str, update_fields: dict):
        try:
            self.collection.update_one({"_id": capture_id}, {"$set": update_fields})
            logger.info(f"Updated MongoDB document {capture_id} with fields: {update_fields}")
        except Exception as e:
            logger.error(f"Failed to update document in MongoDB: {e}")
            raise

