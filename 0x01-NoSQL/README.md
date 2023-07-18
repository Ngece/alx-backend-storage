0-list_databases                a script that lists all databases in MongoDB.



1-use_or_create_database        a script that creates or uses the database my_db




2-insert                        a script that inserts a document in the collection school



3-all                           a script that lists all documents in the collection school



4-match                         a script that lists all documents with name="Holberton school" in the collection school



5-count                         a script that displays the number of documents in the collection school



6-update                        a script that adds a new attribute to a document in the collection school: 
                                The script updates only document with name="Holberton school" (all of them)
                                The update adds the attribute address with the value “972 Mission street”



7-delete                        a script that deletes all documents with name="Holberton school" in the collection school



8-all.py                        a Python function that lists all documents in a collection:
                                Prototype: def list_all(mongo_collection):
                                Return an empty list if no document in the collection
                                mongo_collection will be the pymongo collection object




9-insert_school.py              a Python function that inserts a new document in a collection based on kwargs:
                                Prototype: def insert_school(mongo_collection, **kwargs):
                                mongo_collection will be the pymongo collection object
                                Returns the new _id



10-update_topics.py             a Python function that changes all topics of a school document based on the name:
                                Prototype: def update_topics(mongo_collection, name, topics):
                                mongo_collection will be the pymongo collection object
                                name (string) will be the school name to update
                                topics (list of strings) will be the list of topics approached in the school



11-schools_by_topic.py          a Python function that returns the list of school having a specific topic:
                                Prototype: def schools_by_topic(mongo_collection, topic):
                                mongo_collection will be the pymongo collection object
                                topic (string) will be topic searched



12-log_stats.py                 a Python script that provides some stats about Nginx logs stored in MongoDB:



100-find                        a script that lists all documents with name starting by Holberton in the collection school:



101-students.py                 a Python function that returns all students sorted by average score:
                                Prototype: def top_students(mongo_collection):
                                mongo_collection will be the pymongo collection object
                                The top must be ordered
                                The average score must be part of each item returns with key = averageScore



102-log_stats.py                Improves 12-log_stats.py by adding the top 10 of the most present IPs in the collection nginx of the database logs:
