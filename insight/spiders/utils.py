import os
import re
import time
from copy import deepcopy
from csv import DictReader
from html import unescape

import pandas as pd


def clean(text):
    text = unescape(text or '')
    for c in ['\r\n', '\n\r', u'\n', u'\r', u'\t', u'\xa0']:
        text = text.replace(c, ' ')
    return re.sub(' +', ' ', text).strip()


def clean_all(seq, sep=", "):
    return f"{sep}".join(clean(e) for e in seq if clean(e))


def retry_invalid_response(callback):
    def wrapper(spider, response):
        if response.status >= 400:
            if response.status == 404:
                print('Page not 404')
                return spider.get_next_request(response)

            retry_times = response.meta.get('retry_times', 0)
            if retry_times < 3:
                time.sleep(5)
                response.meta['retry_times'] = retry_times + 1
                return response.request.replace(dont_filter=True, meta=response.meta)

            print("Dropped after 3 retries. url: {}".format(response.url))
            response.meta.pop('retry_times', None)
            return spider.get_next_request(response)

        return callback(spider, response)

    return wrapper


def get_jl_records(filename):
    if not os.path.exists(filename):
        return []
    # return json.loads("[" + ",".join(open(filename, encoding='utf-8').readlines()) + "]" or '[]')
    return list(pd.read_json(filename, lines=True).fillna('').to_dict(orient='index').values())


def get_csv_records(filename):
    return [dict(r) for r in DictReader(open(filename, encoding='utf-8')) if r]
