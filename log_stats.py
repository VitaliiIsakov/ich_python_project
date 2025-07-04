from pymongo import MongoClient
from typing import List, Tuple, Dict, Any
import settings


# Connect to MongoDB
client = MongoClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DBNAME]
collection = db[settings.MONGODB_COLLECTION]


def get_top_queries(limit: int = 5) -> List[Tuple[str, int]]:
    """
    Get the most frequent search query parameters.

    Args:
        limit (int): Number of top queries to return.

    Returns:
        List[Tuple[str, int]]: List of tuples (query parameters as string, count).
    """
    pipeline = [
        {"$group": {"_id": "$params", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    results = collection.aggregate(pipeline)
    return [(str(doc["_id"]), doc["count"]) for doc in results]


def get_last_queries(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get the most recent unique search queries.

    Args:
        limit (int): Number of recent queries to return.

    Returns:
        List[Dict[str, Any]]: List of query documents.
    """
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {"$group": {"_id": "$params", "doc": {"$first": "$$ROOT"}}},
        {"$replaceRoot": {"newRoot": "$doc"}},
        {"$sort": {"timestamp": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))