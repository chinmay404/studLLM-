import requests , os
import json
from langchain_core.tools import tool
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from dotenv import load_dotenv
from typing import Any



load_dotenv()
api_key = os.getenv("SERPER_API_KEY")
gl = "us"

@tool
def location_finder(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Tool for finding location information using Serper API

    Args:
        api_key (str): Your Serper API key
        query (str): Location to search for (e.g., "coffee shops in Boston")
        num_results (int): Maximum number of results to return

    Returns:
        List[Dict[str, Any]]: Location information including addresses, coordinates, and business details
    """
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "gl": gl,
        "num": num_results
    }

    try:
        response = requests.post(
            "https://api.serper.dev/search/places", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "places" in data:
            return data["places"][:num_results]
        return []
    except requests.exceptions.RequestException as e:
        return [{"error": str(e)}]

@tool
def news_search(query: str, num_results: int = 5, time_period: str = None) -> List[Dict[str, Any]]:
    """
    Tool for searching news articles using Serper API

    Args:
        api_key (str): Your Serper API key
        query (str): News topic to search for
        num_results (int): Maximum number of results to return
        time_period (str, optional): Time period for news (e.g., "d" for day, "w" for week, "m" for month)

    Returns:
        List[Dict[str, Any]]: News articles with titles, snippets, sources, and publish dates
    """
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "gl": gl,
        "num": num_results
    }
    if time_period:
        payload["tbs"] = f"qdr:{time_period}"

    try:
        response = requests.post(
            "https://api.serper.dev/search/news", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "news" in data:
            return data["news"][:num_results]
        return []
    except requests.exceptions.RequestException as e:
        return [{"error": str(e)}]

@tool
def places_search(query: str, location: str = None, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Tool for searching places and points of interest using Serper API

    Args:
        api_key (str): Your Serper API key
        query (str): Place or business type to search for (e.g., "restaurants", "hotels")
        location (str, optional): Location context (e.g., "New York")
        num_results (int): Maximum number of results to return

    Returns:
        List[Dict[str, Any]]: Places with names, addresses, ratings, and other business information
    """
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    search_query = query
    if location:
        search_query = f"{query} in {location}"

    payload = {
        "q": search_query,
        "gl": gl,
        "num": num_results
    }

    try:
        response = requests.post(
            "https://api.serper.dev/search/places", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "places" in data:
            return data["places"][:num_results]
        return []
    except requests.exceptions.RequestException as e:
        return [{"error": str(e)}]

@tool
def flight_search(origin: str, destination: str, date: str = None) -> Dict[str, Any]:
    """
    Tool for searching flight information using Serper API

    Args:
        api_key (str): Your Serper API key
        origin (str): Origin airport or city (e.g., "JFK", "New York")
        destination (str): Destination airport or city (e.g., "LAX", "Los Angeles")
        date (str, optional): Travel date in format YYYY-MM-DD, defaults to current date

    Returns:
        Dict[str, Any]: Flight options, prices, airlines, and travel times
    """
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # Craft a search query that will yield flight results
    search_query = f"flights from {origin} to {destination} on {date}"

    payload = {
        "q": search_query,
        "gl": gl
    }

    try:
        response = requests.post(
            "https://api.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        flight_data = {
            "search_query": search_query,
            "organic_results": data.get("organic", [])[:5],
            "flight_info": {}
        }
        if "answerBox" in data:
            flight_data["flight_info"]["answer_box"] = data["answerBox"]

        if "knowledgeGraph" in data:
            flight_data["flight_info"]["knowledge_graph"] = data["knowledgeGraph"]

        return flight_data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@tool
def google_scholar_search(query: str, num_results: int = 5,
                          year_start: int = None, year_end: int = None) -> List[Dict[str, Any]]:
    """
    Tool for searching academic papers through Google Scholar using Serper API

    Args:
        api_key (str): Your Serper API key
        query (str): Academic topic or keywords to search for
        num_results (int): Maximum number of results to return
        year_start (int, optional): Start year for filtering papers
        year_end (int, optional): End year for filtering papers

    Returns:
        List[Dict[str, Any]]: Academic papers with titles, authors, publication details, and citations
    """
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    search_query = query
    if year_start and year_end:
        search_query = f"{query} {year_start}..{year_end}"
    elif year_start:
        search_query = f"{query} {year_start}.."
    elif year_end:
        search_query = f"{query} ..{year_end}"

    payload = {
        "q": f"{search_query} site:scholar.google.com",
        "gl": gl,
        "num": num_results * 2
    }

    try:
        response = requests.post(
            "https://api.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        papers = []
        if "organic" in data:
            for result in data["organic"]:
                if "scholar.google.com" in result.get("link", "") or "academia" in result.get("link", "").lower():
                    paper = {
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "published_info": result.get("date", "")
                    }
                    papers.append(paper)
                    if len(papers) >= num_results:
                        break
        return papers
    except requests.exceptions.RequestException as e:
        return [{"error": str(e)}]
