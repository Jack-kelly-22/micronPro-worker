import time
from dtypes.simpleImage import SimpleImage
from os import mkdir
from utils.sql_utils import adapt_array, convert_array
from numpy import ndarray, array
from utils.data_utils import *
import uuid
import os
import shutil
from matplotlib import pyplot as plt
from numpy import std
from math import pi


class Frame:
    def get_images_in_path(self, path):
        imgs = os.listdir(path)
        imgs_paths = []
        for img in imgs:
            if img[0] != ".":
                imgs_paths.append(path + "/" + img)
        return imgs_paths

    def __init__(self, path, options,client=None):
        """
        name: what to call the frame
        image_ls: list of images paths
        inspect_mode: light/dark
        """
        self.name = os.path.basename(os.path.normpath(path))
        self.options = options
        self.job_name = options["job_name"]
        self.image_paths = self.get_images_in_path(path)
        self.id = str(uuid.uuid4()).replace("-", "") + "_" + self.name
        self.constants = options["constants"]
        self.image_data_ls = []
        self.image_ref_ls = []
        self.avg_pore = 0
        self.all_areas = []
        self.histogram = []
        self.hist_bins = []
        self.client = client
        self.largest_holes = []
        self.largest_areas = []
        self.failed_images = 0
        (
            self.area_hist_path,
            self.diam_hist_path,
            self.area_pie_path,
            self.pore_pie_path,
        ) = ("", "", "", "")
        self.area_std, self.diam_std = 0, 0
        self.create_dir()
        self.process_frame()

    def get_dic(self):
        """returns a dictionary of all the data of frame"""
        return {
            "frame_name": self.name,
            "frame_id": self.id,
            "avg_pore":self.avg_pore,
            "largest_holes":self.largest_holes,
            "failed_images":self.failed_images,
            "failed_image_data":[image_data for image_data in self.image_data_ls if not image_data["pass"]],
            "image_data": self.image_data_ls,
            "num_images": len(self.image_data_ls),

        }


    def create_dir(self):
        try:
            mkdir("./job-data/" + self.job_name + "/" + self.name)
        except Exception as e:
            shutil.rmtree("./job-data/" + self.job_name + "/" + self.name)
            os.makedirs("./job-data/" + self.job_name + "/" + self.name)

    def process_frame(self):
        """creates instances ImageData objects for all
        images and adds them so self.image_data_ls
        """
        i = 0
        for img in self.image_paths:
            img_dic = {
                "img_path": img,
                "id": "",
                "pass": False,
                "img_name": "",
                "fail_reason": [],
                "largest_pore": 0,
                "porosity": 0,
                "avg_pore": 0,
                "out_path": "./job-data/" + self.options["out_path"],
                "num_violated": 0,
                "violated_pores": [],
                
            }
            self.process_image(img_dic, self.options)
            i = i + 1
        self.histogram, self.hist_bins = get_histogram(
            self.all_areas, self.constants["scale"], self.constants["min_ignore"]
        )
        self.avg_pore = self.avg_pore / len(self.image_data_ls)

    def process_image(self, img_dic, options):
        """creates new ImageData objects and appends"""
        # print("starting image processing of file with path:", img)
        new_image = SimpleImage(img_dic, options)
            
        new_image_dic = new_image.get_dic()
        if self.client is not None:
            self.client.micronProDB.jobs.update_one({'job_id':options['job_id']},{"$inc":{'progress':1}})
        self.image_data_ls.append(new_image_dic)
        self.image_ref_ls.append(new_image_dic["id"])
        if not options["simple"]:
            # self.all_areas = self.all_areas + new_image_dic["all_areas"]
            self.largest_holes = self.largest_holes + new_image_dic["largest_holes"]
            self.largest_areas = self.largest_areas + new_image_dic["largest_areas"]
        self.avg_pore = self.avg_pore + new_image_dic["porosity"]
        if not new_image_dic['pass']:
            self.failed_images+=1
            
        # print("finished image processing of file with path:", img)

    def save_histogram_hole_diameter(self):
        # print(self.largest_holes)
        largest_diams = [
            x[1] * 2 * float(self.constants["scale"]) for x in self.largest_holes
        ]
        self.diam_std = std(largest_diams)
        print("STD diam:", self.diam_std)
        plt.hist(largest_diams, 10)
        plt.xlabel("Diameter(microns)")
        plt.ylabel("Frequency")
        plt.title(
            "Histogram of Diameter of top "
            + str(len(largest_diams))
            + " Largest Circles"
        )
        plt.savefig(
            "./job-data/"
            + self.job_name
            + "/"
            + self.name
            + "/"
            + "diameter_histogram.png"
        )
        self.diam_hist_path = (
            "./job-data/"
            + self.job_name
            + "/"
            + self.name
            + "/"
            + "diameter_histogram.png"
        )

    def save_histogram_hole_area(self):
        plt.clf()
        largest_areas = [
            (x[1] ** 2) * pi * (float(self.constants["scale"]) ** 2)
            for x in self.largest_holes
        ]
        plt.hist(largest_areas, bins=20)
        self.area_std = std(largest_areas)
        print("STD area:", self.area_std)
        plt.xlabel("Area(microns^2)")
        plt.ylabel("Frequency")
        plt.title(
            "Histogram of Area of Top " + str(len(largest_areas)) + " Largest Circles"
        )
        plt.savefig(
            "./job-data/" + self.job_name + "/" + self.name + "/" + "area_histogram.png"
        )
        self.area_hist_path = (
            "./job-data/" + self.job_name + "/" + self.name + "/" + "area_histogram.png"
        )

    def compute_fractions(self):
        lables = [image.name for image in self.image_data_ls]
        area_totals = [0] * len(self.image_data_ls)
        area_totals = {image.name: 0 for image in self.image_data_ls}
        area_sum = 0
        for area in self.largest_holes:
            area_totals[area[2]] = area_totals[area[2]] + area[1]
            area_sum = area[1]
        for k, v in area_totals.items():
            area_totals[k] = v / area_sum
        print("THIS is AREA TOTALS", area_totals)
        return area_totals
