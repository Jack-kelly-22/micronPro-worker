from flask import Flask, request
from flask_cors import CORS
from backend_vars import configFile, log, scheduler
from endpoints import tasks
import atexit


POLL_INTERVAL = 30
QUEUE_POLL_INTERVAL = 20
FOLDER_INTERVAL = 60

def create_app():
    app = Flask(__name__)
    # CORS(app)
    # setup scheduler to let the backend know that it's running
    # scheduler.add_job(func=tasks.send_here, trigger="interval", seconds=POLL_INTERVAL)
    scheduler.add_job(func=tasks.post_folders, trigger="interval", seconds=FOLDER_INTERVAL)
    scheduler.add_job(func=tasks.check_queued, trigger="date")
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return app
