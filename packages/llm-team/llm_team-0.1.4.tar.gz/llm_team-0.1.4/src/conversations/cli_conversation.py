import logging
from dataclasses import dataclass

from pynput import keyboard

from src.agents.basic_agent import LLMAgent
from src.conversations.base_conversation import ConversationWithAgents
from src.conversations.messages import AgentIntrospectionResult, ConversationMessage
from src.conversations.participants import HumanParticipant, SystemParticipant

log = logging.getLogger(__name__)


@dataclass
class IntrospectionLimitOverrun(Exception):
    """Exception raised when an agent's introspection exceeds allowed limits."""
    pass


@dataclass(kw_only=True)
class CLIConversation(ConversationWithAgents):
    """Handles command-line-based conversations with language model agents."""

    def start_interruptable_conversation(self,
                                         first_message: ConversationMessage):
        """
        Starts a conversation that allows user interruption via the keyboard.

        This method sets up the conversation with the provided first message,
        initializes a keyboard listener to detect interruptions, and begins
        processing conversation messages.

        """
        print(
            "Starting conversation, press the 'F1' key to interrupt the conversation at any point"
        )
        self._start_keyboard_listener()

        self.prepare_new_message(first_message)
        self._run_conversation()

    def _handle_new_message_for_human(self,
                                      incoming_message: ConversationMessage):
        """
        Handles a new message directed at the human participant.

        Prompts the user for input after displaying the conversation history
        and selects a recipient for the response.

        """
        super()._handle_new_message_for_human(incoming_message)

        human = self.get_human()
        print("\n\n<<Requesting human input>>")
        print(self.format_history_in_xml())

        recipient = self._choose_recipient([
            p for p in self.participants
            if not isinstance(p, HumanParticipant)
            and not isinstance(p, SystemParticipant)
        ])

        user_input = input(f"\n\nEnter your response > ")

        self.prepare_new_message(
            ConversationMessage(sender=human,
                                recipient=recipient,
                                content=user_input))

    def _choose_recipient(self, recipients: list[LLMAgent]):
        """
        Prompts the user to choose a recipient from a list of agents.
        """
        print("Choose a recipient of the message or -1 to exit:")
        choices = {str(idx): i for idx, i in enumerate(recipients, start=1)}
        for k, v in choices.items():
            print(f"{k}: {v.name}")
        while True:
            user_input = input(">")
            if user_input in ["-1", "exit"]:
                exit()
            if user_input in choices:
                return choices[user_input]
            else:
                print("Invalid selection.")

    def _start_keyboard_listener(self):
        """
        Starts a keyboard listener to detect interruptions during the conversation.

        Listens for the 'F1' key press to set an interrupt flag, enabling
        manual interruption of the conversation.
        """

        def on_press(key):
            if key == keyboard.Key.f1:
                print("Triggering interrupt")
                self.manual_interrupt_flag = True

        def on_release(key):
            return key not in ["\x03", keyboard.Key.esc]

        listener = keyboard.Listener(on_press=on_press,
                                     on_release=on_release)  # type: ignore

        listener.start()

    def _run_conversation(self):
        """
        Continuously processes messages in the conversation.

        This method loops through unprocessed messages and advances the conversation,
        handling any manual interruptions triggered by the user.
        """
        while self.unprocessed_message:
            if self.manual_interrupt_flag:
                self.manual_interrupt_flag = True
                self.manual_interrupt_flag = False

            self._advance()

    def _handle_agent_introspection_overrun(
            self, agent_thoughts: list['AgentIntrospectionResult'],
            agent: LLMAgent):
        """
        Handles cases where an agent's introspection exceeds the allowed limit.

        Logs the message history and raises an IntrospectionLimitOverrun exception.
        """

        super()._handle_agent_introspection_overrun(
            agent_thoughts=agent_thoughts, agent=agent)

        raise IntrospectionLimitOverrun
