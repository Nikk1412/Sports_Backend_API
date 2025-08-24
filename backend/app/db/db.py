import uuid
import pymongo
import datetime

client = pymongo.MongoClient("mongodb+srv://nikhilmohite:pYFM70m8SI4cNOs1@cluster0.ttzletl.mongodb.net/")

db = client.sports
collection = db.matches

async def delete_match(data):
    return collection.delete_one({"_id": data["id"]})

async def update_match(data):
    if "date_time" in data:
        # Parse ISO8601 string with Z (UTC)
        data["date_time"] = datetime.datetime.fromisoformat(
            data["date_time"].replace("Z", "+00:00")
        )
    return collection.update_one({"_id": data["id"]}, {"$set": data})

async def create_match(data):
    if "date_time" in data:
        # Parse ISO8601 string with Z (UTC)
        data["date_time"] = datetime.datetime.fromisoformat(
            data["date_time"].replace("Z", "+00:00")
        )
    data["_id"] = str(uuid.uuid4())
    print(collection.insert_one(data))
    return True

def get_department_matches_filtered(filters: dict):
    query = {}

    if filters["is_final"] != "all":
        query["is_final"] = filters["is_final"]

    if filters["dept"] != "all":
        query["department"] = {"$or":[
            {"team1_id": filters["dept"]}, 
            {"team2_id": filters["dept"]}
        ]}

    if filters["year"] != "all":
        start = datetime.datetime(filters["year"], 1, 1)
        end = datetime.datetime(filters["year"] + 1, 1, 1)
        query["date_time"] = {"$gte": start, "$lt": end}

    if filters["sport"] != "all":
        query["sport"] = filters["sport"]
    
    print(query)

    cursor = collection.find(query)
    # TODO: sort for `top`

    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # serialize ObjectId
        results.append(doc)

    return results


# def get_final_matches(year: int):
#     start = datetime.datetime(year, 1, 1)
#     end = datetime.datetime(year + 1, 1, 1)
#     data = list(collection.find({
#         "is_final": True
#         # "date_time": {"$gte": start, "$lt": end}
#     }, {"_id": 0}
#     )) # TODO: Add projection
    

def get_department_matches(department):
    year = datetime.datetime.now().year
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime(year + 1, 1, 1)

    query = {
        "date_time": {
            "$gte": start, "$lt": end
        },
        "$or": [
            {"team1": department},
            {"team2": department},
        ]
    }
    return list(collection.find(query))

def get_points_data(year: int):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime(year + 1, 1, 1)

    query = {
        "status": "ended",
        "is_final": True,
        "date_time": {"$gte": start, "$lt": end},  # assuming field is called "date"
    }

    cursor = collection.find(query, {"team1": 1, "team2": 1, "winner_id": 1})

    data_dict = {}
    for match in cursor:
        t1, t2, winner = match["team1"], match["team2"], match["winner_id"]
        data_dict.setdefault(t1, 0)
        data_dict.setdefault(t2, 0)
        if winner == t1:
            data_dict[t1] += 20
            data_dict[t2] += 10
        else:
            data_dict[t2] += 20
            data_dict[t1] += 10
    return data_dict

