from flask import Flask, request
from flask_cors import CORS
from backend_vars import configFile, log, scheduler
from endpoints import tasks
import atexit


POLL_INTERVAL = 30


def create_app():
    app = Flask(__name__)
    CORS(app)
    # setup scheduler to let the backend know that it's running
    scheduler.add_job(func=tasks.send_here, trigger="interval", seconds=POLL_INTERVAL)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return app
