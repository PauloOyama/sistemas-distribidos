import logging
import sys
import grpc
import time
from base import base_pb2
from base import base_pb2_grpc
import paho.mqtt.client as mqtt

def createClient(port ='50055'):
    

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('CID: ')
            aux['CID'] = cid
            name  = input('Nome do Clinte: ')
            aux['name'] = name

            response = stub.CreateClient(base_pb2.Client(CID=cid,data=str(aux)))

            if int(response.error) == 0:
                 print('Success')
            else:
                 print('Error: ' + response.description)
        
      
def retrieveClient(port ='50055'):

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('CID: ')

            response = stub.RetrieveClient(base_pb2.ID(ID=cid))

            print('Client ID: ' + response.CID)
            print('Client Data: '+ response.data)

def updateClient(port ='50055'):
    

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('CID: ')
            aux['CID'] = cid
            name  = input('New Client Name: ')
            aux['name'] = name

            response = stub.UpdateClient(base_pb2.Client(CID=cid,data=str(aux)))

            if int(response.error) == 0:
                 print('Success')
            else:
                 print('Error: ' + response.description)
        
      
def deleteClient(port ='50055'):

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('CID: ')

            response = stub.DeleteClient(base_pb2.ID(ID=cid))

            if int(response.error) == 0:
                 print('Success')
            else:
                 print('Error: ' + response.description)


def createProduct(port ='50055'):
    

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('PID: ')
            aux['PID'] = cid
            name  = input('Name Product: ')
            aux['name'] = name
            name  = input('Quantity : ')
            aux['quantity'] = name

            response = stub.CreateProduct(base_pb2.Product(PID=cid,data=str(aux)))

            if int(response.error) == 0:
                 print('Success')
            else:
                 print('Error: ' + response.description)
        
      
def retrieveProduct(port ='50055'):

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('PID: ')

            response = stub.RetrieveProduct(base_pb2.ID(ID=cid))

            print('Client ID: ' + response.PID)
            print('Client Data: '+ response.data)


def updateProduct(port ='50055'):
    

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('PID: ')
            aux['PID'] = cid
            name  = input('Name Product: ')
            aux['name'] = name
            name  = input('Quantity : ')
            aux['quantity'] = name

            response = stub.UpdateProduct(base_pb2.Product(PID=cid,data=str(aux)))

            if int(response.error) == 0:
                 print('Success')
            else:
                 print('Error: ' + response.description)
        
      
def deleteProduct(port ='50055'):

        with grpc.insecure_channel('localhost:'+ port) as channel:
            aux = {}
            stub = base_pb2_grpc.AdminPortalStub(channel)
            
            cid = input('PID: ')

            response = stub.DeleteProduct(base_pb2.ID(ID=cid))

            if int(response.error) == 0:
                 print('Success')
            else:
                 print('Error: ' + response.description)

     
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

def run(port = '50055'):
    
    while True:
        time.sleep(2)
        options()
        inp = int(input('Choose one option:'))

        match inp:
            case 1:
                  createClient(port)
            case 2:
                  retrieveClient(port)
            case 3:
                  updateClient(port)
            case 4:
                  deleteClient(port)
            case 5:
                  createProduct(port)  
            case 6:
                  retrieveProduct(port)
            case 7:
                  updateProduct(port)
            case 8:
                  deleteProduct(port)
        




if __name__ == '__main__':
    logging.basicConfig()
    
    run(sys.argv[1:][0] if len(sys.argv[1:]) > 0 else '50055')