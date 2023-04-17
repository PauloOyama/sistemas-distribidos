from __future__ import print_function

import logging
import sys
import grpc
import time
from base import base_pb2
from base import base_pb2_grpc

def createClient(port ='50051'):
    

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('CID: ')
            aux['CID'] = cid
            name  = input('Nome do Clinte: ')
            aux['name'] = name

            response = stub.CreateClient(base_pb2.Client(CID=cid,data=str(aux)))

            if int(response.error) == 0:
                 print('Sucesso')
            else:
                 print('Error: ' + response.description)
        
      
def retrieveClient(port ='50051'):

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('CID: ')

            response = stub.RetrieveClient(base_pb2.ID(ID=cid))

            print('Client ID: ' + response.CID)
            print('Client Data: '+ response.data)


     
def options() -> None:
    print('#----------------------------#')
    print('1 - Create Client')
    print('2 - Retrieve Client')
    print('3 - Update Client')
    print('4 - Delete Client')
    print('5 - Create Product')
    print('6 - Retrieve Product')
    print('7 - Update Product')
    print('8 - Delete Product')
    print('#----------------------------#')

def run(port = '50051'):
    
    while True:
        time.sleep(2)
        options()
        inp = int(input('Choose one option:'))

        match inp:
            case 1:
                  createClient(port)
            case 2:
                  retrieveClient(port)
                  pass
            case 3:
                  pass
            case 4:
                  pass
            case 5:
                  pass
            case 6:
                  pass
            case 7:
                  pass
            case 8:
                  pass
        




if __name__ == '__main__':
    logging.basicConfig()
    
    run(sys.argv[1:] if len(sys.argv[1:]) > 0 else '50051')