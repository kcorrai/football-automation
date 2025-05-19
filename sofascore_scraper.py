import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_sofascore_link(match_query):
    """
    Fetches the first valid SofaScore link from the first 10 search results for the given match query.
    
    Args:
        match_query (str): The match query to search for (e.g., "São Paulo FC vs Grêmio FBPA score 2 - 1 sofascore").
    
    Returns:
        str: The first valid SofaScore link from the search results, or None if no valid link is found.
    """
    # Encode the query for the search engine
    query = urllib.parse.quote(match_query)
    search_url = f"https://www.google.com/search?q={query}"

    # Send a GET request to the search engine
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the first 10 search result links
        links = soup.find_all("a", href=True)[:10]
        for link in links:
            href = link["href"]
            # Filter for links containing "sofascore.com"
            if "sofascore.com" in href:
                # Extract the actual URL from the search result format
                if "/url?q=" in href:
                    return href.split("/url?q=")[1].split("&")[0]
    return None
