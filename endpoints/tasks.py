import requests
from os import environ
from backend_vars import configFile

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
