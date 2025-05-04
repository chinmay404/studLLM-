from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import yaml


@tool
def search(query):
    """Search on the internet"""
    search = DuckDuckGoSearchRun()
    return search.run(query)

