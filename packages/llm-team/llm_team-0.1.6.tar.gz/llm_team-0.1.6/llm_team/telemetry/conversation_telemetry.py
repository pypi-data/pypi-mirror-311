import logging
import os
from collections.abc import Sequence

from llm_team.config.project_paths import application_data_dir
from llm_team.conversations.messages import (
    AgentIntrospectionResult,
    ConversationMessage,
)
from llm_team.telemetry.common import load_json_from_disk, save_jsonlist_to_disk

log = logging.getLogger(__name__)


class LLMConversationTelemetry:

    def get_conversation_filepath(self, conversation_name: str):
        return application_data_dir / 'conversations' / f"{conversation_name}_messages.json"

    def get_agent_introspection_filepath(self, agent_name: str,
                                         conversation_name: str | None):
        conversation_name = conversation_name or "Unnamed"
        return application_data_dir / 'introspection' / conversation_name / f"{agent_name}_introspection.json"

    def store_conversation_history(
        self,
        conversation_name: str,
        messages: Sequence[ConversationMessage],
    ):
        data = [i.to_dict() for i in messages]

        save_jsonlist_to_disk(
            data, self.get_conversation_filepath(conversation_name))

    def store_new_conversation_message(
        self,
        conversation_name: str,
        message: ConversationMessage,
    ):
        history = self.get_conversation_history(conversation_name)
        history.append(message.to_dict())
        save_jsonlist_to_disk(
            history, self.get_conversation_filepath(conversation_name))

    def get_conversation_history(
        self,
        conversation_name: str,
    ):
        """
        Retrieve all messages for the specified agent.
        """

        messages = load_json_from_disk(
            filepath=self.get_conversation_filepath(conversation_name))
        return messages

    def get_introspection_history(self, agent_name: str,
                                  conversation_name: str | None):
        """
        Retrieve all messages for the specified agent.
        """

        messages = load_json_from_disk(
            filepath=self.get_agent_introspection_filepath(
                agent_name=agent_name, conversation_name=conversation_name))
        return messages

    def get_all_conversation_names(self):
        dirpath = self.get_conversation_filepath('').parent
        files = os.listdir(dirpath)
        conversations = [
            f.split("_")[0] for f in files if f.endswith("_messages.json")
        ]
        return conversations

    def store_new_introspection_message(self, agent_name: str,
                                        message: AgentIntrospectionResult,
                                        conversation_name: str | None):
        history = self.get_introspection_history(
            agent_name=agent_name, conversation_name=conversation_name)
        history.append(message.to_dict())

        save_jsonlist_to_disk(filepath=self.get_agent_introspection_filepath(
            agent_name=agent_name, conversation_name=conversation_name),
                              messages=history)

    def store_introspection_history(
            self, agent_name: str,
            messages: Sequence[AgentIntrospectionResult],
            conversation_name: str | None):

        history = [i.to_dict() for i in messages]
        save_jsonlist_to_disk(filepath=self.get_agent_introspection_filepath(
            agent_name=agent_name, conversation_name=conversation_name),
                              messages=history)
        save_jsonlist_to_disk(filepath=self.get_agent_introspection_filepath(
            agent_name=agent_name, conversation_name=conversation_name),
                              messages=history)
