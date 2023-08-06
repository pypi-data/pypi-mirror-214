import json
import time
from itertools import islice

import requests
from bs4 import BeautifulSoup as bs4
from duckduckgo_search import DDGS

from .prompt import SUMMARIZE_PROMPT

MAX_ATTEMPTS = 3
MAX_SEARCH_RESULTS = 8


def get_browser_functions(ai: "OpenAI"):
    child = ai.make_child(model_name="gpt-3.5-turbo-16k")
    child.set_system_prompt(SUMMARIZE_PROMPT + "\nPlease include url links.")

    def _summarize(query_text: str, results: str) -> str:
        """Summarizes the query text and results."""
        return child(f"Query: {query_text}\nResults: {results}\nSummary: ")[1]

    def web_search(query_text: str) -> str:
        """Searches the web for the query text.

        :param query_text: The text to query.
        :type query_text: str
        :return: json dumped results (string)
        :rtype: str
        """
        attempts = 0
        search_results = []
        while attempts < MAX_ATTEMPTS:
            ddgs = DDGS()
            time.sleep(1)
            result = ddgs.text(query_text, region="ja-ja", safesearch="Off")
            search_results = list(islice(result, MAX_SEARCH_RESULTS))
            if search_results:
                break
            attempts += 1

        results = json.dumps(search_results, ensure_ascii=False, indent=2)
        ret = _summarize(query_text, results)
        return ret

    def visit_page(query_text: str, url: str) -> str:
        """Visits the page at the url and summarizes the text with respect to the query text. Recommended to use after web_search for each url.

        :param query_text: The text to query for summarization.
        :type query_text: str
        :param url: The url to visit (must be a valid url like `https://commerce-flow.com/request_brochure/`)
        :type url: str
        :return: The summarized text of the page.
        :rtype: str
        """
        response = requests.get(url)
        soup = bs4(response.text, "html.parser")
        body = soup.find("body").text.strip()
        ret = _summarize(query_text, body[:10000])
        return ret

    return web_search, visit_page
