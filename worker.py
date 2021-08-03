
import os
from app import create_app
from flask import Flask, request
from flask_cors import CORS
from backend_vars import localWorker,scheduler
import json
app = create_app()
CORS(app,origins=["http://localhost:5080","http://localhost:8000", "https://micron-pro-frontend.herokuapp.com/admin/","*"])

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


# @app.route("/new_job", methods=["POST"])
# def post_job():
#     print(request.get_json())
#     data = request.get_json()
#     # data = json.dump(request.get_data(as_text=True))
#     data['job_id'] = data['job_nameπ'] + "_" + str(uuid.uuid4()).replace("-", "")

#     scheduler.add_job(localworker.start_job, trigger="date", args=[data])
#     return {"status": "ok"}

@app.route("/delete_job", methods=["POST"])
def delete_job():
    data = request.get_json()
    localWorker.remove_job(data['job_name'])
    return {"msg": "Job succussfully delete(on worker)"}


# @app.route("/update_job', methods=["POST"])
# def update_job():
#     data = request.get_json(force=True)
#     if "action" in data.keys():
#         if data['action'] == "add_folder":
#             localworker.add_folder_to_job(data['folder'], data['job_name'])


@app.route("/folders", methods=["POST"])
# @jwt_required()
def get_folders():
    """should get folders of all active workers return folders and files inside"""
    """get folders on specified worker computer"""
    data = request.get_json()

    folders = localWorker.get_image_folders()
    folder_ls = []
    for folder in folders:
        folder_ls.append({folder: folders[folder]})
    print("FOLDERS returning:", folder_ls) 
    return {"folders": folder_ls}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    app.run(port=60, debug=True, use_reloader=True)
