import json
from os import path
import re
import time

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.error


def get_soup(url):

    success = False
    sleep_time = 1
    max_sleep_time = 60 * 5

    req, html_page = None, None
    while not success:
        try:
            req = Request(url)
            html_page = urlopen(req)
            success = True
        except urllib.error.HTTPError as e:
            print(f'error {e.code}')
            if 500 <= e.code <= 599 and sleep_time < max_sleep_time:
                print(f'server error; sleep {sleep_time} seconds')
                time.sleep(sleep_time)
                sleep_time *= 2
            else:
                raise e

    soup = BeautifulSoup(html_page, 'html.parser')
    return soup


def get_soup_text(soup: BeautifulSoup, search_str: str, one=False):
    if one:
        return format_str(soup.select_one(search_str).text)
    else:
        return list(map(lambda x: format_str(x.text), soup.select(search_str)))


def append_to_json(json_file, new_data):
    if path.isfile(json_file):
        with open(json_file, 'r') as fp:
            all_data = json.load(fp)
    else:
        all_data = []

    all_data.append(new_data)

    with open(json_file, 'w') as fp:
        json.dump(all_data, fp, indent=4, separators=(',', ': '))


def format_str(s):
    return re.sub("[\n\t\r]+", '|', s)


def remove_symbols_str(s):
    return re.sub("[|+:,.]", '', s)


def argmax(d):
    max_val = None
    max_key = None

    for key, val in d.items():
        if max_val is None or val > max_val:
            max_val = val
            max_key = key

    return max_key
