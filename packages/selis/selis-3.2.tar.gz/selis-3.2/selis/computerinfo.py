import requests
import platform

from bs4 import BeautifulSoup


class ComputerInfo:
    def __init__(self):
        self.url = "https://www.iplocation.net/find-ip-address"


    def get_ip_public(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        ip = soup.find("span", style="font-weight: bold; color:green;").get_text()
        return ip


    def get_system_info(self):
        return platform.machine() + "/" + platform.node() + "/" + platform.platform() + "/" + platform.processor() + "/" + \
            platform.release() + "/" + platform.system() + "/" + platform.version()


    def get(self):
        ip = self.get_ip_public()
        os_info = self.get_system_info()

        return ip + "/" + os_info
    