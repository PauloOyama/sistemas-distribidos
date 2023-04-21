from __future__ import print_function
import time
import logging
import sys
import grpc
from base import base_pb2
from base import base_pb2_grpc

def createOrder(port='50051'):
    order = dict()
    
    oid = input('Order ID: ')
    cid = input('Client ID: ')


    aux = []
    while True:
        aux2 = dict()
        opt = input('Precisa de algo a mais? (y/N): ')

        if opt == 'N':
            break
        else:        
            pid = input('Product ID: ')
            aux2['PID'] = pid
            price = input('Price : ')
            aux2['price'] = price
            quantities = input('Quantities: ')
            aux2['quantity'] = quantities

        aux.append(aux2)

    
    order['data'] = aux

    print(order)

    with grpc.insecure_channel('localhost:50051') as channel:

        stub = base_pb2_grpc.OrderPortalStub(channel)
        response = stub.CreateOrder(base_pb2.Order(OID=oid,CID=cid,data=str(aux)))
        print("Response -> " + response.description)

def options() -> None:
    print('#----------------------------#')
    print('1 - Create Order')
    print('2 - Retrieve Order')
    print('3 - Update Order')
    print('4 - Delete Order')
    print('5 - Retrieve Client Orders')
    print('#----------------------------#')

def run(port = '50055'):
    
    while True:
        time.sleep(2)
        options()

        inp = int(input('Choose one option:'))

        match inp:
            case 1:
                  createOrder(port)
            case 2:
                  pass
                #   retrieveClient(port)
            case 3:
                  pass
                #   updateClient(port)
            case 4:
                  pass
                #   deleteClient(port)
            case 5:
                  pass
                #   createProduct(port)  



if __name__ == '__main__':
    logging.basicConfig()
    run(sys.argv[1:][0] if len(sys.argv[1:]) > 0 else '50051')