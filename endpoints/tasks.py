import requests
from uuid import uuid4
from os import environ
from backend_vars import configFile, scheduler, localWorker,num_folders

config = configFile.get_configuration()

# def send_here():
#     print("Saying hey to the webserver :)")
#     self_url, self_name = config["SELF"]["URL"], config["SELF"]["NAME"]
#     # password = config['SELF']['PASS']
#     backend_url = config["HOST"]["URL"]
#     requests.post(
#         backend_url + "/hello", json={"self_url": self_url, "self_name": self_name}
#     )
#     print({"self_url": self_url, "self_name": self_name})

def post_folders():
    """sends folder data to the backend"""
    
    folders = localWorker.get_image_folders()
    backend_url = config["HOST"]["URL"]
    print("NAME: ", config["SELF"]["NAME"])
    db_folders = localWorker.client.micronProDB.workers.find_one({"name":config["SELF"]["NAME"]})
    print("DB:",dict(db_folders))
    if db_folders:
        # cleanup later
        db_folders1 = db_folders["folders"]
        db_folders = list(map(lambda x: list(x.keys())[0], db_folders1))
        print("DB_FOLDERS: ", db_folders)
        print("FOLDERS: ", folders)
        folders = [{folder:folders[folder]} for folder in folders.keys() if folder not in db_folders]
        # del_folders = [{folder:db_folders1[folder]} for folder in db_folders if folder not in folders.keys()]
        # if del_folders:
        #     print("Deleting folders: ", del_folders)
        #     localWorker.client.micronProDB.workers.update_one({"name": localWorker.name}, {"$pull":{"folders":{"$each": del_folders}}})
        print("FOUND {} NEW FOLDERS".format(len(folders)))
        print(folders)
    if len(folders):
        requests.post(backend_url + "/post_folders",json={"folders":folders,"name":config["SELF"]["NAME"]})
    else:
        print("no new folders")

def check_queued():
    """ sends request to the backend to ask if there are queued jobs"""
    backend_url = config["HOST"]["URL"]
    result = requests.get(backend_url + "/queued",json={"name":config["SELF"]["NAME"]})
    if result.status_code==200:
        data = result.json()
        if "jobs" in data:
            # starts first queued job
            if "action" in data.keys() and data["action"]=="delete":
                # delete queued job
                scheduler.add_job(localWorker.remove_job, trigger="date", args=[data['job_name']])
            else:
                print("There are queued jobs")
                # start queued job
                scheduler.add_job(localWorker.start_job, trigger="date", args=[data['jobs'][0]])
        else:
            print("No jobs to start")
    else:
        print("Error: {}".format(result.status_code))

def check_delete_queue():
    """ sends request to the backend to ask if there are queued jobs for deletion"""
    backend_url = config["HOST"]["URL"]
    result = requests.get(backend_url + "/delete_queue")
    if result.status_code==200:
        print("There are queued jobs")
        data = result.json()
        if "jobs" in data:
            # starts first queued job
            scheduler.add_job(localWorker.delete_job, trigger="date", args=[data['jobs'][0]])
        else:
            print("No jobs to start")
    else:
        print("Error: {}".format(result.status_code))
