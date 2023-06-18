from concurrent import futures
import logging
import grpc
import sys
from base import base_pb2_grpc,base_pb2
import paho.mqtt.client as mqtt
from common import error
import re


subscribers = [('clients',0), ('products',0), ('orders',0)]


client_orders = dict()
orders_oid = dict()
# [clients] take the CID as value and the data as value
clients = {}
# [products] take the PID as value and the data as value
products = {}
# [price_by_product] take the PID as value and the price of that product as value
price_by_product = {}
# [qtd_by_product] take the PID as value and the absolut quantity of that product as value
qtd_by_product = {}
order_like_lst_of_dicts = []

    ###### --------------------------------------------------------------- ###### 
    ######                     Auxiliar Functions                          ######
    ###### --------------------------------------------------------------- ######

def get_name(pid: str):
    """
        get_name() take a PID and return the name of the product
    """
    names = re.findall("\'[a-zA-Z]+\'",products[pid])
    return names[2]



def productParser(data:str) -> None:

    key = re.findall("\'[a-zA-Z]+\'",data)
    key = [x.strip('\'') for x in key]
    values = re.findall("\'[0-9]{1,2}\.?[0-9]{0,2}\'",data)
    values = [x.strip('\'') for x in values]

    price_by_product[values[0]] = float(values[1])
    qtd_by_product[values[0]] = int(values[2])



def orderParser(data: str)-> None:
    """
        orderParser() take the data and parser into a list of dicts for better manipulation later
    """
    aux = dict()

    key = re.findall("\'[a-zA-Z]+\'",data)
    key = [x.strip('\'') for x in key]
    values = re.findall("\'[0-9]{1,2}\.?[0-9]{0,2}\'",data)
    values = [x.strip('\'') for x in values]

    cont = 1
    lst = []
    while cont <= (len(key)):

        aux[key[cont-1]] = values[cont-1] 
        if cont%2==0:
            lst.append(aux.copy())
            aux.clear()
        cont+=1

    global order_like_lst_of_dicts 
    order_like_lst_of_dicts  = lst.copy()

    ###### --------------------------------------------------------------- ###### 
    ######                     MQTT     Functions                          ######
    ###### --------------------------------------------------------------- ######

# def on_message(client, userdata, msg):
#     """
#         on_message is a handler for when MQTT protocol receive a message, it'll filter the message receive
#         storaging the data the local memory
#     """

#     print(msg.topic+" "+str(msg.payload.decode()))
#     rps = str(msg.payload.decode()).split(' ')

#     if msg.topic == 'clients':

#         if rps[0] == 'DELETE':
#             rqt = rps[1]
#             data = clients[rqt] 
#             del clients[rps[1]]
#             print(rqt,data)

#         elif rps[0] == 'UPDATE':
#             clients[rps[1]] = ''.join(rps[2:])

#         elif rps[0] == 'CREATE':
#             clients[rps[1]] = ''.join(rps[2:])
#             print(clients)

#         else:
#             print('NOT FOUND')

#     elif msg.topic == 'products':

#         if rps[0] == 'DELETE':
#             rqt = rps[1]
#             data = products[rqt] 
#             del products[rps[1]]
#             print(rqt,data)

#         elif rps[0] == 'UPDATE':
#             products[rps[1]] = ''.join(rps[2:])
#             print('Updated Product')

#         elif rps[0] == 'CREATE':
#             products[rps[1]] = ''.join(rps[2:])
#             productParser(products[rps[1]])
#             print('Created Product')

#         else:
#             print('NOT FOUND')

#     elif msg.topic == 'orders':

#         if rps[0] == 'CREATE':
#             oid = rps[1]
#             cid = rps[2]
#             data = ''.join(rps[3:])

#             aux = list() if cid not in client_orders.keys() else client_orders[cid]
#             orderParser(data)

#             aux.append(oid)
#             client_orders[cid] = aux
#             orders_oid[oid] = order_like_lst_of_dicts

#         elif rps[0] == "CHANGE":
#             pid = rps[1]
#             qtd = rps[2]
#             qtd_by_product[pid] = int(qtd)

#         elif rps[0] == "DELETE":
#             oid = rps[1]
#             cid = rps[2]

#             client_orders[cid].remove(oid)
#             del orders_oid[oid]


