from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import db_helper


app = FastAPI()

@app.get('/api')
async def start():
   

    return {"message": "gand* marao"}
@app.post("/")
async def root(req: Request):
    payload = await req.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']

    if intent == 'track.order - context: ongoing-tracking':
        response = track_order(parameters)
        return JSONResponse(content=response)

    return JSONResponse(content={
            'fulfillmentText': f'Received =={intent}== in the backend'
        })

def track_order(parameters: dict):
    print(parameters)
    order_id = parameters['order-id']
    order_status = db_helper.get_order_status(int(order_id))

    if order_status:
        fulfillment_text = f"Order status for order id: {order_id} is: {order_status}" 
    else:
        fulfillment_text = f"Order status for order id: {order_id} is not found"
    
    return {
        'fulfillmentText': fulfillment_text
    }
