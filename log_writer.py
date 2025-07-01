from pymongo import MongoClient
from datetime import datetime
from typing import Any, Dict
import settings

# Connect to MongoDB
client = MongoClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DBNAME]
collection = db[settings.MONGODB_COLLECTION]

def log_search(search_type: str, params: Dict[str, Any], results_count: int) -> None:
    """
    Save a search query to the database.

    Args:
        search_type: Type of search (e.g., "keyword", "genre+year").
        params: Search parameters as a dictionary.
        results_count: Number of results found.
    """
    doc = {
        "timestamp": datetime.now(),
        "search_type": search_type,
        "params": params,
        "results_count": results_count
    }
    try:
        collection.insert_one(doc)
    except Exception as e:
        print(f"Warning: Failed to save search log: {e}")