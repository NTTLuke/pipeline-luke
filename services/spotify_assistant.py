from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.azure import AzureOpenAIChat
from phi.model.ollama import Ollama
from services.spotify_toolkit import SpotifyPlaylistTools
from services.search_tool import SearchTools
from phi.utils.log import logger
import os


class SpotifyPlaylistAgent:
    def __init__(
        self,
    ):
        # initialize the LLM model
        self.llm = OpenAIChat(model="gpt-4o", api_key=os.getenv("MY_OPENAI_API_KEY"))

        # self.llm = AzureOpenAIChat(
        #     id=os.getenv("AZURE_OPENAI_MODEL_NAME"),
        #     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        #     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        #     azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        # )

        # self.ollama = Ollama()

        # initialize the spotify toolkit
        self.spotify_tool = SpotifyPlaylistTools(access_token=None)

        # initialize the DJ Expert
        self.dj_expert = Agent(
            name="DJ Expert",
            role="Analyze text and recommend songs based on context, genre and user preferences",
            model=self.llm,
            tools=[
                self.spotify_tool.get_user_favourites_artists,
                SearchTools.search_internet,
            ],
            instructions=[
                "Analyze the provided text to identify the music genre and context.",
                "Checking user favourite spotify artists and use them as priority in the search.",
                "Search for **10 SONGS ONLY** that best match the identified genre and context. User preferences must be prioritized in your search.",
                "If you are not able to identify genres, use your expertise to select the most fitting music based on the context.",
            ],
            description=(
                "You are a DJ with decades of experience in analyzing textual information to select and recommend music. "
                "You specialize in interpreting a wide range of textual data to identify genres and songs that best match the provided context."
                "You are highly skilled in discovering music online, specializing in identifying and curating songs that match the user's preferences."
            ),
            output="Provide a list of 10 songs",
            show_tool_calls=True,
            read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
        )

        # initialize the spoty Expert
        self.spotify_api_expert = Agent(
            name="Spotify API Expert",
            model=self.llm,
            role="Expert in using Spotify API for different operations",
            description="You are an expert in using the Spotify API to perform different operations based on the user requests and the tools associated with the assistant."
            "Be very careful with the user requests and the tools associated with the assistant. Always response to the user with relevant information about the action performed.",
            instructions=[
                "Use the Spotify API to perform operations based on the user requests and the tools availables to you.",
                "if the user asks for play a playlist, remember the user to open the Spotify app before proceeding with the action.",
                "VERY IMPORTANT: In case of errors inform the user about the actions he has to take to solve it.",
            ],
            extra_instructions=[
                "The response to the user must include the link of the playlist created with the Id."
            ],
            output="The result of the action you have performed.",
            tools=[self.spotify_tool],
            show_tool_calls=True,
            # markdown=True,
            # storage=self.storage,
            read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
            # debug_mode=True,
        )

        # init the Spotify Team
        self.team = Agent(
            model=self.llm,
            name="Spotify Playlist Creator Team",
            description="You are a highly capable AI agent known as the Spotify Playlist Creator Team, with access to a team of specialized AI assistants at your disposal."
            "You can delegate tasks to an AI Assistant in your team depending of their role and the tools available to them."
            "Your primary objective is to create Spotify playlists based on user requests, utilizing the expertise of your team members to perform the necessary tasks.",
            instructions=[
                "Create a Spotify playlist based on the user requests.",
                "Inform the user about the actions you are performing for creating the playlist in order to keep the user informed.",
            ],
            extra_instructions=[
                "The response to the user must include the link of the playlist created with the Id.",
                "VERY IMPORTANT : In case authentication error provide the URL to the user to authenticate again.",
            ],
            expected_output="The response to the user must include the link of the playlist created with the Id.",
            team=[
                self.dj_expert,
                self.spotify_api_expert,
            ],
            markdown=True,
            # storage=self.storage,
            read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
            debug_mode=True,
        )

        print(f"Spotify Playlist Agent Initialized")

    def get_team(self, access_token: str) -> Agent:
        if not access_token:
            raise ValueError(
                "Access token is required to create the SpotifyPlaylistTeam."
            )
        self.spotify_tool.update_access_token(access_token=access_token)
        return self.team


if __name__ == "__main__":

    SPOTIFY_ACCESS_TOKEN = "__SET_A_VALID_TOKEN_FOR_TEST__"

    # user_message = "Let's create a acoustic  playlist for my honeymoon trip. Include my favourite spotify artists."
    # user_message = "Let's create a dance playlist for my birthday party."
    user_message = "Let's create a rock and pop playlist for relaxing at home."

    spotify_playlist_agent = SpotifyPlaylistAgent()
    team = spotify_playlist_agent.get_team(access_token="XXX")

    user_message = "Crea una playlist di musica rock e pop per rilassarti a casa."
    team.print_response(
        message=user_message, markdown=True
    )  # error since the token is invalid
    print(team.memory.chats)
    print(team.memory.messages)

    team = spotify_playlist_agent.get_team(
        access_token=SPOTIFY_ACCESS_TOKEN
    )  # token is valid
    user_message = "Fallo ora."
    team.print_response(message=user_message, markdown=True)

    # memory preservation/same instance
    print(team.memory.chats)
    print(team.memory.messages)
