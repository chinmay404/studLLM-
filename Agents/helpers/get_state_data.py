from ..DB_ops.main import MongoCRUD

db = MongoCRUD()
stateclient = db.get_clients("v0-Openlab-eth-chatbot-data") 
state_collection = stateclient["CountrywiseStates"]
 



def get_next_state(country_id, current_state=None):
    """
    Get the next state in the arrival flow based on the current state.
    
    Args:
        country_id (str): The ID of the country.
        current_state (str): The current state in the arrival flow.
        
    Returns:
        str: The next state in the arrival flow, or None if current state is the last one.
        dict: The data associated with the next state, or None if not found.
    """
    country_doc = state_collection.find_one({"_id": country_id})  
    if not country_doc or "states" not in country_doc:
        return None, None

    ideal_states = list(country_doc["states"].keys())
    try:
        if current_state:
            current_index = ideal_states.index(current_state)
            if current_index < len(ideal_states) - 1:
                next_state = ideal_states[current_index + 1]
                next_state_data = country_doc["states"][next_state]
                return next_state, next_state_data
            else:
                print("Current state is the last one.")
                return None, None
        else:
            next_state = ideal_states[0]
            next_state_data = country_doc["states"][next_state]
            return next_state, next_state_data  
    except Exception as e:
        print(f"Error: {e}")
        return None, None

    
    
def get_ideal_states(country_id):
    """
    Get the ideal states for a given country.
    
    Args:
        country_id (str): The ID of the country.
        
    Returns:
        list: A list of ideal states for the country, or None if not found.
    """
    country_doc = state_collection.find_one({"_id": country_id})
    
    if not country_doc or "states" not in country_doc:
        return None
    
    return list(country_doc["states"].keys())