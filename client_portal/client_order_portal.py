from __future__ import print_function

import logging

import grpc
from base import base_pb2
from base import base_pb2_grpc


def run():

    print("BlaBlaBla ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        pass
        stub = base_pb2_grpc.OrderPortalStub(channel)
        response = stub.CreateOrder(base_pb2.Order(OID='1',CID='2',data='3'))
    print("Greeter client received: " + response.description)


if __name__ == '__main__':
    logging.basicConfig()
    run()