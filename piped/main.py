import os
import time
from urllib.parse import urlparse

import httpx

HEADERS = {"User-Agent": "@NoPlagiarism / frontend-instances-scraper"}

session = httpx.Client(headers=HEADERS)


def get_api_urls():
    return session.get("https://piped-instances.kavin.rocks/").json()

def get_frontend_from_api_url(api_url):
    try:
        return session.get(api_url).headers.get("location")
    except Exception:
        time.sleep(2)
        try:
            return session.get(api_url).headers.get("location")
        except Exception:
            return None

def sort_filter_list(domains):
    return list(sorted(tuple(filter(lambda url: url not in (False, "", None, b"", "b''"), domains))))

def save_list_as_txt(obj):
    to_save = "\n".join(obj)
    with open(os.path.join(os.path.dirname(__file__), "clearnet.txt"), mode="w+", encoding="utf-8") as f:
        f.write(to_save)

def get_domain_from_url(url):
    parsed = urlparse(url)
    return str(parsed.netloc)

def sync_main():
    apis = get_api_urls()
    res_dict = dict()
    for x in apis:
        res_dict[x["api_url"]] = get_frontend_from_api_url(x["api_url"])
        time.sleep(1)
    res_list = sort_filter_list(list(map(get_domain_from_url, res_dict.values())))
    save_list_as_txt(res_list)


if __name__ == "__main__":
    sync_main()
