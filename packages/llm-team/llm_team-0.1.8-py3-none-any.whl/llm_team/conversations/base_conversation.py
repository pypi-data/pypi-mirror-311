import logging
import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Optional, TypeAlias, Union

from llm_team.agents.basic_agent import LLMAgent
from llm_team.agents.messages import (
    LLMMessage,
    LLMToolUseDecision,
    NoToolsAvailable,
    ToolUsedOrFailed,
)
from llm_team.agents.tools.conversation import (
    create_read_all_conversation_messages_tool,
    create_read_previous_messages_tool,
)
from llm_team.config.configuration import project_configuration
from llm_team.conversations.messages import (
    AgentIntrospectionResult,
    ConversationMessage,
)
from llm_team.conversations.participants import (
    BroadcastToAllParticipants,
    HumanParticipant,
    Participant,
    SystemParticipant,
)
from llm_team.telemetry.conversation_telemetry import LLMConversationTelemetry
from llm_team.utils.exceptions import NotSupposedToHappenException

log = logging.getLogger(__name__)
default_enable_telemetry = project_configuration.get(
    "default_enable_telemetry")


@dataclass
class IntrospectionMessage:
    message: str


ConversationOrIntrospectionMessage: TypeAlias = Union[IntrospectionMessage,
                                                      ConversationMessage]


@dataclass(kw_only=True)
class BaseConversation(ABC):
    name: str = "Unnamed"
    participants: list[Participant] = field(default_factory=list)

    message_history: list[ConversationMessage] = field(default_factory=list)

    unprocessed_message: ConversationMessage | None = None
    initial_message: ConversationMessage | None = None

    human_intervention_count: int = 4

    def __post_init__(self):
        # number of messages before a human is prompted to allow the conversation to continue
        self.human_intervention_value = max(1, self.human_intervention_count)

        # counter to track how many messages have gone past since the last human confirmation
        self.human_intervention_counter = 0

        self.manual_interrupt_flag = False

        self.add_participant(HumanParticipant())

        self.telemetry_agent = LLMConversationTelemetry(
        ) if default_enable_telemetry else None

        if self.initial_message:
            self.add_initial_message(self.initial_message)

    @abstractmethod
    def _advance(self):
        """Processes the next unprocessed message in the conversation."""
        pass

    def add_initial_message(self, message: ConversationMessage):
        """Add an initial message at the start of the conversation
        """

        self.message_history = [message, *self.message_history]

    def format_message_in_xml(self, message: ConversationMessage) -> str:
        output = f"<Sender>{message.sender.name}</Sender>\n"
        output += f"<Recipient>{message.recipient.name}</Recipient>\n"
        output += message.content + '\n'
        return output

    def format_history_in_xml(self) -> str:
        participants = ",".join(p.name for p in self.participants)
        messages = [
            self.format_message_in_xml(message)
            for message in self.message_history
        ]
        messages_as_str = "\n\n".join(messages)
        return (
            f"Conversation participants: {participants}\nMessages:\n{messages_as_str}"
        )

    def display_conversation(self):
        text = ""
        text += f"\n\nConversation History, {self.name}"
        for message in self.message_history:
            sender_name = ("Human" if isinstance(
                message.sender, HumanParticipant) else message.sender.name)
            recipient_name = ("Human" if isinstance(message.recipient,
                                                    HumanParticipant) else
                              message.recipient.name)
            text += f"{sender_name} to {recipient_name}\n{message.content}\n"
        return text

    def add_participant(self, participant: Participant):
        """Add a new participant to the conversation."""
        if participant not in self.participants:
            self.participants.append(participant)

    def add_participants(self, participants: Sequence[Participant]):
        """Add new participants to the conversation. """
        for i in participants:
            self.add_participant(i)

    def get_participant_from_name(self, name: str) -> Optional[Participant]:
        return next((p for p in self.participants if p.name == name), None)

    def prepare_new_message(self, message: ConversationMessage):
        self.unprocessed_message = message

    def get_human(self):
        return HumanParticipant()

    def get_system(self):
        return SystemParticipant()

    def get_broadcast_to_all_participants(self):
        return BroadcastToAllParticipants()


