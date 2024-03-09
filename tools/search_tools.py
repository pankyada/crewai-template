import json
import os

import requests
from langchain.tools import tool

class SearchTools():

    @tool("Search the Internet")
    def search_internet(query):
        """Useful to search the internet
        about a given topic and return relevant results."""
        print("searching the internet")
        top_result_to_return = 10
        url = "https://google.serper.dev/search"
        payload = json.dumps(
            {"q": query, "num": top_result_to_return})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        #check if there is an organic key
        if 'organic' not in response.json():
            return "Sorry, I couldnt find anything about that, there could be an error with your serper api key"
        else:
            results = response.json()['organic']
            string = []
            # print("Results: ", results[:top_result_to_return])
            for result in results[:top_result_to_return]:
                print(result)
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}",
                        "\n-----------------"
                    ]))
                except KeyError:
                    next

            return '\n'.join(string)
        