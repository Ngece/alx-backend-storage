#!/usr/bin/env python3
"""Improve 12-log_stats.py by adding the top 10 of the most present IPs in the collection nginx of the database logs"""

from pymongo import MongoClient

if __name__ == "__main__":
    """ Database: logs
        Collection: nginx
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    n_logs = nginx_collection.count_documents({})
    print(f'{n_logs} logs')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
        )
    print(f'{status_check} status check')

    print('IPs:')
    ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
        ])
    for ip in ips:
        print(f'\t{ip.get("_id")}: {ip.get("count")}')
