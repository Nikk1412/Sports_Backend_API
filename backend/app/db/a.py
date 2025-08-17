import uuid
import pymongo
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.sports
collection = db.matches

for doc in collection.find({"date_time": {"$type": "string"}}):
    try:
        # Convert ISO string with Z into datetime
        dt = datetime.datetime.fromisoformat(doc["date_time"].replace("Z", "+00:00"))

        # Update the document with proper datetime
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"date_time": dt}}
        )
        print(f"Updated: {doc['_id']} -> {dt}")

    except Exception as e:
        print(f"Failed for {doc['_id']}: {e}")
