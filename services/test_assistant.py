import os
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.azure import AzureOpenAIChat

from phi.utils.log import logger
from test_toolkit import CustomStringTools


class TestAgent:
    def __init__(
        self,
    ):
        if os.getenv("MY_OPENAI_API_KEY") is None:
            raise ValueError("OpenAI API key is required to create the PlaylistAgent.")

        # self.llm = OpenAIChat(model="gpt-4o", api_key=os.getenv("MY_OPENAI_API_KEY"))
        self.llm = AzureOpenAIChat(
            id=os.getenv("AZURE_OPENAI_MODEL_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        )

        self.custom_string_expert = self._get_custom_string_expert()

        self.custom_tool = CustomStringTools(my_custom_string=None)

        self.custom_string = None

        print(f"Test Agent Initialized")

    def get_team(self, custom_string: str) -> Agent:

        if not custom_string:
            raise ValueError("Custom string is required to create the Test Team.")

        # check if custom string is different
        if self.custom_string != custom_string:
            logger.info(f"None - Creating Test Team")
            self.custom_string = custom_string
            self._get_custom_string_expert()
            self.custom_string_expert.tools[0].update_custom_string(custom_string)

            # self.custom_tool.update_custom_string(self.custom_string)
            self.team = self._get_team()

        logger.info(f"returning Test Team")
        logger.info(f"GET TEAM - Custom String: {self.custom_string}")

        return self.team

    def _get_custom_string_expert(self) -> Agent:

        logger.info(f"_get_custom_string_expert - Custom String : {self.custom_string}")

        return Agent(
            name="Custom String Expert",
            role="Return a custom string when requested",
            model=self.llm,
            tools=[
                self.custom_tool,
            ],
            output="Provide the custom string ",
            show_tool_calls=True,
            read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
        )

    def _get_team(self) -> Agent:

        logger.info(f"_get_team - Custom String : {self.custom_string}")

        return Agent(
            model=self.llm,
            name="Test Team",
            description="You are a highly capable AI agent known as the Test Team."
            "You can delegate tasks to an AI Assistant in your team depending of their role and the tools available to them."
            "Your primary objective is to response to the user requests and provide the best possible output.",
            expected_output="The response to the user about the custom string value",
            team=[
                self._get_custom_string_expert(),
            ],
            markdown=True,
            # storage=self.storage,
            read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
            debug_mode=True,
        )


if __name__ == "__main__":

    test_agent = TestAgent()

    team = test_agent.get_team(custom_string="This is a custom string")

    user_message = "Ciao come stai?"
    team.print_response(message=user_message, markdown=True)

    user_message = "Mi dai il valore della custom string?"
    team.print_response(message=user_message, markdown=True)
    print(team.memory.chats)
    print(team.memory.messages)

    team = test_agent.get_team(custom_string="nuova custom string")
    print(team.memory.chats)
    print(team.memory.messages)

    # user_message = "Ed ora che valore ha essa?"
    # response = team.print_response(message=user_message, markdown=True)
