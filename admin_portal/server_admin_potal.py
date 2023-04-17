from concurrent import futures
import logging
import grpc
import sys
import random as rd
import time
from common import error
from base import base_pb2_grpc,base_pb2


class AdminPortalServicer(base_pb2_grpc.AdminPortal):
    clients = {}

    def CreateClient(self,request,target):

        if request.CID not in self.clients:
            self.clients[request.CID] = request.data
            print('Created Client')
            return base_pb2.Reply(description=error.Error.noError, error=0)
        else: 
            print('Already in DataBase')
            return base_pb2.Reply(description=error.Error.clientExist, error=2)
            


    def RetrieveClient(self,request,target):
        print("rquest " + request.ID)
        if request.ID not in self.clients:
            print('Client Doesn\'t Exist')
            return base_pb2.Client(CID='-1', data='\{\}')
        else: 
            print('Retrieve Client')
            return base_pb2.Client(CID=request.ID,data=self.clients[request.ID] )
        pass

    def UpdateClient(self,request,target):
        pass

    def DeleteClient(self,request,target):
        pass

    def CreateProduct(self,request,target):
        pass

    def RetrieveProduct(self,request,target):
        pass

    def UpdateProduct(self,request,target):
        pass

    def DeleteProduct(self,request,target):
        pass

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    base_pb2_grpc.add_AdminPortalServicer_to_server(AdminPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
