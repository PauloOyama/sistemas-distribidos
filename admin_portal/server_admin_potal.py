from concurrent import futures
import logging
import grpc
import sys
from base import base_pb2_grpc,base_pb2


class AdminPortalServicer(base_pb2_grpc.AdminPortal):

    def CreateClient(self,request,target):
        return base_pb2.Reply(description="OKSADASD", error =0)

    def RetrieveClient(self,request,target):
   
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
