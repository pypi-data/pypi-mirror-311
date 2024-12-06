"""Tools for searching the internet and processing results."""

import logging

from duckduckgo_search import DDGS
from pydantic import BaseModel, Field

from src.agents.tools.base_tool import AnthropicTool

log = logging.getLogger(__name__)


class SearchResult(BaseModel):
    """A single search result in a structured format."""
    title: str = Field(description="The title of the search result")
    snippet: str = Field(description="A brief excerpt or summary of the content")
    url: str | None = Field(description="The URL where this content was found")


class SearchQuery(BaseModel):
    """Parameters for performing a search."""
    query: str = Field(description="The search query to execute")
    max_results: int = Field(default=3, description="Maximum number of results to return (1-10)")
    region: str = Field(default="wt-wt", description="Region code for search results")


def search_internet(query: str, max_results: int = 3, region: str = "wt-wt") -> list[SearchResult]:
    """
    Search the internet using DuckDuckGo and return structured results.
    
    Args:
        query: The search query to execute
        max_results: Maximum number of results to return (default: 3)
        region: Region code for search results (default: worldwide)
    
    Returns:
        List of SearchResult objects containing structured information
    """
    try:
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, region=region, max_results=max_results):
                result = SearchResult(
                    title=r.get('title'),
                    snippet=r.get('body'),
                    url=r.get('link')
                )
                results.append(result)
            return results
        
    except Exception as e:
        log.error(f"Error performing search: {str(e)}")
        return []

# Create the Anthropic tool
internet_search = AnthropicTool(
    name="search_internet",
    description="""Search the internet for information and return structured results. 
    Each result includes a title, snippet (summary), and URL. Results are limited to 
    prevent information overload.""",
    function=search_internet
)
