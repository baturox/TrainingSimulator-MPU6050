import asyncio
import datetime
import random
import websockets
import json

async def time(websocket, path):
    while True:
        Array = json.dumps({
            'x': random.random() * 3, 
            'y': random.random() * 3, 
            'z': random.random() * 3
            })
        await websocket.send(Array)
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()