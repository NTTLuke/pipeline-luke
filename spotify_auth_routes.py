##############################
# CUSTOM API FOR SPOTIFY AUTH ENDPOING
##############################

from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException, status, Request, Response
import requests
from main import (
    update_valves,
)  # used to update the valves.json file using the default method in main.py

import os
from main import app

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify API scopes
SCOPES = "playlist-modify-private playlist-modify-public user-modify-playback-state user-read-playback-state playlist-read-private user-follow-read user-top-read"

# Spotify API auth URL
REDIRECT_URI = "http://localhost:9099/spotify/callback"
AUTH_URL = f"https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri={REDIRECT_URI}"

# Spotify API token URL
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Redirect URL after login
# REDIRECT_RESPONSE_URL = "http://localhost:8000/static/index3.html?#showForm"


# add the custom router to the main app
spotify_router = APIRouter()


@spotify_router.get(
    "/v1/spotify/login",
    description="Redirects to Spotify login page. This is a custom endpoint and should be moved to a separate service.",
)
@spotify_router.get(
    "/spotify/login",
    description="Redirects to Spotify login page. This is a custom endpoint and should be moved to a separate service.",
)
def spotify_login():
    return RedirectResponse(url=AUTH_URL)


@spotify_router.get(
    "/v1/spotify/callback",
    description="Callback URL for Spotify login. This is a custom endpoint and should be moved to a separate service.",
)
@spotify_router.get(
    "/spotify/callback",
    description="Callback URL for Spotify login. This is a custom endpoint and should be moved to a separate service.",
)
def callback(code: str, request: Request, response: Response) -> RedirectResponse:
    import asyncio

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    token_response = requests.post(TOKEN_URL, data=payload)
    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error retrieving access token")

    token_data = token_response.json()
    access_token = token_data["access_token"]

    # Update the access token in the valves.json file
    form_data = {"spotify_access_token": access_token}
    pipeline_id = "spotify_pipeline"

    try:
        asyncio.run(update_valves(pipeline_id, form_data))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}",
        )

    # set the response to redirect to the frontend
    return "Access token retrieved successfully and updated into valves pipeline. You can close this tab now."


app.include_router(
    spotify_router,
    prefix="",
    tags=["spotify_auth"],
)
