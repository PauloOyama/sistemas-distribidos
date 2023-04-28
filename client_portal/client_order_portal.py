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
    cont = 0
    while True:
        aux2 = dict()

        if cont == 0 :
            opt = input('Quer fazer um pedido (y/N): ')
        if cont > 0:             
            opt = input('Precisa de algo a mais? (y/N): ')

        if opt == 'N':
            break
        else:        
            pid = input('Product ID: ')
            aux2['PID'] = pid
            quantities = input('Quantities: ')
            aux2['quantity'] = quantities

        aux.append(aux2)
        cont+=1
    
    order['data'] = aux

    with grpc.insecure_channel('localhost:'+port) as channel:

        stub = base_pb2_grpc.OrderPortalStub(channel)
        response = stub.CreateOrder(base_pb2.Order(OID=oid,CID=cid,data=str(aux)))
        print("Response -> " + response.description)

def RetrieveOrder(port='50051'):

    oid = input('Order ID: ')
    cid = input('Client ID: ')

    id = oid + ":" + cid

    with grpc.insecure_channel('localhost:'+ port) as channel:

        stub = base_pb2_grpc.OrderPortalStub(channel)
        response  = stub.RetrieveOrder(base_pb2.ID(ID=id))
        print("Response -> " + ' OID: '+ response.OID + " CID: "+response.CID +" Data: "+ response.data )


def UpdateOrder(port='50051'):
    order = dict()
    
    oid = input('Order ID: ')
    cid = input('Client ID: ')

    aux = []
    cont = 0
    while True:
        aux2 = dict()

        if cont == 0 :
            opt = input('Quer fazer um pedido (y/N): ')
        if cont > 0:             
            opt = input('Precisa de algo a mais? (y/N): ')

        if opt == 'N':
            break
        else:        
            pid = input('Product ID: ')
            aux2['PID'] = pid
            quantities = input('Quantities: ')
            aux2['quantity'] = quantities

        aux.append(aux2)
        cont+=1
    
    order['data'] = aux

    with grpc.insecure_channel('localhost:'+port) as channel:

        stub = base_pb2_grpc.OrderPortalStub(channel)
        response = stub.UpdateOrder(base_pb2.Order(OID=oid,CID=cid,data=str(aux)))
        print("Response -> " + response.description)


def DeleteOrder(port= '50051'):

    oid = input('Order ID: ')
    cid = input('Client ID: ')

    id = oid + ":" + cid

    with grpc.insecure_channel('localhost:'+ port) as channel:

        stub = base_pb2_grpc.OrderPortalStub(channel)
        response  = stub.DeleteOrder(base_pb2.ID(ID=id))
        print("Response -> " + response.description)


def retrieveClientOrders(port='50051'):


    cid = input('Client ID: ')

    with grpc.insecure_channel('localhost:'+ port) as channel:

        stub = base_pb2_grpc.OrderPortalStub(channel)
        print()
        print("Responses - - - ->  "+ cid)
        lst_response = stub.RetrieveClientOrders(base_pb2.ID(ID=cid))
        for response in lst_response:
            print( "Cliente = "+ response.CID +  ' OID: '+response.OID +" Data: "+ response.data )



def options() -> None:
    print('#----------------------------#')
    print('1 - Create Order')
    print('2 - Enum Order')
    print('3 - Modifier Order')
    print('4 - Cancel Order')
    print('5 - Enum all Orders')
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
                RetrieveOrder(port)
            case 3:
                UpdateOrder(port)
            case 4:
                DeleteOrder(port)
            case 5:
                retrieveClientOrders(port)  



if __name__ == '__main__':
    logging.basicConfig()
    run(sys.argv[1:][0] if len(sys.argv[1:]) > 0 else '50051')