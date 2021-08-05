
import os
from app import create_app
from flask import Flask, request
from flask_cors import CORS
from backend_vars import localWorker,scheduler
import json
app = create_app()
CORS(app,origins=["http://localhost:5080","http://localhost:8000", "https://micron-pro-frontend.herokuapp.com","*"])

@app.route("/rm_folder", methods=["POST"])
def delete_folder():
    # data = request.get_json(force=True)
    folder = request.get_data(as_text=True).split("=")[1]
    print(folder)
    if folder:
        resp = localWorker.delete_image_folder(folder)
        print("RESponse: ", resp)
        return resp
    return {"msg": "No folder specified"}


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5004))
#     app.run(port=60, debug=True, use_reloader=True)
