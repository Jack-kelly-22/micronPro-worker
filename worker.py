import uuid
import os
from app import create_app
from flask import Flask, request
from LocalWorker import LocalWorker
from backend_vars import scheduler
app = create_app()
localworker = LocalWorker()


@app.route("/rm_folder", methods=["POST"])
def delete_folder():
    # data = request.get_json(force=True)
    folder = request.get_data(as_text=True).split("=")[1]
    print(folder)
    if folder:
        resp = localworker.delete_image_folder(folder)
        print("RESponse: ", resp)
        return resp
    return {"msg": "No folder specified"}


@app.route("/new_job", methods=["POST"])
def post_job():
    data = request.get_json(force=True)
    data['job_id'] = data['job_name'] + "_" + str(uuid.uuid4()).replace("-", "")
    print(data)
    scheduler.add_job(localworker.start_job, trigger="date", args=[data])
    return {"status": "ok","job_id": data['job_id']}


@app.route("/folders", methods=["POST"])
# @jwt_required()
def get_folders():
    """should get folders of all active workers return folders and files inside"""
    """get folders on specified worker computer"""
    data = request.get_json()

    folders = localworker.get_image_folders()
    folder_ls = []
    for folder in folders:
        folder_ls.append({folder: folders[folder]})
    print("FOLDERS returning:", folder_ls)
    return {"folders": folder_ls}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    app.run(port=60, debug=True, use_reloader=True)
