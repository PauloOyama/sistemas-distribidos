from concurrent import futures
import logging
import grpc
import sys
from base import base_pb2_grpc,base_pb2


class OrderPortalServicer(base_pb2_grpc.OrderPortal):

    def CreateOrder(self,request,target):
        return base_pb2.Reply(description="Teste RECEBIDO AEEEE ", error =0)
        pass

    def RetrieveOrder(self,request,target):
   
        pass

    def UpdateOrder(self,request,target):
        pass

    def DeleteOrder(self,request,target):
        pass

    def RetrieveClientOrders(self,request,target):
        pass

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    base_pb2_grpc.add_OrderPortalServicer_to_server(OrderPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
