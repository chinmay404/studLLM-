from langchain_core.tools import tool
import time
from datetime import datetime
from typing import Any
import sys
sys.path.append("..")
from ...DB_ops.main import MongoCRUD

db = MongoCRUD()


@tool
def set_things_about_user(user_id: str, things_data: dict) -> int | None:
    """Set various information about a user (replaces all existing things).

    Args:
        user_id (str): The user ID to set information for.
        things_data (dict): A dictionary containing information about the user.

    Returns:
        int: 1 if successful, 0 if failed.
    """
    result = db.set_user_things(user_id, things_data)
    return result


@tool
def get_things_about_user(user_id: str) -> dict | None:
    """Retrieve all stored information about a user.

    Args:
        user_id (str): The user ID to fetch information for.

    Returns:
        dict: A dictionary containing all information about the user if found, otherwise None.
    """
    things = db.get_user_things(user_id)
    return things if things else None


@tool
def update_things_about_user(user_id: str, things_to_update: dict) -> int | None:
    """Update specific pieces of information about a user without replacing all data.

    Args:
        user_id (str): The user ID to update information for.
        things_to_update (dict): A dictionary containing only the fields to update.

    Returns:
        int: 1 if successful, 0 if failed.
    """
    result = db.update_user_things(user_id, things_to_update)
    return result


@tool
def remove_things_about_user(user_id: str, keys: list) -> int | None:
    """Remove specific pieces of information about a user.

    Args:
        user_id (str): The user ID to remove information from.
        keys (list): A list of keys to remove from the user's information.

    Returns:
        int: The number of fields removed, 0 if none were removed.
    """
    result = db.remove_user_things(user_id, keys)
    return result


@tool
def add_single_thing_about_user(user_id: str, key: str, value: Any) -> int | None:
    """Add or update a single piece of information about a user.

    Args:
        user_id (str): The user ID to add information for.
        key (str): The key for the information (e.g., "favorite_color").
        value (any): The value to store.

    Returns:
        int: 1 if successful, 0 if failed.
    """
    # Create a dictionary with just this key-value pair
    update_dict = {key: value}
    result = db.update_user_things(user_id, update_dict)
    return result


@tool
def check_if_user_has_thing(user_id: str, key: str) -> bool:
    """Check if a specific piece of information exists for a user.

    Args:
        user_id (str): The user ID to check.
        key (str): The key to check for (e.g., "favorite_color").

    Returns:
        bool: True if the information exists, False otherwise.
    """
    things = db.get_user_things(user_id)
    return key in things if things else False


# @tool
# def get_single_thing_about_user(user_id: str, key: str) ->  | None:
#     """Get a specific piece of information about a user.

#     Args:
#         user_id (str): The user ID to get information for.
#         key (str): The key to retrieve (e.g., "favorite_color").

#     Returns:
#         any: The value if found, None otherwise.
#     """
#     things = db.get_user_things(user_id)
#     if not things:
#         return None
    
#     return things.get(key)