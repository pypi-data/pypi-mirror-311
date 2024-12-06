import logging

from llm_team.agents.basic_agent import LLMAgent
from llm_team.agents.tools.search_tools import internet_search__duckduckgo

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

agent = LLMAgent(
    name="Robert",
    prompt="",
)

agent.register_tool(internet_search__duckduckgo)

response = agent.decide_and_use_tools(
    text="How is the ASTS share doing recently?", must_use_tool=True)