@dataclass(kw_only=True)
class ConversationWithAgents(BaseConversation, ABC):
    """
    At start of conversation: initial system message added showing participants in conversation
    
    """
    agent_tool_use_enabled: bool = True
    message_history: list[ConversationMessage] = field(default_factory=list)

    introspection_limit: int = 3

    #     initial_message_text = """Hello! This is a conversation between AI Agents and human users.
    # The conversation is formatted with the sender and recipient at the top of each message in the conversation.
    # ```
    # <Sender>Person 1</Sender>
    # <Recipient>Person 2</Recipient>
    # Hello! How are you?

    # <Sender>Person 2</Sender>
    # <Recipient>Person 1</Recipient>
    # I'm great, thanks for asking! How about you?
    # ```\n
    # """

    def _advance(self):
        try:
            if not self.unprocessed_message:
                log.exception(
                    "tried to advance a conversation but there are no unprocessed messages"
                )
                return

            previous_message = self.unprocessed_message
            self.unprocessed_message = None

            self.message_history.append(previous_message)

            if (isinstance(previous_message.recipient,
                           HumanParticipant | SystemParticipant)
                    or self.manual_interrupt_flag):
                self._handle_new_message_for_human(previous_message)

            elif isinstance(previous_message.recipient, LLMAgent):
                self._handle_new_message_for_agent(
                    incoming_message=previous_message)

            else:
                raise ValueError(
                    f"Expected Conversation Participant but received {previous_message.recipient=}"
                )
        finally:
            if self.telemetry_agent:
                self.telemetry_agent.store_conversation_history(
                    conversation_name=self.name,
                    messages=self.message_history,
                )

    @abstractmethod
    def _handle_new_message_for_human(self,
                                      incoming_message: ConversationMessage):
        """The function that will be invoked if a new message is directed at the human user."""
        self.human_intervention_counter = 0
        self.manual_interrupt_flag = False

        pass

    def _handle_new_message_for_agent(
        self,
        incoming_message: ConversationMessage,
    ):
        agent = incoming_message.recipient

        thoughts: list[AgentIntrospectionResult] = []
        while len(thoughts) <= self.introspection_limit:
            introspection_result = self._agent_introspect(
                previous_thoughts=[i.thought for i in thoughts],
                incoming_message=incoming_message)

            if introspection_result.recipient != agent:
                self.prepare_new_message(
                    ConversationMessage(
                        sender=incoming_message.recipient,
                        recipient=introspection_result.recipient,
                        content=introspection_result.thought,
                    ))
                return
            else:
                log.info(f"{agent.name} diving deeper...")
                thoughts.append(introspection_result)

        self._handle_agent_introspection_overrun(
            agent_thoughts=thoughts,
            agent=agent,  # type: ignore
        )

    def _agent_introspect(
        self,
        previous_thoughts: list[str],
        incoming_message: ConversationMessage,
    ):
        """Allows an agent to think through their response upon receiving a conversation message and send it when they're ready."""

        agent = incoming_message.recipient
        assert isinstance(agent, LLMAgent)

        prompt = f"""You received a message from a conversation of which you are a participant. You are {self.name}.\n"""
        prompt += f"Here are the other participants in the conversation: {','.join(str(i) for i in self.participants)}\n"
        prompt += """Take your time to think through your response. If the task requires some thought, plan out how you should approach it first rather than immediately replying.\n"""
        prompt += f"Here are the last {len(self.message_history[-4:-1])} message before the latest message: {self.message_history[-4:-1]}"

        prompt += f"Here is the latest message from the conversation:\n{incoming_message}\n\n"

        if self.agent_tool_use_enabled:
            prompt += f"""Your message is sent ONLY to the first person you tag with their name (e.g. <Recipient>Example Name</Recipient>).
You have 2 options on handling this message:
1. You can think through the question, in which case your response will not have a recipient. 
2. You can send a message to any participant in the conversation. To do so, you can tag them anywhere in your response (e.g. <Recipient>Example Name</Recipient>).
"""
        if previous_thoughts:
            prompt += "Here were your previous thoughts while thinking about how to respond to the message:\n"
            prompt += "\n\n".join(previous_thoughts)

        # message_history = [
        #     self.format_message_in_xml(i) for i in self.message_history
        # ]

        # # allow the agents to read the main conversation thread if they need to
        # agent.register_tools(
        #     create_read_previous_messages_tool(message_history),
        #     create_read_all_conversation_messages_tool(message_history))

        # prepare output of function
        agent_thoughts_as_str = ''
        recipient = None

        if not agent.tools:
            agent_thoughts = agent.think(text=prompt)
            agent_thoughts_as_str = '\n'.join(i.content
                                              for i in agent_thoughts)

            # extract recipient of response, if any. if no recipient - assume is a self-thought
            recipient_by_name = self._extract_message_recipient(
                agent_thoughts_as_str)
            if not recipient_by_name:
                recipient = agent
            else:
                recipient = self.get_participant_from_name(recipient_by_name)
                if not recipient:
                    recipient = agent

            return AgentIntrospectionResult(recipient=recipient,
                                            thought=agent_thoughts_as_str,
                                            agent=agent)

        new_thought = agent.decide_and_use_tools(
            text=prompt,
            must_use_tool=False,
        )

        if isinstance(new_thought, NoToolsAvailable):
            raise NotSupposedToHappenException

        # no tool was chosen
        if all(isinstance(i, LLMMessage) for i in new_thought):  # type: ignore
            agent_thoughts: Sequence[LLMMessage] = new_thought  # type: ignore
            agent_thoughts_as_str = '\n'.join(i.content
                                              for i in agent_thoughts)

            # extract recipient of response, if any. if no recipient - assume is a self-thought
            recipient_by_name = self._extract_message_recipient(
                agent_thoughts_as_str)
            if not recipient_by_name:
                recipient = agent
            else:
                recipient = self.get_participant_from_name(recipient_by_name)
                if not recipient:
                    recipient = agent

            return AgentIntrospectionResult(recipient=recipient,
                                            thought=agent_thoughts_as_str,
                                            agent=agent)

        # tool was chosen and used
        else:
            tool_uses: list[
                tuple[LLMToolUseDecision,
                      ToolUsedOrFailed]] = new_thought  # type: ignore

            for tool_use_decision, tool_use_result in tool_uses:
                # include both the rationale and tool use result for now.
                agent_thoughts_as_str += tool_use_decision.format_as_message()
                agent_thoughts_as_str += "\n" + str(tool_use_result)

            # extract recipient of response, if any. if no recipient - assume is a self-thought
            recipient_by_name = self._extract_message_recipient(
                agent_thoughts_as_str)
            if not recipient_by_name:
                recipient = agent
            else:
                recipient = self.get_participant_from_name(recipient_by_name)
                if not recipient:
                    recipient = agent

            return AgentIntrospectionResult(agent=agent,
                                            recipient=recipient,
                                            thought=agent_thoughts_as_str)

    @abstractmethod
    def _handle_agent_introspection_overrun(
            self, agent_thoughts: list['AgentIntrospectionResult'],
            agent: LLMAgent):
        """The function that will be invoked if an agent has hit its introspection limit while forming its response."""
        log.warning('saving introspection history')
        if self.telemetry_agent:
            self.telemetry_agent.store_conversation_history(
                conversation_name=self.name,
                messages=self.message_history,
            )
            self.telemetry_agent.store_introspection_history(
                conversation_name=self.name,
                messages=agent_thoughts,
                agent_name=agent.name)

    def _check_if_human_intervention_required(self):
        return self.human_intervention_counter >= self.human_intervention_value

        # self.display_conversation()``
        # print(self.unprocessed_message)
        # print("AI conversation threshold reached.")
        # user_input = input(
        #     "Enter '1' to intervene after the next message, 0 to exit, or any key to allow the conversation to continue."
        # )

        # if user_input == "0":
        #     exit()
        # self.human_intervention_counter = 0
        # self.manual_interrupt_flag = user_input == "1"

    def _extract_message_recipient(self, message: str):

        pattern = r"<Recipient>(.*?)</Recipient>"
        recipients = re.findall(pattern, message, re.DOTALL)

        recipients: list[str] = [i for i in recipients if i != "Example Name"]

        return None if not recipients else recipients[0]


TOOL_USE_RECIPIENT_TEXT = "TOOL_USE"

TOOL_USE_RECIPIENT_TEXT = "TOOL_USE"
