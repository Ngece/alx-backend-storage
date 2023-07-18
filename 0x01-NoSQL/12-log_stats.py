#!/usr/bin/env python3
"""provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')

db = client['logs']
collection = db['nginx']

total_logs = collection.count_documents({})

print(f"{total_logs} logs")

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    count = collection.count_documents({"method": method})
    print(f"method {method}: {count}")

status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
print(f"{status_check_count} status check")

client.close()
