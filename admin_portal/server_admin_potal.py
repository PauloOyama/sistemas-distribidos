from concurrent import futures
import logging
import grpc
import sys
import paho.mqtt.client as mqtt
from common import error
from base import base_pb2_grpc,base_pb2


subscribers = [('clients',0), ('products',0)]
clients = {}
products = {}


def on_message(client, userdata, msg):

    print(msg.topic+" "+str(msg.payload.decode()))
    rps = str(msg.payload.decode()).split(' ')

    if msg.topic == 'clients':

        if rps[0] == 'DELETE':
            rqt = rps[1]
            data = clients[rqt] 
            del clients[rps[1]]
            print(rqt,data)

        elif rps[0] == 'UPDATE':
            clients[rps[1]] = ''.join(rps[2:])

        elif rps[0] == 'CREATE':
            clients[rps[1]] = ''.join(rps[2:])

        else:
            print('NOT FOUND')

    elif msg.topic == 'products':

        if rps[0] == 'DELETE':
            rqt = rps[1]
            data = products[rqt] 
            del products[rps[1]]
            print(rqt,data)

        elif rps[0] == 'UPDATE':
            products[rps[1]] = ''.join(rps[2:])
            print('Updated Product')

        elif rps[0] == 'CREATE':
            products[rps[1]] = ''.join(rps[2:])
            print('Created Product')

        else:
            print('NOT FOUND')

def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqtt_client.subscribe(subscribers)

class AdminPortalServicer(base_pb2_grpc.AdminPortal):

    ###### --------------------------------------------------------------- ###### 
    ######                      Client Functions                           ######
    ###### --------------------------------------------------------------- ######

    def CreateClient(self,request,target):
        """
            createClient() takes and CID [request.CID], and the data of the client [request.data],
            and add in the dictionary, if exists return error 2 and description, if not return error 0 
        """

        if request.CID not in clients:

            rps = mqtt_client.publish('clients', f'CREATE {request.CID} {request.data}')

            print('Created Client')
            return base_pb2.Reply(description=error.Error.noError, error=0)
        else: 
            print('Already in DataBase')
            return base_pb2.Reply(description=error.Error.clientExist, error=2)
            


    def RetrieveClient(self,request,target):
        """
            retrieveClient() takes and CID [request.ID], and check in the dictionary if the CID exist in the keys,
            if not return CID -1 and empty data (standard error), if it's return client
        """

        if request.ID not in clients:
            print('Client Doesn\'t Exist - Retrieve')
            return base_pb2.Client(CID='-1', data='\{\}')
        else: 
            print('Retrieve Client')
            return base_pb2.Client(CID=request.ID,data=clients[request.ID] )
        

    def UpdateClient(self,request,target):
        """
            updateClient() takes and CID [request.CID], and the data of the client [request.data],
            and check in the dictionary if CID exists in it, if it exists, update data and return error 0, 
            if it not return error 2 and description. 
        """

        if request.CID not in clients:
            print('Client Doens\'t Exist - Update')
            return base_pb2.Reply(description=error.Error.clientNotExist, error=2)
        else: 
            rps = mqtt_client.publish('clients', f'UPDATE {request.CID} {request.data}')

            if rps.is_published():
                print('Updated Client')
            else:
                print('Error sending message')

            return base_pb2.Reply(description=error.Error.noError, error=0)
        

    def DeleteClient(self,request,target):
        """
            deleteClient() takes and CID [request.ID], and check in the dictionary if the CID exist in the keys,
            if it not, return error 2 and description, if it's return error 0 
        """

        if request.ID not in clients:
            print('Client Doesn\'t Exist')
            return base_pb2.Reply(description=error.Error.clientNotExist, error=2)
        else: 

            mqtt_client.publish('clients', f'DELETE {request.ID}')
            return base_pb2.Reply(description=error.Error.noError, error=0)

    ###### --------------------------------------------------------------- ###### 
    ######                      Product Functions                          ######
    ###### --------------------------------------------------------------- ######
 
    def CreateProduct(self,request,target):
        """
            createProduct() takes and PID [request.PID], and the data of the product [request.data],
            and add in the dictionary, if exists return error 2 and description, if not return error 0 
        """

        if request.PID not in products:

            mqtt_client.publish('products', f'CREATE {request.PID} {request.data}')
            return base_pb2.Reply(description=error.Error.noError, error=0)
        
        else: 
            print('Already in DataBase')
            return base_pb2.Reply(description=error.Error.orderExist, error=2)

    def RetrieveProduct(self,request,target):
        """
            retrieveProduct() takes a PID [request.ID], and check in the dictionary if the PID exist in the keys,
            if not return PID -1 and empty data (standard error), if it's return product
        """
        print(products)
        if request.ID not in products:
            print('Product Doesn\'t Exist - Retrieve')
            return base_pb2.Product(PID='-1', data='\{\}')
        else: 
            print('Retrieve Product')
            return base_pb2.Product(PID=request.ID,data=products[request.ID])

    def UpdateProduct(self,request,target):
        """
            updateProduct() takes and PID [request.CID], and the data of the product [request.data],
            and check in the dictionary if PID exists in it, if it exists, update data and return error 0, 
            if it not return error 2 and description. 
        """

        if request.PID not in products:

            print('Product Doens\'t Exist - Update')
            return base_pb2.Reply(description=error.Error.orderNotExist, error=2)
        else: 

            mqtt_client.publish('products', f'UPDATE {request.PID} {request.data}')
            return base_pb2.Reply(description=error.Error.noError, error=0)

    def DeleteProduct(self,request,target):
        """
            deleteProduct() takes and PID [request.ID], and check in the dictionary if the PID exist in the keys,
            if it not, return error 2 and description, if it's return error 0 
        """

        if request.ID not in products:
            print('Product Doesn\'t Exist')
            return base_pb2.Reply(description=error.Error.orderNotExist, error=2)
        else: 
            
            mqtt_client.publish('products', f'DELETE {request.ID}')
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
    try:
        logging.basicConfig()

        #Open MQTT Connection
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.connect("localhost", 1883)
        mqtt_client.loop_start()


        serve(sys.argv[1:][0] if len(sys.argv[1:]) > 0 else '50055')
        
        # client.loop_forever()

    except:
        print("Disconnecting...")
        mqtt_client.disconnect()