"""Tools for searching the internet and processing results."""

import logging
from typing import Literal, Optional

from duckduckgo_search import DDGS
from pydantic import BaseModel, Field
from tavily import (
    InvalidAPIKeyError,
    MissingAPIKeyError,
    TavilyClient,
    UsageLimitExceededError,
)

from llm_team.agents.tools.base_tool import AnthropicTool

log = logging.getLogger(__name__)


class SearchResult(BaseModel):
    """A single search result in a structured format."""

    title: str = Field(description="The title of the search result")
    content: str = Field(description="A brief excerpt or summary of the content")
    url: str | None = Field(description="The URL where this content was found")
    score: float | None = Field(
        description="The relevance score of the result", default=None
    )


class SearchQuery(BaseModel):
    """Parameters for performing a search."""

    query: str = Field(description="The search query to execute")
    max_results: int = Field(
        default=3, description="Maximum number of results to return (1-10)"
    )
    region: str = Field(default="wt-wt", description="Region code for search results")


def search_internet_with_duckduckgo(
    query: str, max_results: int = 3, region: str = "wt-wt"
) -> list[SearchResult]:
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
                if content := r.get("body"):
                    result = SearchResult(
                        title=r.get("title") or "", content=content, url=r.get("link")
                    )
                results.append(result)
            return results

    except Exception as e:
        log.error(f"Error performing search: {str(e)}")
        return []


# Tavily Search Integration
def search_internet_with_tavily(
    query: str,
    max_results: int = 5,
    search_depth: Literal["basic", "advanced"] = "basic",
    topic: Literal["general", "news"] = "news",
    days: Optional[int] = None,
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
) -> list[SearchResult]:
    """
    Search the internet using Tavily SDK and return structured results.

    Args:
        query: The search query to execute.
        max_results: Maximum number of results to return (default: 5).
        search_depth: Depth of the search (default: "basic").
        topic: Search topic (default: "general").
        days: Timeframe for news topic (optional).
        include_images: Whether to include images in the results (default: False).

    Returns:
        List of SearchResult objects containing structured information.
    """
    try:
        tavily_client = TavilyClient(api_key="YOUR_API_KEY_HERE")
        response = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            topic=topic,
            days=days or 3,
            include_images=False,
            include_domains=include_domains or [],
            exclude_domains=exclude_domains or [],
        )
        results = []
        for result in response["results"]:
            results.append(
                SearchResult(
                    title=result.get("title"),
                    content=result.get("content"),
                    url=result.get("url"),
                    score=result.get("score"),
                )
            )
        return results

    except MissingAPIKeyError:
        log.error("Missing API key for Tavily.")
    except InvalidAPIKeyError:
        log.error("Invalid API key for Tavily.")
    except UsageLimitExceededError:
        log.error("Usage limit exceeded. Please check your plan.")
    except Exception as e:
        log.error(f"Unexpected error during Tavily search: {e}")

    return []


# Create the Anthropic tool
internet_search__duckduckgo = AnthropicTool(
    name="search_internet",
    description="""Search the internet for information and return structured results. 
    Each result includes a title, snippet (summary), and URL. Results are limited to 
    prevent information overload.""",
    function=search_internet_with_duckduckgo,
)


# Create Tavily Tool for LLM
internet_search_tavily = AnthropicTool(
    name="search_internet_tavily",
    description="""Search the internet using the Tavily SDK and return structured results. 
                   Each result includes a title, snippet, URL, and relevance score.""",
    function=search_internet_with_tavily,
)
