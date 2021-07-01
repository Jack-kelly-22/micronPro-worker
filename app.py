from flask import Flask,request
from flask_cors import CORS
# from backend_vars import configFile, log


def create_app():
    app = Flask(__name__)
    CORS(app)
    # app.register_blueprint(job_blueprint)
    return app

# app = Flask("worker")

# CORS(app)
# app.route("/start_job",methods = ["POST"])
# def start_job():
#     data = request.get_json(force=True)
#     print("would start job")

# app.run_server()
