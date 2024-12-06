from dataclasses import dataclass
from typing import TypeAlias, Union

from llm_team.agents.basic_agent import LLMAgent
from llm_team.utils.serialization import SerializableMixin

Participant: TypeAlias = Union[LLMAgent, 'HumanParticipant',
                               'SystemParticipant']
HumanMessage: TypeAlias = str


@dataclass(kw_only=True)
class SystemParticipant(SerializableMixin):

    def __init__(self) -> None:
        self.name = 'System'


@dataclass(kw_only=True)
class HumanParticipant(SerializableMixin):

    def __init__(self, ):
        self.name = 'Human'


@dataclass(kw_only=True)
class BroadcastToAllParticipants(SerializableMixin):

    def __init__(self, ):
        self.name = 'Broadcast To All Participants'
