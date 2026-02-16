import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# If Mongo not available → use memory
if not MONGO_URI:
    print("⚠ MongoDB not configured — using in-memory storage")

    class FakeCollection:
        def __init__(self):
            self.data = []

        def find_one(self, query):
            for item in self.data:
                if item["question"] == query["question"]:
                    return item
            return None

        def insert_one(self, document):
            self.data.append(document)

    question_analysis_collection = FakeCollection()

else:
    from pymongo import MongoClient

    client = MongoClient(MONGO_URI)
    db = client["arikya_ai"]
    question_analysis_collection = db["question_analysis"]
