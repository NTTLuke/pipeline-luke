import os
import json
import time
import requests


class SearchTools:
    def search_internet(query: str) -> str:
        """Search the internet for a given topic and return relevant results.

        Args:
            query (str): The query to search on the internet.

        Returns:
            str: The search results in a formatted string or an error message.
        """

        retries: int = 3
        backoff_factor: float = 0.5

        print("Searching the internet...", query)
        top_result_to_return = 3
        url = "https://google.serper.dev/search"

        payload = json.dumps({"q": query})
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "SERPAPI API key not found"

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        }

        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, data=payload)

                # Check if the request was throttled
                if response.status_code == 429:
                    retry_after = int(
                        response.headers.get("Retry-After", 1)
                    )  # Retry after time
                    print(f"Rate limited. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)  # Wait for the retry time
                    continue

                # Raise exception for other HTTP errors
                response.raise_for_status()

                # Parse JSON response
                response_data = response.json()

                # Check if organic results are available
                if "organic" not in response_data:
                    return "No results found"

                results = response_data.get("organic", [])
                formatted_results = []
                for result in results[:top_result_to_return]:
                    title = result.get("title", "No title available")
                    link = result.get("link", "No link available")
                    snippet = result.get("snippet", "No snippet available")
                    formatted_results.append(
                        f"Title: {title}\nLink: {link}\nSnippet: {snippet}"
                    )

                if not formatted_results:
                    return "No valid results found"

                return "\n\n".join(formatted_results)

            except requests.exceptions.RequestException as e:
                print(f"HTTP request failed: {e}")
                time.sleep(backoff_factor * (2**attempt))  # Exponential backoff delay

            except json.JSONDecodeError:
                return "Failed to parse the response as JSON"

        return f"Failed to retrieve data after {retries} retries."


# Example usage:
# print(SearchHelper.search_internet("Python programming"))
