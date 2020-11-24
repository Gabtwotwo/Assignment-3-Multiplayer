import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import requests

clients_lock = threading.Lock()


Players = []
def connectionLoop(sock):
   numGames = 0
   numLobby = 0
   numLoops = 0

   while True:
      data, addr = sock.recvfrom(1024)
      data = json.loads(data)
      print(str(data))
      setPlayerURL = "https://dxnj0ustr4.execute-api.us-east-2.amazonaws.com/default/setPlayerInfo" + "?ELODifference=" 
      if 'players' in data:

         for count in range(numGames):

            Game = {'GameID': count + 1, 'players': [], 'Winner': {}}


            
            for playerCount in range(3):
               print(playerCount + numLoops)
               if playerCount + numLoops >= len(data['players']):
                  numLoops = 0
               Game['players'].append(data['players'].__getitem__(playerCount + numLoops))
               
            
            
            Winner = random.choice(Game['players'])
            Game['Winner'] = Winner


            for player in Game['players']:
               if player is Winner:
                  player['ELO'] = str(int(player['ELO']) + 10)
                  requests.get(setPlayerURL + player['ELO'] + '&PlayerID=' + player['PlayerNames'])
                  Winner = player
               else:
                  player['ELO'] = str(int(player['ELO']) - 5)
                  requests.get(setPlayerURL + player['ELO'] + '&PlayerID=' + player['PlayerNames'])
            numLoops += 3
            sock.sendto(bytes(str(Game), "utf-8"), addr)

        

      else:
         numGames = data['numGames']

      


      



def main():
   port = 12345
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.bind(('', port))
   start_new_thread(connectionLoop, (s,))
   while True:
      time.sleep(1)


if __name__ == '__main__':
   main()