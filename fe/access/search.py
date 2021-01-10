import requests
from urllib.parse import urljoin


class Search:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "auth/")

    def search_author(self, author: str, page: int) -> int:
        json = {"author": author, "page": page}
        url = urljoin(self.url_prefix, "search_author")
        r = requests.post(url, json=json)
        return r.status_code

    def search_book_intro(self, book_intro: str, page: int) -> int:
        json = {"book_intro": book_intro,"page": page}
        url = urljoin(self.url_prefix, "search_book_intro")
        r = requests.post(url, json=json)
        return r.status_code

    def search_tags(self, tags: str, page: int) -> int:
        json = {"tags": tags, "page": page}
        url = urljoin(self.url_prefix, "search_tags")
        r = requests.post(url, json=json)
        return r.status_code

    def search_title(self, title: str, page: int) -> int:
        json = {"title": title, "page": page}
        url = urljoin(self.url_prefix, "search_title")
        r = requests.post(url, json=json)
        return r.status_code

    def search_author_in_store(self, author: str, store_id: str, page: int) -> int:
        json = {"author": author, "store_id": store_id, "page": page}
        url = urljoin(self.url_prefix, "search_author_in_store")
        r = requests.post(url, json=json)
        return r.status_code

    def search_book_intro_in_store(self, book_intro: str, store_id: str, page: int) -> int:
        json = {"book_intro": book_intro, "store_id": store_id, "page": page}
        url = urljoin(self.url_prefix, "search_book_intro_in_store")
        r = requests.post(url, json=json)
        return r.status_code

    def search_tags_in_store(self, tags: str, store_id: str, page: int) -> int:
        json = {"tags": tags, "store_id": store_id, "page": page}
        url = urljoin(self.url_prefix, "search_tags_in_store")
        r = requests.post(url, json=json)
        return r.status_code

    def search_title_in_store(self, title: str, store_id: str, page: int) -> int:
        json = {"title": title, "store_id": store_id, "page": page}
        url = urljoin(self.url_prefix, "search_title_in_store")
        r = requests.post(url, json=json)
        return r.status_code
