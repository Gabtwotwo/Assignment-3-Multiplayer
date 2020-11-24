import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import requests


def getInfo(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        print(str(data))


def main():
    addr = "18.191.58.55"
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((addr, port))
    start_new_thread(getInfo, (s,))
    getPlayersURL = "https://m6y6f01lb2.execute-api.us-east-2.amazonaws.com/default/getPlayerInfo"

    numGames = int(input("How Many Games? : "))

    Players = requests.get(getPlayersURL)
    playersBody = json.loads(Players.content)


    serverInfo = {"players": playersBody['Items']}


    s.send(bytes(json.dumps({'numGames': numGames}), "utf-8"))
    s.send(bytes(json.dumps(serverInfo), "utf-8"))



    
    while True:
        time.sleep(0)

main()