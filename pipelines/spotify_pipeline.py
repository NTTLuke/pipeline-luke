"""
title: Spotify Pipeline
author: nttluke
date: 2024-09-30
version: 1.0
license: MIT
description: A pipeline for creating spotify playlist
requirements: phidata
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import json
from services.spotify_assistant import SpotifyPlaylistAgent
from typing import Optional

# This pipline contains a workaround for having the chat_id in the pipeline using valves.
# see https://github.com/open-webui/pipelines/issues/168


class Pipeline:
    class Valves(BaseModel):
        spotify_access_token: str = "Your spotify access token"

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "wiki_pipeline"
        self.name = "Luke Spotify Pipeline"

        # Initialize rate limits
        self.valves = self.Valves(**{"pipelines": ["*"]})

        self.chat_id = None

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print(f"inlet:{__name__}")
        print(f"user: {user}")
        print(f"body: {body}")
        # Store the chat_id from body
        self.chat_id = body.get("chat_id")
        print(f"Stored chat_id: {self.chat_id}")

        return body

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")
        print(f"BODY: {body}")

        access_token = self.valves.spotify_access_token
        print(access_token)
        if not access_token:
            raise ValueError(
                "Spotify access token is required to create the MusicAssistant."
            )

        if body.get("title", False):
            print("Title Generation Request")

        print(f"chat_id available in pipe: {self.chat_id}")
        chat_id = self.chat_id
        if chat_id is None:
            raise ValueError("chat_id is required to create the MusicAssistant.")

        user_info = body["user"]
        user_id = user_info["id"]

        assistant = SpotifyPlaylistAgent()
        team = assistant.get_team(
            access_token=access_token, run_id=chat_id, user_id=user_id
        )

        try:
            for chunk in team.run(
                message=user_message,
                messages=messages,
                stream=True,
                # stream_intermediate_steps=True,
            ):
                yield chunk.content
        except Exception as e:
            yield f"Error during chat, please try again later."
