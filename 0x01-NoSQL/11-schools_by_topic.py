#!/usr/bin/env python3
"""Contains a function that returns the list of school having a specific topic"""

def schools_by_topic(mongo_collection, topic):
    """returns the list of school having a specific topic"""
    if not mongo_collection:
        return []
    return list(mongo_collection.find({"topics": topic}))