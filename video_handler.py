import logging
import os
import random
import re

from mongo_handler import MongoHandler

log = logging.getLogger("video_crowd_control")


class VideoHandler(object):

    video_folder = '/app/static/videos/'

    def __init__(self):
        self.fileregex = r".*\.mp4"

    def list_videos(self):
        """
        list all available videos
        """
        result = []
        for dirname, dirnames, filenames in os.walk(self.video_folder):
            for filename in filenames:
                if re.match(self.fileregex, filename):
                    result.append(os.path.join(dirname, filename))
        return result

    def get_video(self, query):
        videofile = query
        statbuf = os.stat(os.path.join(self.video_folder, videofile))
        return {'filename': videofile, 'version': statbuf.st_mtime}

    def get_best_video(self):
        """
        Return a random video among the best videos to rate
        """
        videos = self.get_unrated_videos() or self.list_videos()
        bestfile = random.choice(videos)
        version = os.path.getmtime(bestfile)
        return {'filename': bestfile[len(self.video_folder):], 'version': version}

    def get_unrated_videos(self):
        unrated = []
        videos = self.list_videos()
        for vid in videos:
            if not MongoHandler().get_statistics(name=vid, version=os.path.getmtime(vid)):
                unrated.append(vid)
        return unrated
