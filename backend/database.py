# ReWear Clothing System - Database Initialization
# Using MongoDB with MongoEngine

from mongoengine import connect, disconnect

db = None


def init_mongodb(app):
    """Initialize MongoDB connection."""
    global db
    mongodb_url = app.config.get("MONGODB_URL", "mongodb://localhost:27017/rewear")

    # Avoid stale duplicate connections in dev reload cycles.
    disconnect(alias="default")

    db = connect(host=mongodb_url, alias="default")
    return db
