import os
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.azure import AzureOpenAIChat

from phi.utils.log import logger
from test_toolkit import CustomStringTools


class TestAgent:
    def __init__(self):
        # Initialize the LLM model
        self.llm = AzureOpenAIChat(
            id=os.getenv("AZURE_OPENAI_MODEL_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        )

        # Initialize the custom tool (Singleton instance)
        self.custom_tool = CustomStringTools(my_custom_string="valore iniziale")

        # Initialize the custom string expert agent
        self.custom_string_expert = Agent(
            name="Custom String Expert",
            role="Return a custom string when requested",
            model=self.llm,
            tools=[self.custom_tool],
            output="Provide the custom string",
            show_tool_calls=True,
            read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
        )

        # Initialize the team agent
        self.team = Agent(
            model=self.llm,
            name="Test Team",
            description=(
                "You are a highly capable AI agent known as the Test Team. "
                "You can delegate tasks to an AI Assistant in your team depending on their role and the tools available to them. "
                "Your primary objective is to respond to the user's requests and provide the best possible output."
            ),
            expected_output="The response to the user about the custom string value",
            team=[self.custom_string_expert],
            markdown=True,
            read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
            debug_mode=True,
        )

    def get_team(self, custom_string):
        self.custom_tool.update_custom_string(custom_string=custom_string)
        return self.team

    # def print_response(self, message):
    #     # Use the team agent to get the response
    #     return self.team.print_response(message=message, markdown=True)

    # def update_custom_string(self, new_value):
    #     # Update the custom string in the tool


if __name__ == "__main__":

    # Create an instance of the manager
    test_agent = TestAgent()
    team = test_agent.get_team(custom_string="Questo è un valore personalizzato")

    # First interaction
    user_message = "Mi dai il valore della custom string?"
    team.print_response(message=user_message)

    print(team.memory.chats)
    print(team.memory.messages)

    team = test_agent.get_team(custom_string="Nuovo valore personalizzato")
    # Second interaction
    user_message = "Ed ora che valore ha essa?"
    team.print_response(message=user_message)
    print(team.memory.chats)
    print(team.memory.messages)
