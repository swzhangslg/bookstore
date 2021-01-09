import requests
from urllib.parse import urljoin


class Search:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "auth/")

    def search_author(self, author: str) -> int:
        json = {"author": author}
        url = urljoin(self.url_prefix, "search_author")
        r = requests.post(url, json=json)
        return r.status_code

    def search_book_intro(self, book_intro: str) -> int:
        json = {"book_intro": book_intro}
        url = urljoin(self.url_prefix, "search_book_intro")
        r = requests.post(url, json=json)
        return r.status_code

    def search_tags(self, tags: str) -> int:
        json = {"tags": tags}
        url = urljoin(self.url_prefix, "search_tags")
        r = requests.post(url, json=json)
        return r.status_code

    def search_title(self, title: str) -> int:
        json = {"title": title}
        url = urljoin(self.url_prefix, "search_title")
        r = requests.post(url, json=json)
        return r.status_code

    def search_author_in_store(self, author: str, store_id: str) -> int:
        json = {"author": author, "store_id": store_id}
        url = urljoin(self.url_prefix, "search_author_in_store")
        r = requests.post(url, json=json)
        return r.status_code

    def search_book_intro_in_store(self, book_intro: str, store_id: str) -> int:
        json = {"book_intro": book_intro, "store_id": store_id}
        url = urljoin(self.url_prefix, "search_book_intro_in_store")
        r = requests.post(url, json=json)
        return r.status_code

    def search_tags_in_store(self, tags: str, store_id: str) -> int:
        json = {"tags": tags, "store_id": store_id}
        url = urljoin(self.url_prefix, "search_tags_in_store")
        r = requests.post(url, json=json)
        return r.status_code

    def search_title_in_store(self, title: str, store_id: str) -> int:
        json = {"title": title, "store_id": store_id}
        url = urljoin(self.url_prefix, "search_title_in_store")
        r = requests.post(url, json=json)
        return r.status_code
