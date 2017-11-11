import logging
import pymongo

from pymongo import MongoClient

log = logging.getLogger("video_crowd_control")


class MongoHandler(object):

    def __init__(self):
        client = MongoClient('mongo', 27017)
        self.db = client.videos
        self.collection = self.db.statistics

    def init_db(self):
        self.db.profiles.create_index([('version', pymongo.ASCENDING), ('name', pymongo.ASCENDING)], unique=True)

    def get_statistics(self, name=None, version=None):
        query = {}
        if name is not None:
            query['name'] = name
        if version is not None:
            query['version'] = version
        return list(self.collection.find({}, {'_id': 0}).sort(
            [('feedback.certified_bug', -1), ('feedback.certified_bad', -1), ('feedback.bug', -1), ('feedback.bad', -1)]
        ))

    def insert_new(self, name, version):
        entry = {
            "name": name,
            "version": version,
            "feedback": {
                'good': 0,
                'bad': 0,
                'bug': 0,
                'certified_good': 0,
                'certified_bad': 0,
                'certified_bug': 0,
                'comments': []
            }
        }
        result = self.collection.insert_one(entry)
        return result == 1

    def add_feedback(self, name, version, rating, feedback=None, certified=False):
        if not self.collection.find_one({"name": name, "version": version}):
            self.insert_new(name, version)

        if rating == 1:
            field = 'good'
        elif rating == 0:
            field = 'bad'
        elif rating == -1:
            field = 'bug'
        else:
            raise Exception("%s rating unknown" % rating)
        if certified:
            field = "certified_%s" % field

        query = {'$inc': {"feedback.%s" % field: 1}}

        if feedback is not None:
            query['$push'] = {"feedback.comments": feedback}

        result = self.collection.update_one({'name': name, 'version': version}, query)
        return result == 1
