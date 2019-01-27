#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 17:09:36 2018

@author: maitre
"""
import logging
import pickle
import numpy as np
from pymongo import MongoClient

while True:

    client = MongoClient('mongodb://data_science:data_123@ds119343.mlab.com:19343/iris_flor')
    db = client['iris_flor']
    collection = db['especies']
    json_data = collection.find_one()
    print (json_data)
    
    for json_data in collection.find():
               sl = json_data['sl']
               sw = json_data['sw']
               pl = json_data['pl']
               pw = json_data['pw']
    
               print(sl)
               print(sw)
               print(pl)
               print(pw)
    
    file = open("../models/modelo_knn.mod", "rb")
    modelo = pickle.load(file)
    file.close()
    datos = np.array([sl, sw, pl, pw], ndmin = 2)
    
    predictions = modelo.predict(datos)
    clase = str(predictions)
    print(clase)
    
    collection.update({"sl":sl,"sw":sw,"pl":pl,"pw":pw},{"sl":sl,"sw":sw,"pl":pl,"pw":pw, "clase": clase})
    
    new_sl = str(sl)
    new_sw = str(sw)
    new_pl = str(pl)
    new_pw = str(pw)
    
    from socketIO_client_nexus import SocketIO,LoggingNamespace
    
    with SocketIO('localhost', 8080, LoggingNamespace) as socketIO:
            socketIO.emit('clasificacion',{"sl" : new_sl},{"sw" : new_sw},{"pl" : new_pl},{"pw" : new_pw},{"clase" : clase})
            socketIO.wait(seconds=1)