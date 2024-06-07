from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Retrieve MongoDB connection URI from environment variable
uri = os.getenv("DB")
if uri is None:
    raise ValueError("DB environment variable is not set")

# Create a new client and connect to the MongoDB server
client = MongoClient(uri)

# Access the database
db = client["dialog-flow-chat-bot"]

# Access or create the collection
collection = db["orders"]

# Define functions to interact with the database

def add_order():
    order_data = [
        {"order_id": 41, "item_name": "pav bhaji,mango lassi", "order_status": "transit"},
        {"order_id": 345, "item_name": "Bryani,Samosa", "order_status": "delivered"},
        {"order_id": 453, "item_name": "chole bhature,chese pizza", "order_status": "transit"}
    ]

    # Insert the example data into the collection
    for order in order_data:
        existing_order = collection.find_one({"order_id": order["order_id"]})
        if existing_order is None:
            collection.insert_one(order)
            print(f"Inserted new order: {order}")
        else:
            print(f"Order with ID {order['order_id']} already exists. Skipping insertion.")

    # Confirm the successful insertion
    print("Data inserted successfully.")

def get_order_status(order_id):
    order = collection.find_one({"order_id": order_id})
    if order is None:
        print(f"Order with ID {order_id} not found.")
        return None
    else:
        print()
        return order["order_status"]


if __name__ == "__main__":

    order_status = get_order_status(41)