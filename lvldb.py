import plyvel
import json
from pysyncobj import SyncObj, replicated

class Database(SyncObj):
  def __init__(self, port, part, primary, secundary):
    super(Database, self).__init__(primary, secundary)
    self.database = f'./files/{part}/{port}/'

  @replicated
  def insertData(self, key, value):
    print("ADD")
    db = plyvel.DB(self.database, create_if_missing=True)
    bytesKey = bytes(key, 'utf-8')
    bytesValue = bytes(value,'utf-8')
    db.put(bytesKey, bytesValue)
    db.close()
    
      
  @replicated
  def deleteData(self, key):
    print("DEL")
    
    db = plyvel.DB(self.database, create_if_missing=True)

    bytesKey = bytes(key, 'utf-8')
    db.delete(bytesKey)
    db.close()
    
  
  def updateData(self, key, value):
    print("UPDATE")
    self.deleteData(key)
    self.insertData(key, value)


  def getData(self, key):
    print("GET")
    
    db = plyvel.DB(self.database, create_if_missing=True)
    bytesKey = bytes(key, 'utf-8')
    respBytes = db.get(bytesKey)

    if respBytes:
      resp = respBytes.decode()
    else:
      resp = None
      
    db.close()
    return resp
  

