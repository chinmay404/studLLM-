from langchain_core.tools import tool



@tool
def GetAvilableApartments(location, rent, condtions, duration, trusted)-> dict:
    """
    This function retrieves available apartments based on the given location, check-in and check-out dates, and number of guests.

    Parameters:
    location (str): The location where the user wants to find an apartment.
    checkin (str): The check-in date in 'YYYY-MM-DD' format.
    checkout (str): The check-out date in 'YYYY-MM-DD' format.
    guests (int): The number of guests for the stay.

    Returns:
    Dictionary: A list of available apartments with their details.
    """
    # Placeholder for actual implementation
    return {
        "location": location,
        "rent": rent,
        "conditions": condtions,
        "duration": duration,
        "trusted": trusted,
        "apartments": [
            {
                "name": "Apartment 1",
                "price": 1200,
                "location": location,
                "availability": True
            },
            {
                "name": "Apartment 2",
                "price": 1500,
                "location": location,
                "availability": False
            }
        ]
    }
