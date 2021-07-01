import os

class LocalWorker:
    
    def __init__(self):
        super().__init__()\

    def valid_folder(self,folder_name):
        folder_path = "./image_folders/" + folder_name
        empty = os.path.isdir(folder_path)
        if len(os.listdir(folder_path)):
            return True
        return False
    
    def get_image_folders(self,alt_path = ""):
        if not len(alt_path):
            folders = list(filter(self.valid_folder, os.listdir("./image_folders")))
            folder_dic = {}
            for folder in folders:
                files = os.listdir("./image_folders/"+folder)
                folder_dic[folder] = files
            return folder_dic

        else:
            try:
                folders = os.listdir(alt_path)
            except:
                return {"message": "error no folders found"}
        return folders

    

worker = LocalWorker()
print(worker.get_image_folders())
