from typing import List
from phi.tools import Toolkit
from phi.utils.log import logger
import requests
from collections import Counter, defaultdict

from typing import List
from phi.tools import Toolkit
from phi.utils.log import logger
import requests
from collections import Counter, defaultdict
import traceback


class SpotifyPlaylistTools(Toolkit):
    def __init__(self, access_token: str):
        super().__init__(name="spotity_playlist_tools")
        self.register(self.get_user_id)
        self.register(self.search_songs_uris)
        self.register(self.create_playlist_by_uris)
        self.register(self.start_playlist_playback)
        self.register(self.get_user_favourites_artists)

        self.access_token = access_token

    def update_access_token(self, access_token: str):
        """
        Update the access token for the Spotify API requests.

        Args:
            access_token : str : The new access token to use for API requests.
        """
        self.access_token = access_token

    def _handle_request_error(self, e: Exception, function_name: str):
        logger.error(f"Error invoking {function_name}: {e}")
        logger.error(traceback.format_exc())

        if e.response.status_code in [400, 401, 403]:
            logger.error(f"Toolkit access token : {self.access_token}")
            return "Unauthorized access to Spotify. Please regenerate a new access token. Use this link http://localhost:9099/spotify/login for retrieving a new access token."

        return f"Error in {function_name}: {str(e)}"

    def get_user_id(self) -> str:
        """
        Make a request to Spotify API to get user information

        Returns:
            str: the user id of the spotify user
        """

        logger.info(f"Running get_user_id with access token")
        try:
            user_url = "https://api.spotify.com/v1/me"
            headers = {"Authorization": f"Bearer {self.access_token}"}

            user_response = requests.get(user_url, headers=headers)
            logger.debug(f"Result: {user_response}")

            user_response.raise_for_status()

            user_data = user_response.json()
            user_id = user_data["id"]

            return user_id
        except Exception as e:
            return self._handle_request_error(e, "get_user_id")

    def search_songs_uris(self, song_titles: List[str]) -> List[str]:
        """
        Userful to search the songs uri on spotify and return the list of uris of each song.

        Args:
            song_titles : List[str] : A list of song titles to search on spotify

        Returns:
            List[str] : The list of songs uris found on spotify

        """

        logger.info(f"Running search_songs_uris with access token")
        try:
            if not self.access_token:
                raise ValueError("No access token provided.")

            url = "https://api.spotify.com/v1/search"
            headers = {"Authorization": f"Bearer {self.access_token}"}

            songs_uris = []
            for song_title in song_titles:
                params = {"q": song_title, "type": "track", "market": "IT", "limit": 1}

                logger.debug(f"Searching for song: {song_title}")
                response = requests.get(url, params=params, headers=headers)
                logger.debug(f"Result: {response}")

                response.raise_for_status()

                data = response.json()
                if (
                    "tracks" in data
                    and "items" in data["tracks"]
                    and len(data["tracks"]["items"]) > 0
                ):
                    track_uri = data["tracks"]["items"][0]["uri"]
                    songs_uris.append(f"the song uri of {song_title} is : {track_uri}")
                else:
                    logger.info(f"No track found for {song_title}.")

            return "\n".join(songs_uris)

        except Exception as e:
            return self._handle_request_error(e, "search_songs_uris")

    def create_playlist_by_uris(
        self, songs_uris: List[str], playlist_name="made by NTTLuke (with Phidata)"
    ) -> str:
        """
        Userful to create a playlist on spotify by using the uris of the songs and returns the playlist id
        Uris of the songs can be retrieved using search_songs_uris method

        Args:
            songs_uris : List[str] : The list of songs uris to add to the playlist.
            playlist_name : str : The name of the playlist to create

        Returns
            str: the playlist id of the created playlist
        """

        logger.info(f"Running create_playlist_by_uris")
        try:
            user_id = self.get_user_id()
            if "Error" in user_id:
                raise ValueError(user_id)

            url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            data = {
                "name": playlist_name,
                "description": "generated by phidata",
                "public": False,
            }

            logger.debug(f"Creating playlist: {playlist_name}")

            response = requests.post(url, headers=headers, json=data)
            logger.debug(f"Result: {response}")

            response.raise_for_status()

            playlist_data = response.json()
            playlist_id = playlist_data.get("id")

            logger.info(f"Playlist created successfully with ID: {playlist_id}")

            data = {"uris": songs_uris, "position": 0}

            response = requests.post(
                f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                headers=headers,
                json=data,
            )
            response.raise_for_status()

            logger.info("Songs added to the playlist successfully.")
            return f"Created a new playlist with Playlist ID={playlist_id}"

        except Exception as e:
            return self._handle_request_error(e, "create_playlist_by_uris")

    def get_user_favourites_artists(
        self, limit=10, time_range="medium_term", genres_filter=None
    ):
        """
        Useful for retrieving user's favourite Spotify artists.
        It returns the top artists based on the user's listening history, optionally filtered by genre.

        Parameters:
        - limit (int): The number of top artists to return (default is 10).
        - time_range (str): The time range to consider for top artists. Options include:
            - 'short_term': Over the last 4 weeks
            - 'medium_term': Over the last 6 months (default)
            - 'long_term': Over the user's entire Spotify listening history
        - genres_filter (list): A list of genres to filter the artists by. If None, no genre filtering is applied (default is None).
        """

        try:
            url = f"https://api.spotify.com/v1/me/top/artists?limit={limit}&time_range={time_range}"
            headers = {"Authorization": f"Bearer {self.access_token}"}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            items = response.json()["items"]
            top_artists_genres = []

            for artist in items:
                artist_name = artist["name"]
                artist_genres = artist["genres"]

                # Filter artists based on genres if a filter is provided
                if genres_filter:
                    # Check if any of the artist's genres match the genres_filter
                    if not any(
                        genre.lower() in [g.lower() for g in artist_genres]
                        for genre in genres_filter
                    ):
                        continue  # Skip this artist if none of the genres match

                genres = (
                    ", ".join(artist_genres) if artist_genres else "No genres available"
                )
                artist_info = f"Artist: {artist_name}, Genres: {genres}"
                top_artists_genres.append(artist_info)

            # Return the list as a formatted string
            return "\n".join(top_artists_genres)

        except Exception as e:
            return self._handle_request_error(e, "get_favorite_artists")

    def start_playlist_playback(self, playlist_id: str) -> str:
        """
        Useful for initiating playback of a playlist on a user's device.
        Args:
            playlist_id : str : The id of the playlist to play

        Returns:
            str: the status of the playback
        """

        import time

        try:
            url = f"https://api.spotify.com/v1/me/player/devices"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            devices = response.json().get("devices", [])
            if not devices:
                return "You have to open at least one device to play the playlist."

            device_id = devices[0]["id"]
            device_name = devices[0]["name"]

            url = f"https://api.spotify.com/v1/me/player/play?device_id={device_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            data = {
                "context_uri": f"spotify:playlist:{playlist_id}",
                "offset": {"position": 0},
                "position_ms": 0,
            }

            counter = 0
            max_counter = 5
            while counter < max_counter:
                response = requests.get(
                    f"https://api.spotify.com/v1/playlists/{playlist_id}",
                    headers=headers,
                )

                if response.status_code == 200:
                    break
                else:
                    counter += 1
                    time.sleep(1)

            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            return f"Playback started successfully on device: {device_name}"

        except Exception as e:
            return self._handle_request_error(e, "start_playlist_playback")
