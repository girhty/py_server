#!/usr/bin/env python

import asyncio
import websockets
import json
import redis
import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://mongo:Gt38JOuEsD0xin7JSOEJ@containers-us-west-13.railway.app:7924")
cc=client["CC"]["info"]
r = redis.from_url("redis://default:te2WF7r63qOGkIAbrx8F@containers-us-west-65.railway.app:5589")

async def handle_message(websocket, message):
    msgstruct=json.loads(message)
    cardnum=str(msgstruct['cardnum'])
    await websocket.send("Order received")
    crddata=r.hgetall(cardnum)
    hash_data = {field.decode('utf-8'): value.decode('utf-8') for field, value in crddata.items()}
    if hash_data.__len__()<=0:
        await websocket.send("Invalid Card")
    elif int(msgstruct["amount"])<=0:
        await websocket.send("Amount cant be Negative Value")
    elif int(msgstruct["amount"])<=int(hash_data["amount"]):
        new_amount=str(int(hash_data['amount'])-msgstruct['amount'])
        r.hset(cardnum, 'amount', new_amount)
        trans={"T_Amount":msgstruct['amount'],"Am_Before":hash_data['amount'],"Am_After":new_amount,"date":datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        cc.update_one({'CCNUM':msgstruct['cardnum']},{'$addToSet':{'transactions':trans}})
        await websocket.send(f"success , remaining balance:{new_amount}")
        print(f"Sent response: {new_amount}")
    else:
        await websocket.send(f"proccess faild : insufficient funds , balance:{hash_data['amount']}")
        print("Sent Err")

async def server(websocket, path):
    print("New connection established")
    try:
        async for message in websocket:
            await handle_message(websocket, message)
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed gracefully")
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed with an error")

import os

port = os.environ.get('PORT')
start_server = websockets.serve(server, "0.0.0.0", port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()