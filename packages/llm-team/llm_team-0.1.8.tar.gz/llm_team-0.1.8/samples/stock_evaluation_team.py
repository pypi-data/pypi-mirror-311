import logging

from llm_team.agents.basic_agent import LLMAgent
from llm_team.agents.tools.search_tools import internet_search__duckduckgo
from llm_team.conversations.cli_conversation import CLIConversation
from llm_team.conversations.messages import ConversationMessage
from llm_team.conversations.participants import HumanParticipant

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s',
                    level=logging.INFO)

log = logging.getLogger(__name__)

human = HumanParticipant()

researcher = LLMAgent(
    name="Researcher",
    prompt="",
)
researcher.register_tool(internet_search__duckduckgo)

manager = LLMAgent(
    name="Manager",
    prompt=
    "You are a manager of a team of agents. Lay out a plan to accomplish the task and make sure that they remain on track and work in measurable steps to complete it.",
)

conversation = CLIConversation(participants=[researcher, manager])
first_message = ConversationMessage(
    sender=human,
    recipient=manager,
    content="Evaluate how the ASTS share is doing recently.")

conversation.start_interruptable_conversation(first_message)
