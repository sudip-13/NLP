from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import db_helper
import generic_helper


inprogress_orders={}
app = FastAPI()

@app.get('/api')
async def start():
   

    return {"message": "gand* marao"}
@app.post("/")
async def root(req: Request):
    payload = await req.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts=payload['queryResult']['outputContexts']

    session_id=generic_helper.extract_session_id(output_contexts[0]['name'])



    intent_handler ={
        'order.add - context: ongoing-order':add_to_order,
        'order.remove - context: ongoing-order':remove_from_order,
        'order.complete - context: ongoing-order':complete_order,
        'track.order - context: ongoing-tracking':track_order,
        'new.order':clear_inprogress_orders
    }
   
    return intent_handler[intent](parameters,session_id)

def complete_order(parameterrs:dict, session_id:str):

    if session_id not in inprogress_orders:
        fulfillment_text="I'm having a trouble finding your order. Sorry! can you place a new order please?"
    else: 
        order=inprogress_orders[session_id]
        orderId,totalprice=db_helper.add_order(order)


        if orderId==-1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
        else:
            fulfillment_text = f"Awesome. We have placed your order. " \
                           f"Here is your order id # {orderId}. " \
                           f"Your order total is {totalprice} which you can pay at the time of delivery!"
            
    del inprogress_orders[session_id]


    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def add_to_order(parameters: dict,session_id:str):
    food_items = parameters["food-item"]
    quantity = parameters["number"]
    print("Adding to order")
    if len(food_items) != len(quantity):
        fulfillment_text = "Sorry, I don't understand. Can you specify food items and quantity clearly?"
    else:
        new_food_dict=dict(zip(food_items,quantity))
        if session_id in inprogress_orders:
            current_food_dict=inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id]=current_food_dict
        else:
            inprogress_orders[session_id]=new_food_dict


        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text=f"So far you have: {order_str}. Do you need anything else?"

   
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })




def track_order(parameters: dict,session_id: str):
    print(parameters)
    order_id = parameters['order-id']
    order_status = db_helper.get_order_status(int(order_id))

    if order_status:
        fulfillment_text = f"Order status for order id: {order_id} is: {order_status}" 
    else:
        fulfillment_text = f"Order status for order id: {order_id} is not found"
    
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def remove_from_order(parameters: dict,session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text="I'm having a trouble finding your order. Sorry! can you place a new order please?"
    current_order = inprogress_orders[session_id]
    food_items = parameters["food-item"]

    removed_items=[]
    no_such_items=[]
    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]
    if len(removed_items)>0:
        fulfillment_text=f"Removed {", ".join(removed_items)} from your order!"
    if len(no_such_items)>0:
        fulfillment_text=f"Sorry, I couldn't find {', '.join(no_such_items)} in your order"
    if len(current_order.keys())==0:
        fulfillment_text="Your order is empty"

    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text=f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def clear_inprogress_orders(parameters: dict,session_id: str):
    if session_id in inprogress_orders:
        del inprogress_orders[session_id]
    fulfillment_text="Your previous order has been cleared"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })