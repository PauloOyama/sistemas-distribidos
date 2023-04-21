from concurrent import futures
import logging
import grpc
import sys
from base import base_pb2_grpc,base_pb2
import paho.mqtt.client as mqtt
from common import error


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
            print(clients)
        else:
            print('NOT FOUND')
    elif msg.topic == 'products':
        pass


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(subscribers)

def publish(topic, payload):
    
    client.publish('clients',input('Teste Cliente'))
    # client.publish('products',input('Teste Produtos'))

class OrderPortalServicer(base_pb2_grpc.OrderPortal):

    client_orders = dict()


    def CreateOrder(self,request,target):
        print('OID -> ', request.OID)
        print('CID -> ', request.CID)
        print('data -> ', request.data)

        client.publish('clients', f'GET CID {request.CID}')
        
        if request.OID in self.client_orders:
            return base_pb2.Reply(description=error.Error.orderExist, error =3)
        else:
            aux = list() if request.CID not in self.client_orders.keys() else self.client_orders[request.CID]
            aux.append(request.OID)
            print(aux)
            self.client_orders[request.CID] = aux
            print(self.client_orders)



    def RetrieveOrder(self,request,target):
   
        pass

    def UpdateOrder(self,request,target):
        pass

    def DeleteOrder(self,request,target):
        pass

    def RetrieveClientOrders(self,request,target):
        pass

def serve(    port = '50051'):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    base_pb2_grpc.add_OrderPortalServicer_to_server(OrderPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    try: 
        logging.basicConfig()

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("localhost", 1883)
        client.loop_start()
        
        serve(sys.argv[1:][0] if len(sys.argv[1:]) > 0 else '50051')
        
        
        # client.loop_forever()
        
    except:
        print("Disconnecting...")
        client.loop_stop()
        client.disconnect()