class OrderPortalServicer(base_pb2_grpc.OrderPortal):


    ###### --------------------------------------------------------------- ###### 
    ######                      Orders  Functions                          ######
    ###### --------------------------------------------------------------- ######

    def CreateOrder(self,request,target):
        aux = list() if request.CID not in client_orders.keys() else client_orders[request.CID]
        
        #Check if OID exists
        if request.OID in aux:
            return base_pb2.Reply(description=error.Error.orderExist, error =1)
        
        #Check if CID exists
        if request.CID not in clients:
            print("CID Not Found...")
            return base_pb2.Reply(description=error.Error.clientNotExist, error =1)

        orderParser(request.data)
        
        #TODO
        # rollback_qtd = int(order['quantity'])
        for order in order_like_lst_of_dicts:
            print(order)
            qtd = int(order['quantity'])

            #Product ID doenst exist
            if order['PID'] not in products.keys():
                print('Product Doens\'t exist')
                return base_pb2.Reply(description=error.Error.productNotExist, error=1)
            
            #Insufficient quantity
            elif (qtd_by_product[order['PID']] - qtd) < 0:
                print('Can\'t create - Quantity Exceeds Limit')
                return base_pb2.Reply(description=error.Error.messageError, error=1)
            
            else:
                #Product Exist and Quantity is available
                pid = order['PID']
        #         qtd_by_product[pid] = qtd_by_product[order['PID']] - qtd
        #         client.publish('orders', f'CHANGE {pid} {str(qtd_by_product[pid])}')

        
        # client.publish('orders', f'CREATE {request.OID} {request.CID} {request.data}')

        return base_pb2.Reply(description=error.Error.noError, error =0)



    def RetrieveOrder(self,request,target):
        
        oid = request.ID.split(':')[0]
        cid = request.ID.split(':')[1]

        lst_oids = []
        for x in client_orders.values():       
            lst_oids[::] = lst_oids + x

        #Client doesn't exist
        if cid not in client_orders.keys():
            print('CID Not Exist')
            return base_pb2.Order(OID = '0',CID = '0',data = '{}')
        
        # Order doesn't exist
        elif oid not in lst_oids:
            print('OID Not Exist')
            return base_pb2.Order(OID = '0',CID = '0',data = '{}')
        else:
            aux = dict()
            orders = orders_oid[oid]
            
            qtd = 0
            set_aux = set()
            for order in orders:
                name = get_name(order['PID'])
                price = price_by_product[order['PID']]
                qtd_i = price*int(order['quantity'])
                qtd += qtd_i
                set_aux.add(name)

            aux['products'] = str("{}" if len(set_aux) == 0 else str(set_aux))
            aux['total'] = qtd

            return base_pb2.Order(OID = str(oid),CID = str(cid),data = str(aux))

    def UpdateOrder(self,request,target):

        oid = request.OID
        cid = request.CID

        #IT'S A DELETE FOLLOWED BY A CREATE

        #UPDATE PART
        #Client doesn't exist
        if cid not in clients:
            print("CID Not Found...")
            return base_pb2.Reply(description=error.Error.clientNotExist, error =1)
    
        #Order doesn't exist
        if oid not in client_orders[cid]:
            print("Order Not Found...")
            return base_pb2.Reply(description=error.Error.orderNotExist, error =1)

        print('UPDATE #-------------------')
        #Refactor **TODO**
        orders = orders_oid[oid]
        for order in orders:
            pid = order['PID']
            qtd = qtd_by_product[pid] + int(order['quantity'])
            # rs = client.publish('orders', f'CHANGE {pid} {qtd}')
            # rs.wait_for_publish()

        # client.publish('orders', f'DELETE {oid} {cid}')

        # CREATE PART 
        orderParser(request.data)
        
        for order in order_like_lst_of_dicts:
            qtd = int(order['quantity'])

            #Product ID doenst exist
            if order['PID'] not in products.keys():
                print('Product Doens\'t exist')
                return base_pb2.Reply(description=error.Error.productNotExist, error=1)
            
            #Insufficient quantity
            elif (qtd_by_product[order['PID']] - qtd) < 0:
                print('Can\'t update - Quantity Exceeds Limit')
                return base_pb2.Reply(description=error.Error.messageError, error=1)
            
            else:
                #Product Exist and Quantity is available
                pid = order['PID']
                qtd_by_product[pid] = qtd_by_product[order['PID']] - qtd
        #         client.publish('orders', f'CHANGE {pid} {str(qtd_by_product[pid])}')

        # client.publish('orders', f'CREATE {request.OID} {request.CID} {request.data}')

        return base_pb2.Reply(description=error.Error.noError, error =0)


    def DeleteOrder(self,request,target):
        
        oid = request.ID.split(':')[0]
        cid = request.ID.split(':')[1]

        #Client doesn't exist
        if cid not in clients:
            print("CID Not Found...")
            return base_pb2.Reply(description=error.Error.clientNotExist, error =1)
    
        if oid not in client_orders[cid]:
            print("Order Not Found...")
            return base_pb2.Reply(description=error.Error.orderNotExist, error =1)
        
        print('DELETE #-------------------')
        orders = orders_oid[oid]
        for order in orders:
            print(order)
            pid = order['PID']
            print(qtd_by_product[pid])
            qtd = qtd_by_product[pid] + int(order['quantity'])
            print(qtd)
            # rs = client.publish('orders', f'CHANGE {pid} {qtd}')
            # rs.wait_for_publish()
            # print(rs.is_published())

        # client.publish('orders', f'DELETE {oid} {cid}')

        return base_pb2.Reply(description=error.Error.noError, error =0)


    def RetrieveClientOrders(self,request,target):
        
        if request.ID not in client_orders.keys():
            return base_pb2.Order(OID = '0',CID = '0',data = '{}')
        else:
            for oid in client_orders[request.ID]:
                yield base_pb2.Order(OID = oid ,CID = request.ID, data = str(orders_oid[oid]))



def serve( port = '50051'):

    #Set connection gRPC    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    base_pb2_grpc.add_OrderPortalServicer_to_server(OrderPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':

    # The server and client in portal will run on port 50051 by default
    try: 
        logging.basicConfig()


        
        serve(sys.argv[1:][0] if len(sys.argv[1:]) > 0 else '50051')
        
    except:
        print("Disconnecting...")


