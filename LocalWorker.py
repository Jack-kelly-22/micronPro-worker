import os
from shutil import rmtree
from dtypes.Job import Job
from utils.SpreadWriter import SpreadWriter
from backend_vars import log,configFile
from pymongo import MongoClient


class LocalWorker:
    def __init__(self):
        self.host = "0.0.0.0.0"
        #read config file
        self.config = configFile.get_configuration()
        user,password = (self.config["MongoDB"]["user"],
            self.config["MongoDB"]["password"])
        self.client = MongoClient(
            "mongodb+srv://" + user +":" + password + "@maincluster.btvwv.mongodb.net"
        )
        print("CLIENT:",self.client.database_names())
        log.info("database responded")

    def valid_folder(self, folder_name):
        folder_path = "./image_folders/" + folder_name
        empty = os.path.isdir(folder_path)
        if len(os.listdir(folder_path)):
            return True
        return False

    def get_image_folders(self, alt_path=""):
        if not len(alt_path):
            folders = list(filter(self.valid_folder, os.listdir("./image_folders")))
            folder_dic = {}
            for folder in folders:
                files = os.listdir("./image_folders/" + folder)
                folder_dic[folder] = files
                print(folder_dic)
            return folder_dic

        else:
            try:
                folders = os.listdir(alt_path)
            except:
                return {"message": "error no folders found"}
        return folders

    def delete_image_folder(self, folder_name):
        if len(folder_name):
            folder_path = "./image_folders/" + folder_name
            try:
                rmtree(folder_path)
                print(folder_path + " deleted")
                return {"msg": "success"}
            except:
                return {"msg": "error deleting folder"}
        return {"message": "no folder given"}

    def start_job(self,job):
        print("SIMPLE QUEUE JOB")
        log.info("SIMPLE QUEUE JOB")
        job = Job(job,self.client)
        filter_dic = job.get_dic()
        print("FILTER DIC: " + str(filter_dic))

        SpreadWriter(filter_dic)
