from concurrent import futures
import json
import logging
import grpc
import sys
from common import error
from base import base_pb2_grpc,base_pb2
import random
import socket as sk

# [clients] take the CID as value and the data as value
clients = {}
# [products] take the PID as value and the data as value
products = {}


def selectReplica():
    
    socket1 = None 
    socket2 = None
    
    num = random.randint(1,3)
    
    try:
        host = sk.gethostname()
        socket1 = sk.socket()
        socket1.settimeout(1)
        socket2 = sk.socket()
        socket2.settimeout(1)
        print(num)
        if num == 1: 
            socket1.connect((host,30020))
            socket2.connect((host,30021))
            print("Sockets Connected: 30020, 30021")
        elif num == 2: 
            socket1.connect((host,30022))
            socket2.connect((host,30023))
            print("Sockets Connected: 30022, 30023")
        elif num == 3: 
            socket1.connect((host,30024))
            socket2.connect((host,30025))
            print("Sockets Connected: 30024, 30025")
    
    except:
        print("Error in Connection")
        sys.exit()
        
    return socket1,socket2


global sck1 
global sck2 
sck1 , sck2 = selectReplica()

class AdminPortalServicer(base_pb2_grpc.AdminPortal):

    ###### --------------------------------------------------------------- ###### 
    ######                      Client Functions                           ######
    ###### --------------------------------------------------------------- ######
        


    def CreateClient(self,request,target):
        """
            createClient() takes and CID [request.CID], and the data of the client [request.data],
            and add in the dictionary, if exists return error 2 and description, if not return error 0 
        """
        
        socket = None
        
        if int(request.CID) %2 == 0 :
            socket = sck1
        else: 
            socket = sck2

        if request.CID not in clients:
            
            # SENAO ACHOU NA LISTA DE CLIENTES PROCURA NO BANCOS
            msg = json.dumps({"function":"insert", "key": 'C-' +request.CID, "value": request.data})
            
            socket.send(msg.encode())
            resp = socket.recv(16480)
            
            print(resp.decode())
            
            clients[request.CID] = request.data

            print('Created Client')
            print(clients)
            return base_pb2.Reply(description=error.Error.noError, error=0)
        else: 
            print('Already in DataBase')
            return base_pb2.Reply(description=error.Error.clientExist, error=2)
            


    def RetrieveClient(self,request,target):
        """
            retrieveClient() takes and CID [request.ID], and check in the dictionary if the CID exist in the keys,
            if not return CID 0 and empty data (standard error), if it's return client
        """
        socket = None
        
        if int(request.ID) %2 == 0 :
            socket = sck1
        else: 
            socket = sck2
            
        msg = json.dumps({'function':'read', 'key': 'C-' + str(request.ID), 'value': None})
        
        socket.send(msg.encode())
        resp = socket.recv(16480)
        print(resp.decode())
        aux=json.loads(resp.decode())
            
        if aux["data"] == None:
            print('Client Doesn\'t Exist - Retrieve')
            return base_pb2.Client(CID='0', data='{}')
        else:
            print(type(aux['data']))
            clients[request.ID] = aux["data"]
            return base_pb2.Client(CID=request.ID,data=json.dumps(aux["data"]))
       
        

    def UpdateClient(self,request,target):
        """
            updateClient() takes and CID [request.CID], and the data of the client [request.data],
            and check in the dictionary if CID exists in it, if it exists, update data and return error 0, 
            if it not return error 2 and description. 
        """
        
        if int(request.CID) %2 == 0 :
            socket = sck1
        else: 
            socket = sck2
        
        msg = json.dumps({'function':'read', 'key': 'C-' + str(request.CID), 'value': None})
        
        socket.send(msg.encode())
        resp = socket.recv(16480)
        print(resp.decode())
        aux=json.loads(resp.decode())
            
        if aux["data"] == None:
            print('Client Doens\'t Exist - Update')
            return base_pb2.Reply(description=error.Error.clientNotExist, error=2)
        
        msg = json.dumps({'function':'update', 'key': 'C-' +str(request.CID), 'value': request.data})
        socket.send(msg.encode())
        resp = socket.recv(16480)
        clients[request.CID] = request.data
        print("Updated CID")        
        return base_pb2.Reply(description=error.Error.noError, error=0)
        

    def DeleteClient(self,request,target):
        """
            deleteClient() takes and CID [request.ID], and check in the dictionary if the CID exist in the keys,
            if it not, return error 2 and description, if it's return error 0 
        """

        if int(request.ID) %2 == 0 :
            socket = sck1
        else: 
            socket = sck2
        
        msg = json.dumps({'function':'read', 'key': 'C-' + str(request.ID), 'value': None})
        
        socket.send(msg.encode())
        resp = socket.recv(16480)
        print(resp.decode())
        aux=json.loads(resp.decode())
            
        if aux["data"] == None:
            print('Client Doesn\'t Exist')
            return base_pb2.Reply(description=error.Error.clientNotExist, error=2)
        
        del clients[request.ID]
        msg = json.dumps({'function':'delete', 'key': 'C-' + str(request.ID), 'value': None})
        socket.send(msg.encode())
        resp = socket.recv(16480)
        
        return base_pb2.Reply(description=error.Error.noError, error=0)

    ###### --------------------------------------------------------------- ###### 
    ######                      Product Functions                          ######
    ###### --------------------------------------------------------------- ######
 
    def CreateProduct(self,request,target):
        """
            createProduct() takes and PID [request.PID], and the data of the product [request.data],
            and add in the dictionary, if exists return error 2 and description, if not return error 0 
        """
        socket = None
        
        if int(request.PID) %2 == 0 :
            socket = sck1
        else: 
            socket = sck2

        if request.PID not in products:
            
            # SENAO ACHOU NA LISTA DE CLIENTES PROCURA NO BANCOS
            msg = json.dumps({"function":"insert", "key": 'P-' + request.PID, "value": request.data})
            
            socket.send(msg.encode())
            resp = socket.recv(16480)
            
            print(resp.decode())
            
            products[request.PID] = request.data

            print('Created Product')
            print(products)
            return base_pb2.Reply(description=error.Error.noError, error=0)
        else: 
            print('Already in DataBase')
            return base_pb2.Reply(description=error.Error.orderExist, error=2)


    def RetrieveProduct(self,request,target):
        """
            retrieveProduct() takes a PID [request.ID], and check in the dictionary if the PID exist in the keys,
            if not return PID 0 and empty data (standard error), if it's return product
        """
        socket = None
        
        if int(request.ID) %2 == 0 :
            socket = sck1
        else: 
            socket = sck2

        msg = json.dumps({'function':'read', 'key': 'P-' + str(request.ID), 'value': None})
        
        socket.send(msg.encode())
        resp = socket.recv(16480)
        print(resp.decode())
        aux=json.loads(resp.decode())

        if aux["data"] == None:
            
            print('Product Doesn\'t Exist - Retrieve')
            return base_pb2.Product(PID='0', data='{}')
        else:
            print(aux['data'])
            products[request.ID] = aux["data"]
            return base_pb2.Product(PID=request.ID,data=json.dumps(aux["data"]))


    def UpdateProduct(self,request,target):
        """
            updateProduct() takes and PID [request.CID], and the data of the product [request.data],
            and check in the dictionary if PID exists in it, if it exists, update data and return error 0, 
            if it not return error 2 and description. 
        """
        if int(request.PID) %2 == 0 :
            socket = sck1
        else: 
            socket = sck2
        
        msg = json.dumps({'function':'read', 'key': 'P-' +str(request.PID), 'value': None})
        
        socket.send(msg.encode())
        resp = socket.recv(16480)
        aux=json.loads(resp.decode())
        print(resp.decode())
            
        if aux['data'] == None:
            print('Product Doens\'t Exist - Update')
            return base_pb2.Reply(description=error.Error.orderNotExist, error=2)

        msg = json.dumps({'function':'update', 'key': 'P-' +str(request.PID), 'value': request.data})
        socket.send(msg.encode())
        resp = socket.recv(16480)
        products[request.PID] = request.data
        print("Updated PID")        
        return base_pb2.Reply(description=error.Error.noError, error=0)

    def DeleteProduct(self,request,target):
        """
            deleteProduct() takes and PID [request.ID], and check in the dictionary if the PID exist in the keys,
            if it not, return error 2 and description, if it's return error 0 
        """
        if int(request.ID) %2 == 0 :
            socket = sck1
        else: 
            socket = sck2
        

        msg = json.dumps({'function':'read', 'key': 'P-' + str(request.ID), 'value': None})
        
        socket.send(msg.encode())
        resp = socket.recv(16480)
        aux=json.loads(resp.decode())
        print(resp.decode())
            
            #Not in BD
        if aux['data'] == None:
            print('Product Doesn\'t Exist')
            return base_pb2.Reply(description=error.Error.orderNotExist, error=2)
            

        print(products)
        del products[request.ID]        
        msg = json.dumps({'function':'delete', 'key': 'P-' + str(request.ID), 'value': None})
        socket.send(msg.encode())
        resp = socket.recv(16480)
        
        return base_pb2.Reply(description=error.Error.noError, error=0)

def serve(port = '50055'):

    #Set connection gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    base_pb2_grpc.add_AdminPortalServicer_to_server(AdminPortalServicer(), server)
    server.add_insecure_port('[::]:' + port )
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':

    # The server and client in portal will run on port 50055 by default

    try:
        logging.basicConfig()



        serve(sys.argv[1:][0] if len(sys.argv[1:]) > 0 else '50055')
        
        # client.loop_forever()

    except:
        print("Disconnecting...")