from ddgs import DDGS
from pprint import pprint


def ddg_search(keyword: str, doc_url: str, max_results: int = 5):
    """
    Search the latest official documentations for a given keyword
    """
    query = f"site:{doc_url} {keyword}"
    results = DDGS().text(query, region='us-en', safesearch='y', page=1, backend="auto", max_results=max_results)
    return [result.get("href") for result in results if not(is_empty(result.get("href")))]


def is_empty(var: str):
    return var is None or var.strip() == ""

if __name__ == '__main__':
    results = ddg_search("multi agent", "https://docs.langchain.com")
    pprint(results)