from dataclasses import dataclass

from pydantic import BaseModel

from llm_team.agents.basic_agent import LLMAgent
from llm_team.conversations.participants import Participant
from llm_team.utils.serialization import SerializableMixin


class ConversationMessageModel(BaseModel):
    """
    Pydantic model representing the serializable fields of an ConversationMessage.

    This model serves as a schema for serialization and deserialization of ConversationMessage instances.
    It includes only the fields that should be persisted when serializing an ConversationMessage.
    """

    sender: Participant
    content: list[str]
    recipient: Participant

    class Config:
        extra = "ignore"  # This will ignore any extra fields during deserialization


@dataclass(kw_only=True)
class ConversationMessage(SerializableMixin):
    sender: Participant
    content: str
    recipient: Participant

    def is_from_human(self):
        return self.sender in ('human', 'Human')

    def __str__(self) -> str:
        return f"""ConversationMessage from {self.sender.name} to {self.recipient.name}\n{self.content}"""

    def to_dict(self):
        return {
            'sender': self.sender.name,
            'content': self.content,
            'recipient': self.recipient.name,
        }


@dataclass
class AgentIntrospectionResult:
    agent: LLMAgent
    thought: str
    recipient: Participant

    def to_dict(self):
        return {
            'thought': self.thought,
            'recipient': self.recipient.name,
            'originator': self.agent.name
        }
