import getpass
import sys

from optparse import OptionParser
from selis.client import Client


def return_arguments():
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", help="Connect to sever through this port")
    parser.add_option("-r", "--root", dest="root", help="Use root [on/off] to become the admin")
    parser.add_option("-n", "--nickname", dest="nickname", help="Choose your name or a nickname")
    (options, arguments) = parser.parse_args()
    return_error(parser, options)
    return options


def return_error(parser, options):
    if not options.port:
        parser.error("[-] Port not found")


def return_admin_mode():
    keypass = getpass.getpass("Admin's Password: ")
    if keypass == "selis.py":
        print("[+] You're now the admin")
        admin_mode = True
    else:
        print("\033[91m[-] Password is wrong!")
        admin_mode = False

    return admin_mode
    

def main():
    options = return_arguments()

    ip = "0.tcp.ap.ngrok.io"
    port = int(options.port)
    nickname = options.nickname

    if nickname:
        pass
    else:
        nickname = input("[+] Choose a name: ")

    if options.root == "on":
        admin_mode = return_admin_mode()
    else:
        admin_mode = False


    try:
        client = Client(ip=ip, port=port, nickname=nickname, admin_mode=admin_mode)
        client.start()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
