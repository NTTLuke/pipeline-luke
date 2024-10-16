from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.llm.ollama import Ollama
from services.spotify_toolkit import SpotifyPlaylistTools
from services.search_tool import SearchTools
import os


class MusicAssistant:
    def __init__(
        self,
    ):
        if os.getenv("MY_OPENAI_API_KEY") is None:
            raise ValueError("OpenAI API key is required to create the MusicAssistant.")

        self.llm = OpenAIChat(model="gpt-4o", api_key=os.getenv("MY_OPENAI_API_KEY"))
        # self.llm = Ollama(model="llama3.2:1b")

    def _get_music_genres_expert(self, run_id: str, user_id: str) -> Assistant:
        return Assistant(
            run_id=run_id,
            user_id=user_id,
            llm=self.llm,
            # storage=self.storage,
            add_chat_history_to_prompt=True,
            num_history_messages=3,
            name="Expert Music Genres",
            role="Search for music genres on a given request",
            description="You are a highly skilled expert in discovering music online, specializing in identifying and curating music based on user preferences. "
            "If specific genres are not provided, use your expertise to select the most fitting genre based on what do you find online",
            instructions=[
                "Search for 10 SONGS ONLY based on the music genre.",
                "REMEMBER: This is very important task for the user, so the quality of the result is important.",
            ],
            output="A list of 10 songs found online",
            tools=[SearchTools.search_internet],
        )

    def _get_spotify_api_expert(
        self, access_token: str, run_id: str, user_id: str
    ) -> Assistant:

        if not access_token:
            raise ValueError(
                "Access token is required to create the Spotify API Expert."
            )

        self.access_token = access_token

        return Assistant(
            run_id=run_id,
            user_id=user_id,
            name="Spotify API Expert",
            llm=self.llm,
            # storage=self.storage,
            add_chat_history_to_prompt=True,
            num_history_messages=3,
            role="Expert in using Spotify API for different operations",
            description="You are an expert in using the Spotify API to perform different operations based on the user requests and the tools associated with the assistant."
            "Be very careful with the user requests and the tools associated with the assistant. Always response to the user with relevant information about the action performed.",
            instructions=[
                "Use the Spotify API to perform operations based on the user requests and the tools availables to you.",
                "if the user asks for play a playlist, remember the user to open the Spotify app before proceeding with the action.",
                "VERY IMPORTANT: In case of errors inform the user about the actions he has to take to solve it.",
            ],
            extra_instructions=[
                # "IMPORTANT: Limit each request to create a single playlist. DO NOT generate more then one playlists."
                "The response to the user must include the link of the playlist created with the Id."
            ],
            output="The result of the action you have performed.",
            tools=[SpotifyPlaylistTools(access_token=self.access_token)],
            show_tool_calls=True,
            # debug_mode=True,
        )

    def get_team(self, access_token: str, run_id: str, user_id: str) -> Assistant:

        if not access_token:
            raise ValueError(
                "Access token is required to create the SpotifyPlaylistTeam."
            )

        if not run_id:
            raise ValueError("Run ID is required to create the SpotifyPlaylistTeam.")

        if not user_id:
            raise ValueError("User ID is required to create the SpotifyPlaylistTeam.")

        return Assistant(
            run_id=run_id,
            user_id=user_id,
            llm=self.llm,
            name="Spotify Playlist Creator Team",
            # storage=self.storage,
            add_chat_history_to_prompt=True,
            num_history_messages=3,
            description="You are a highly capable AI agent known as the Spotify Playlist Creator Team, with access to a team of specialized AI assistants at your disposal."
            "You can delegate tasks to an AI Assistant in your team depending of their role and the tools available to them."
            "Your primary objective is to create Spotify playlists based on user requests, utilizing the expertise of your team members to perform the necessary tasks.",
            instructions=[
                "Create a Spotify playlist based on the user requests.",
                "When the user sends a message, first **think** and determine if:\n",
                " - You need to delegate the task to a team member for\n",
                " - You need to ask a clarifying question",
                "Inform the user about the actions you are performing for achieving the playlist creation using not technical language.",
                "VERY IMPORTANT: In case of errors inform the user about the actions he has to take to solve it.",
            ],
            extra_instructions=[
                "The response to the user must include the link of the playlist created with the Id."
            ],
            # output="The response to the user must include the link of the playlist created with the Id.",
            team=[
                self._get_music_genres_expert(run_id=run_id, user_id=user_id),
                self._get_spotify_api_expert(
                    access_token=access_token, run_id=run_id, user_id=user_id
                ),
            ],
            # debug_mode=True,
        )


if __name__ == "__main__":

    print(f"pipe:{__name__}")
    access_token = "YOUR_SPOTIFY_ACCESS_TOKEN"
    run_id = "1"
    user_id = "luke"
    user_message = "Create a Rock music Spotify playlist for a car trip that I'm going to have today."

    assistant = MusicAssistant()
    team = assistant.get_team(access_token=access_token, run_id=run_id, user_id=user_id)
    # team.print_response(user_message=user_message, markdown=True)

    # print(access_token)
    team.cli_app(markdown=True)
    # result = team.run(user_message, stream=False)
    # print(result)
