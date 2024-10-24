from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.ollama import Ollama
from services.spotify_toolkit import SpotifyPlaylistTools
from services.search_tool import SearchTools
import os


class SpotifyPlaylistAgent:
    def __init__(
        self,
    ):
        if os.getenv("MY_OPENAI_API_KEY") is None:
            raise ValueError("OpenAI API key is required to create the PlaylistAgent.")

        self.llm = OpenAIChat(model="gpt-4o", api_key=os.getenv("MY_OPENAI_API_KEY"))
        # self.llm = Ollama(model="llama3.2:1b")

    def _get_dj_expert(self, access_token: str, run_id: str, user_id: str) -> Agent:
        return Agent(
            name="DJ Expert",
            role="Analyze text and recommend songs based on context, genre and user preferences",
            model=self.llm,
            tools=[
                SpotifyPlaylistTools(
                    access_token=access_token
                ).get_user_favourites_artists,
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
            # read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
            run_id=run_id,
            user_id=user_id,
        )

    def _get_spotify_api_expert(
        self, access_token: str, run_id: str, user_id: str
    ) -> Agent:

        if not access_token:
            raise ValueError(
                "Access token is required to create the Spotify API Expert."
            )

        self.access_token = access_token

        return Agent(
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
            tools=[SpotifyPlaylistTools(access_token=self.access_token)],
            show_tool_calls=True,
            # markdown=True,
            # storage=self.storage,
            # read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
            # debug_mode=True,
            run_id=run_id,
            user_id=user_id,
        )

    def get_team(self, access_token: str, run_id: str, user_id: str) -> Agent:

        if not access_token:
            raise ValueError(
                "Access token is required to create the SpotifyPlaylistTeam."
            )

        if not run_id:
            raise ValueError("Run ID is required to create the SpotifyPlaylistTeam.")

        if not user_id:
            raise ValueError("User ID is required to create the SpotifyPlaylistTeam.")

        return Agent(
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
                self._get_dj_expert(
                    access_token=access_token, run_id=run_id, user_id=user_id
                ),
                self._get_spotify_api_expert(
                    access_token=access_token, run_id=run_id, user_id=user_id
                ),
            ],
            markdown=True,
            # storage=self.storage,
            # read_chat_history=True,
            add_history_to_messages=True,
            num_history_responses=3,
            debug_mode=True,
            run_id=run_id,
            user_id=user_id,
        )


if __name__ == "__main__":

    print(f"pipe:{__name__}")
    access_token = ""
    run_id = "1"
    user_id = "luke"
    # user_message = "Let's create a acoustic  playlist for my honeymoon trip. Include my favourite spotify artists."
    # user_message = "Let's create a dance playlist for my birthday party."
    user_message = "Let's create a rock and pop playlist for relaxing at home."

    spotify_playlist_agent = SpotifyPlaylistAgent()
    team = spotify_playlist_agent.get_team(
        access_token=access_token, run_id=run_id, user_id=user_id
    )

    response = team.print_response(message=user_message, markdown=True)
