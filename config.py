import configparser
import logging
import os
import json

logger = logging.getLogger("root")


class WorkerConfiguration:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.read_from_config_file()

    def read_from_config_file(self):
        if not os.path.exists(".config/api.conf"):
            if not os.path.exists(".config"):
                os.mkdir(".config")

            self.config.add_section("SELF")
            self.config.add_section("HOST")
            self.config.add_section("MongoDB")

            if self.read_env_vars():
                logger.critical("no environmental variables found")
                config_file = open(".config/api.conf", "w")
                self.config.write(config_file)
                config_file.close()
                logger.critical("missing data/env vars, please add to .config/api.conf")
        else:
            logger.info("configuration found")
            self.config.read(".config/api.conf")

    def read_env_vars(self):
        # jwt_secret = os.environ.get("JWTSECRET"
        backend_url = os.environ.get("BACKENDURL")
        worker_url = os.environ.get("SELFURL")
        name = os.environ.get("SELFNAME")
        user = os.environ.get("MONGOUSER")
        password = os.environ.get("MONGOPASS")

        self.config.set("MongoDB", "user", "YOURUSERHERE")
        if user:
            self.config.set("MongoDB", "user", user)

        self.config.set("MongoDB", "password", "YOURPASSWORDHERE")
        if password:
            self.config.set("MongoDB", "password", password)

        return None in [backend_url, worker_url,user,password]

    def get_configuration(self):
        return self.config
