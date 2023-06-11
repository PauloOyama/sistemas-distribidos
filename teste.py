from concurrent import futures
import logging
import grpc
import sys
from base import base_pb2_grpc,base_pb2
import paho.mqtt.client as mqtt
from common import error
import re


if __name__ == '__main__':

        admin_port = 55055
        order_port = 55051
        print("A porta a ser utilizada para o OrderPortalServer é 55055")
        print("A porta a ser utilizada para o AdminPortalServer é 55051")
        input("Pressione qualquer tecla para continuar")
        channel = grpc.insecure_channel(f"localhost:{admin_port}")
        admin_stub = base_pb2_grpc.AdminPortalStub(channel)
        print("##### ======================================================================== #####")
        print("Caso de teste: CRUD do Cliente")
        cid = "1"
        input("Await ... ")
        print("##### ======================================================================== #####")
        print("Criando cliente com CID={cid} e data = {'CID': '1', 'name': 'Paulo'}")
        result = admin_stub.CreateClient(base_pb2.Client(CID=cid, data="{'CID': '1', 'name': 'Paulo'}"))
        if result.error == 0:
            print("Cliente adicionado com sucesso!")
        else:
            print(f"Erro: {result.description}")
        
