import socket
import threading
import sys
import webbrowser
import getpass

from selis.computerinfo import ComputerInfo
from selis.utils import convert_color


class ChatClient:
    def __init__(self, ip, port, nickname):
        self.nickname = nickname
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.connection.connect((ip, port))
        except:
            print(f"[-] Sever not found")
            sys.exit()

        self.send_client_info_to_sever()
        self.is_running = True


    def send_client_info_to_sever(self):
        client_computer = ComputerInfo()
        computer_info = client_computer.get()
        msg = self.nickname + "/" + computer_info
        self.send_message(msg)


    def send_message(self, message):
        self.connection.send(message.encode())


    def exit_room(self):
        self.connection.close()
        self.is_running = False


    def open_url(self, url):
        webbrowser.open(url)


    def out_sever(self):
        self.send_message(f"/exit {self.nickname}")
        self.exit_room()
        self.guide_to_exit()

    
    def guide_to_exit(self):
        print(convert_color("[+] Press 'Ctrl + C' or 'Enter' to exit", style="ENDC"))


    def recieve_message(self):
        while self.is_running:
            try:
                response = self.connection.recv(1024).decode()

                if not response and self.connection:
                    print(convert_color("[-] Sever is not opening", style="FAIL"))
                    self.guide_to_exit()
                    break

                elif "admin/open-url" in response:
                    url = response.split(" ")[1]
                    self.open_url(url)

                elif response == "admin/close-server":
                    print(convert_color("[-] Admin closes the server", style="FAIL"))
                    self.out_sever()

                else:
                    print(response)
            except:
                try:
                    print(convert_color("[-] Connection is closed", style="FAIL"))
                    self.connection.close()
                    break
                except:
                    sys.exit()
    

    def process_admin_mode(self):
        password = getpass.getpass(convert_color("[*] Admin's Password: \n>> ", style="ENDC"))
        msg = "check-admin/" + password
        self.send_message(msg)


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

                elif content == "/admin-mode":
                    self.process_admin_mode()

                elif content == "/close-server":
                    self.send_message(content)
                
                elif content == "/close":
                    self.send_message(content)

                elif content == "/open":
                    self.send_message(content)

                elif "/kick" in content:
                    self.send_message(content)

                elif "/ban" in content:
                    self.send_message(content)

                elif "/un-ban" in content:
                    self.send_message(content)

                elif "/open-url" in content:
                    self.send_message(content)

                elif "/msg" in content:
                    self.send_message(content)

                else:
                    content = convert_color(f"({self.nickname}): {content}", style="ENDC")
                    self.send_message(content)
        except:
            sys.exit()


    def start(self):
        recieve_threading = threading.Thread(target=self.recieve_message)
        recieve_threading.start()
        
        send_threading = threading.Thread(target=self.process_sending_message)
        send_threading.start()

        recieve_threading.join()
        send_threading.join()
