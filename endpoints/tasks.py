import requests
from uuid import uuid4
from os import environ
from backend_vars import configFile, scheduler, localWorker,num_folders

config = configFile.get_configuration()

def send_here():
    print("Saying hey to the webserver :)")
    self_url, self_name = config["SELF"]["URL"], config["SELF"]["NAME"]
    # password = config['SELF']['PASS']
    backend_url = config["HOST"]["URL"]
    requests.post(
        backend_url + "/hello", json={"self_url": self_url, "self_name": self_name}
    )
    print({"self_url": self_url, "self_name": self_name})

def post_folders():
    """sends folder data to the backend"""
    print("Sending folder data to backend")
    folders = localWorker.get_image_folders()
    backend_url = config["HOST"]["URL"]
    if num_folders!=len(folders)-1:
        requests.post(backend_url + "/post_folders",json={"folders":folders,"name":config["SELF"]["NAME"]})
    else:
        print("no new folders")

def check_queued():
    """ sends request to the backend to ask if there are queued jobs"""
    backend_url = config["HOST"]["URL"]
    result = requests.get(backend_url + "/queued")
    if result.status_code==200:
        print(result.json())
        data = result.json()
        if "jobs" in data:
            for job in data["jobs"]:
                job['job_id'] = job['job_name'] + "_" + str(uuid4()).replace("-", "")
                scheduler.add_job(localWorker.start_job, trigger="date", args=[job])
    else:
        print("Error: {}".format(result.status_code))

