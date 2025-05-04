from pymongo import MongoClient
import json
import os



with open("countrywise_state.json", "r") as file:
    student_arrival_flow = json.load(file)
    

client = MongoClient("0")
db = client["v0-Openlab-eth-chatbot-data"]

collection = db["CountrywiseStates"]


collection.replace_one({"_id": student_arrival_flow["_id"]}, student_arrival_flow, upsert=True)

print("Data inserted/updated successfully!")

# for country_doc in student_arrival_flow:
#     result = collection.insert_one(student_arrival_flow[country_doc]["IEAL_STATE_DATA"])
#     print(f"Data inserted with ID: {result.inserted_id}")


# def get_next_state(country_id, current_state):
#     """
#     Get the next state in the arrival flow based on the current state.
    
#     Args:
#         country_id (str): The ID of the country.
#         current_state (str): The current state in the arrival flow.
        
#     Returns:
#         str: The next state in the arrival flow, or None if current state is the last one.
#     """
#     country_doc = collection.find_one({"_id": country_id})
#     print(country_doc)
    
#     if not country_doc or "states" not in country_doc:
#         return None
#     ideal_states = list(country_doc["states"].keys())
#     print(ideal_states)
#     try:
#         current_index = ideal_states.index(current_state)
#         print(current_index)
#         print(len(ideal_states))
#         if current_index < len(ideal_states) - 1:
#             return ideal_states[current_index + 1],country_doc["states"][ideal_states[current_index + 1]]
#         else:
#             return None  
#     except ValueError:
#         return None

# current_state = "Arrival at Airport"
# next_state = get_next_state("Germany", current_state)
# print(f"Current State: {current_state}")
# print(f"Next State: {next_state}")