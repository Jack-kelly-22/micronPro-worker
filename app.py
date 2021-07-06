from flask import Flask,request
from flask_cors import CORS
# from backend_vars import configFile, log


def create_app():
    app = Flask(__name__)
    CORS(app)
    return app



# CORS(app)
# app.route("/start_job",methods = ["POST"])
# def start_job():
#     data = request.get_json(force=True)
#     print("would start job")

# app.run_server()
