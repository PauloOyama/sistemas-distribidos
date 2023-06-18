from __future__ import print_function
from lvldb import Database

import sys
import socket
import threading
import json
            
def controller(replica, conn, addr):
  while True:
    data = conn.recv(4120)
    msg = data.decode()

    if msg:
      responseMsg = json.loads(msg)
      functionName = responseMsg['function']
      key = responseMsg['key']
      value = responseMsg['value']
        
        
    if functionName == 'read':
      response = replica.getData(key)
      if response:
        response = str(response).replace('\'','"')
        response = json.loads(response)
      resp = json.dumps({'data': response})


    if functionName == 'insert':
      replica.insertData(key, value)
      resp = json.dumps({'message': "OK"})


    if functionName == 'update':
      replica.updateData(key, value)
      resp = json.dumps({'message': "OK"})


    if functionName == 'delete':
      replica.deleteData(key)
      resp = json.dumps({'message': "OK"})

    conn.send(resp.encode())

def run(arg):
  
  # Partição 1
  if arg == 1:
    socketPort = 30020
    replica = Database(socketPort, 'pair', 'localhost:39400',['localhost:39402', 'localhost:39404'])
  if arg == 2:
    socketPort = 30022
    replica = Database(socketPort, 'pair', 'localhost:39402',['localhost:39400', 'localhost:39404'])
  if arg == 3:
    socketPort = 30024
    replica = Database(socketPort, 'pair', 'localhost:39404',['localhost:39400', 'localhost:39402'])
  
  # Partição 2
  if arg == 4:
    socketPort = 30021
    replica = Database(socketPort, 'odd', 'localhost:39401',['localhost:39403', 'localhost:39405'])
  if arg == 5:
    socketPort = 30023
    replica = Database(socketPort, 'odd', 'localhost:39403',['localhost:39401', 'localhost:39405'])
  if arg == 6:
    socketPort = 30025
    replica = Database(socketPort, 'odd', 'localhost:39405',['localhost:39401', 'localhost:39403'])

  s = socket.socket()
  host = socket.gethostname()
  s.bind((host, socketPort))
  s.listen(30)
  while True:
    conn, addr = s.accept()
    threading.Thread(target=controller, args=(replica, conn, addr)).start()

if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.exit(-1)

  arg = int(sys.argv[1])

  if arg not in [1, 2, 3, 4, 5, 6]:
    print("Choose one from 1 to 6")
    sys.exit(-1)
    
  run(arg)
