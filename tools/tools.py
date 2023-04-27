from langchain.serpapi import SerpAPIWrapper
from langchain.agents import tool
import os


@tool
def get_profile_url(text:str)->str:
    """Searches for Linkedin profile page"""
    
    search = SerpAPIWrapper(serpapi_api_key=os.getenv('SERPAPI_API_KEY')) # type: ignore 
    res = search.run(f"{text}")
    return res
