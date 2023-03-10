import sys
import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    filename="app.log",
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def connection_log(host, port, headers):
    sys.stdout.write("\033[0;32m")
    print(" [x] Consumer running on host \"" + host + ":" + str(port) + "\" , "
          + "headers : " + str(headers), end="")
    sys.stdout.write("\033[1;36m")
    print(" -- Waiting for Requests ...")


def action_log(message, app_name):
    sys.stdout.write("\033[1;31m")
    print("\n => Entry action: ", end="")
    sys.stdout.write("\033[;1m\033[1;34m")
    logging.info(f"Entry action: {message.get(app_name).get('action')}")
    print(message.get(app_name).get("action"))


def request_log(message, app_name):
    sys.stdout.write("\033[1;31m")
    print("                  Request:  ", end="")
    sys.stdout.write("\033[;1m\033[1;34m")
    logging.info(f"Request: {message.get(app_name).get('body')}")
    print(message.get(app_name).get("body"))


def responce_log(message):
    sys.stdout.write("\033[1;31m")
    print("                  Responce: ", end="")
    sys.stdout.write("\033[;1m\033[1;34m")
    logging.info(f"Response: {message}")
    print(message)
