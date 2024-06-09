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

def add_order(order_data: dict):
    try:
        print(order_data)

        price_details = {
            "pav bhaji": 40,
            "Chole Bhature": 15,
            "pizza": 60,
            "Mango Lassi": 20,
            "Masala Dosa": 70,
            "Vegetable Biryani": 50,
            "Vada Pav": 80,
            "Rava Dosa": 100,
            "Samosa": 10
        }
        max_order_id = collection.find_one(sort=[("orderId", -1)])
        if max_order_id:
            new_order_id = max_order_id["orderId"] + 1
        else:
            new_order_id = 1

        # Set default status as "transit" and add orderId to order_data
        total_price = 0
        for item, quantity in order_data.items():
            if item in price_details:
                item_price = price_details[item]
                total_price += item_price * quantity
            else:
                print(f"Item '{item}' not found in price details. Skipping...")

        order_data["status"] = "transit"
        order_data["orderId"] = new_order_id
        order_data["total_price"] = total_price

        # Insert the new order into the collection
        collection.insert_one(order_data)

        return new_order_id, total_price

    except Exception as e:
        # Rollback if a database error occurs
        print(f"Error occurred: {e}. Rolling back the transaction.")
        if new_order_id:
            collection.delete_one({"orderId": new_order_id})
        return -1, 0

        

  

def get_order_status(order_id):
    order = collection.find_one({"orderId": order_id})
    if order is None:
        print(f"Order with ID {order_id} not found.")
        return None
    else:
        print()
        return order["status"]

