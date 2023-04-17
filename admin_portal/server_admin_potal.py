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
        """
            createClient() takes and CID [request.CID], and the data of the client [request.data],
            and add in the dictionary, if exists return error 2 and description, if not return error 0 
        """

        if request.CID not in self.clients:
            self.clients[request.CID] = request.data
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

        if request.ID not in self.clients:
            print('Client Doesn\'t Exist - Retrieve')
            return base_pb2.Client(CID='-1', data='\{\}')
        else: 
            print('Retrieve Client')
            return base_pb2.Client(CID=request.ID,data=self.clients[request.ID] )
        

    def UpdateClient(self,request,target):
        """
            updateClient() takes and CID [request.CID], and the data of the client [request.data],
            and check in the dictionary if CID exists in it, if it exists, update data and return error 0, 
            if it not return error 2 and description. 
        """

        if request.CID not in self.clients:

            print('Client Doens\'t Exist - Update')
            return base_pb2.Reply(description=error.Error.clientNotExist, error=2)
        else: 
            self.clients[request.CID] = request.data
            print('Updated Client')
            return base_pb2.Reply(description=error.Error.noError, error=0)
        

    def DeleteClient(self,request,target):
        """
            deleteClient() takes and CID [request.ID], and check in the dictionary if the CID exist in the keys,
            if it not, return error 2 and description, if it's return error 0 
        """

        if request.ID not in self.clients:
            print('Client Doesn\'t Exist')
            return base_pb2.Client(description=error.Error.clientNotExist, error=2)
        else: 
            rqt = request.ID
            data = self.clients[request.ID] 
            print(rqt,data)
            del self.clients[request.ID]
            print('Delete Client')
            return base_pb2.Reply(description=error.Error.noError, error=0)

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
