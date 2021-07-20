from dtypes.Frame import Frame
from os import mkdir, listdir, makedirs
import sqlite3
import uuid
from utils.sql_utils import adapt_array, convert_array
from numpy import ndarray, array
from shutil import rmtree
from utils.export_diams import write_diam


class Job:
    def __init__(self, options,client=None):
        print("job init:", options)
        if "folders" in options.keys():
            options['frame_paths'] = []
            for folder in options["folders"]:
                options["frame_paths"].append("./image_folders/" +folder)
                print("FRAME PATHS: ", options["frame_paths"])
        self.job_name = options["job_name"]
        if "job_id" in options.keys():
            self.job_id = options["job_id"]
        else:
            self.job_id = self.job_name + "_" + str(uuid.uuid4()).replace("-", "")
        self.options = options
        self.options['largest_pore']=0
        self.options['num_pores']=0
        self.options['avg_porosity']=0
        self.frame_ls = []
        self.frame_ref_ls = []
        self.try_make_dir()
        self.frame_paths = options["frame_paths"]
        self.create_frames(options, options["frame_paths"])
        self.update_ref_ls()
        self.post_job_data(client)

    def get_dic(self):
        self.options["frame_ls"] = self.frame_ls
        self.options['num_images'] = sum([f['num_images'] for f in self.frame_ls])
        self.options['avg_pore'] = sum([f['avg_pore'] for f in self.frame_ls]) / len(self.frame_ls)
        self.options['img_review'] = [image for frame in self.frame_ls for image in frame['image_data']]
        return self.options
        return self.options

    def try_make_dir(self):
        """will attempt to create directory for job outputs
        if folder already exists will empty folder"""
        try:
            mkdir("./job-data/" + self.job_name)
        except Exception as e:
            print("exception:", e)
            print("emptying dir... dir empty")
            rmtree("./job-data/" + self.job_name)
            makedirs("./job-data/" + self.job_name)

    def update_ref_ls(self):
        for frame in self.frame_ls:
            self.frame_ref_ls.append(frame['frame_id'])

        print("job frame ref ls updated")

    def post_job_data(self,client):
        "insert finished job into db"
        print("posting job data",self.get_dic())
        print("frames:")
        temp_ls = self.frame_ls
        for f in temp_ls:
            print("FRAMEKEYs:",f.keys())
            for img in f["image_data"]:
                del img['violated_circles']
        client.micronProDB.jobs.insert_one(self.get_dic())

    def create_frames(self, options, frame_paths):

        for fpath in frame_paths:
            f = Frame(
                fpath,
                options,
            )
            self.frame_ls.append(f.get_dic())
            for image in f['image_data']:
                if image['largest_pore'] > self.options['largest_pore']:
                    self.options['largest_pore'] = image['largest_pore']
        self.options["status"]= "Complete"
        
