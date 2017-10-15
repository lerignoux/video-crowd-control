
import argparse
import base64
import json
import logging
# from http://flask.pocoo.org/ tutorial
from flask import Flask, render_template, request
import uuid

from mongo_handler import MongoHandler
from video_handler import VideoHandler


log = logging.getLogger("video_crowd_control")

parser = argparse.ArgumentParser(description='Enable users to review some videos.')
parser.add_argument('--debug', '-d', dest='debug',
                    action='store_true',
                    help='Debug mode')

app = Flask(__name__)
app.secret_key = "test"

MongoHandler().init_db()


@app.before_first_request
def initialize():
    logger = logging.getLogger("video_crowd_control")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        """%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s"""
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/video', methods=['GET'])
def video():
    video_query = request.args.get('filequery')
    if video_query is not None:
        return json.dumps(VideoHandler().get_video(base64.b64decode(video_query)))

    return json.dumps(VideoHandler().get_best_video())


@app.route('/video/rate', methods=['POST'])
def rate():
    """
    Upload a video rating
    """
    data = json.loads(request.data)
    version = data.get('version')
    try:
        name = data['name']
        rating = data['rating']
    except KeyError as e:
        return json.dumps({"code": 404, "err": e})
    feedback = data.get('feedback')
    certified = data.get('certified', False)
    MongoHandler().add_feedback(name, version, rating, feedback=feedback, certified=certified)
    return json.dumps({"code": 200})


@app.route('/video/stats', methods=['GET'])
def stats():
    """
    get videos ratings
    """
    version = request.args.get('version')
    stats = MongoHandler().get_statistics(version=version)
    return json.dumps({"code": 200, "data": stats})


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


if __name__ == "__main__":
    args = parser.parse_args()

    app.run()
