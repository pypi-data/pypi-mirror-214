import socket
import threading
import sys
import webbrowser
import random
import requests
import platform

from bs4 import BeautifulSoup


class Client:
    def __init__(self, ip, port, nickname, admin_mode):
        self.admin_mode = admin_mode
        self.nickname = nickname
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((ip, port))
        except:
            print(f"[-] Sever not found")
            sys.exit()
        self.send_info_user_to_sever()
        self.is_running = True


    def get_ip_public(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        ip = soup.find("span", style="font-weight: bold; color:green;").get_text()
        return ip


    def get_system_info(self):
        return platform.machine() + "/" + platform.node() + "/" + platform.platform() + "/" + platform.processor() + "/" + \
            platform.release() + "/" + platform.system() + "/" + platform.version()
    

    def send_info_user_to_sever(self):
        ip = self.get_ip_public("https://www.iplocation.net/find-ip-address")
        os_info = self.get_system_info()
        msg = self.nickname + "/" + ip + "/" + os_info
        self.send_message(msg)


    def send_message(self, message):
        try:
            self.connection.send(message.encode())
        except:
            exit()


    def exit_room(self):
        self.connection.close()
        self.is_running = False


    def open_url(self, url):
        webbrowser.open(url)


    def handle_admin_command(self, command):
        if self.admin_mode == True:
            self.send_message(command)
        else:
            print(self.convert_color("[-] Only admin can use this command", style="ENDC"))


    def convert_color(self, string, style):
        colors = {
        "WARNING": '\033[93m',
        "FAIL": '\033[91m',
        "ENDC": '\033[0m',
        "BOLD": '\033[1m'
        }
        return colors[style] + string


    def get_style_color(self):
        color_list = ["WARNING", "FAIL", "ENDC", "BOLD"]
        return random.choice(color_list)


    def out_sever(self):
        print(self.convert_color("[-] Admin closes the sever", style="FAIL"))
        content = f"/exit {self.nickname}"
        self.send_message(content)
        self.exit_room()
        print(self.convert_color("[+] Press 'Ctrl + C' or 'Enter' to exit", style="ENDC"))


    def recieve_message(self):
        while self.is_running:
            try:
                response = self.connection.recv(1024).decode()
                if not response and self.connection:
                    print(self.convert_color("[-] Sever is not available", style="FAIL"))
                    print(self.convert_color("[+] Press 'Ctrl + C' or 'Enter' to exit", style="ENDC"))
                    break
                elif "admin/open-url" in response and self.admin_mode is not True:
                    url = response.split(" ")[1]
                    self.open_url(url)
                elif response == "/close-sever":
                    self.out_sever()
                else:
                    print(response)
            except:
                try:
                    print(self.convert_color("[-] Connection is closed", style="FAIL"))
                    self.connection.close()
                    break
                except:
                    sys.exit()
    

    def process_sending_message(self):
        try:
            while self.is_running:
                content = input()
                if content == "/exit":
                    content = f"/exit {self.nickname}"
                    self.send_message(content)
                    self.exit_room()
                    break
                elif content == "/ls":
                    self.send_message(content)
                elif "/open-url" in content:
                    self.handle_admin_command(content)
                elif "/close-sever" == content:
                    self.handle_admin_command(content)

                else:
                    content = self.convert_color(f"({self.nickname}): {content}", style="ENDC")
                    self.send_message(content)
        except:
            sys.exit()


    def start(self):
        send_threading = threading.Thread(target=self.process_sending_message)
        send_threading.start()

        recieve_threading = threading.Thread(target=self.recieve_message)
        recieve_threading.start()

        send_threading.join()
        recieve_threading.join()
