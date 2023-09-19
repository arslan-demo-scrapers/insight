# -*- coding: utf-8 -*-
import json
import os
from copy import deepcopy

from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess

from utils import retry_invalid_response, clean, get_csv_records


class InsightSpider(Spider):
    name = "insight_spider"
    output_file_dir = "../output"
    output_file_path = f'{output_file_dir}/all_categories_products.jl'
    keywords_file_path = "keywords.csv"
    base_url = "https://www.insight.com"
    product_api = "https://www.insight.com/api/product-management/product"
    product_url_t = "https://www.insight.com/en_US/shop/product/{mfr_no}/{mfr_name}/{mfr_no}/{title_slug}"

    handle_httpstatus_list = [
        400, 401, 402, 403, 404, 405, 406, 407, 409,
        500, 501, 502, 503, 504, 505, 506, 507, 509,
    ]

    feeds = {
        output_file_path: {
            'format': 'jl',
            'encoding': 'utf8',
            'store_empty': False,
            # 'fields': [],
            'indent': 4,
            'overwrite': True,
        },
    }

    custom_settings = {
        # 'FEEDS': feeds,
        'CONCURRENT_REQUESTS': 1,
        # "ROTATING_PROXY_LIST_PATH": 'proxies.txt',
        "DOWNLOADER_MIDDLEWARES": {
            # 'insight.insight.middlewares.InsightDownloaderMiddleware': 543,
            # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        },
    }

    meta = {
        'handle_httpstatus_list': handle_httpstatus_list,
    }

    headers = {
        'authority': 'www.insight.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': 'Bearer null',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.insight.com',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    product_body = {
        'locale': 'en_US',
        'materialId': '',  # '5D1-00001',
        'salesOrg': '2400',
        'includeSpecifications': True,
        'includeVariants': True,
    }

    cookies = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        yield Request(self.base_url, callback=self.parse, headers=self.headers, cookies=self.cookies)

    @retry_invalid_response
    def parse(self, response):
        for rec in self.get_input_meta()[:]:
            url = rec['category_url'].format(start_offset=0)

            meta = deepcopy(self.meta)
            meta['item'] = {'meta': rec}

            headers = deepcopy(self.headers)
            headers['referer'] = url

            self.delete_file(self.get_abs_filepath(rec['filepath']))
            yield Request(url=url, callback=self.parse_listings, headers=headers, meta=meta, )

    def parse_listings(self, response):
        data = json.loads(response.text)

        for prod in data['products'][:]:
            item = deepcopy(response.meta['item'])
            item['listings_details'] = prod

            meta = deepcopy(self.meta)
            meta['item'] = item

            req_body = deepcopy(self.product_body)
            req_body['materialId'] = prod['materialId']

            yield Request(url=self.product_api, callback=self.parse_product, method='POST',
                          headers=self.headers, body=json.dumps(req_body), meta=meta)

        if data['pages'] > data['pageNumber']:
            url = response.meta['item']['meta']['category_url'].format(start_offset=(data['pageNumber']) * 100)
            yield Request(url=url, callback=self.parse_listings, headers=self.headers, meta=response.meta)

    def parse_product(self, response):
        try:
            data = json.loads(response.text)
            specifications = self.get_specifications(data)
            product = data['product']

            item = response.meta['item']
            item['Full Product Name'] = product['descriptions']['shortDescription']
            item['MFR Name'] = product['manufacturer']['name']
            item['MFR #'] = product['manufacturer']['partNumber']
            item['Price'] = product['price']['listPrice']
            item['Sale Price'] = product['price'].get('insightPrice') or product['price']['listPrice']
            item['Link'] = self.get_product_link(item)
            item.update(specifications)
            return self.write_to_jl(item)
        except Exception as p_err:
            print(p_err)
            print(response.meta['item']['listings_details'])
            a = 0

    def get_specifications(self, data):
        # return {r['label']: r['value'] for specs in data['specifications'] for r in specs['details']}
        specifications = {}

        p_specs = {}
        specs_count = 1

        try:
            for specs in data['specifications']:
                for r in specs['details']:
                    if r['label'] not in specifications:
                        specifications[r['label']] = r['value']
                        p_specs[f"Specs {specs_count}"] = f"{r['label']}: {r['value']}"
                        specs_count += 1
                    else:
                        for i in range(2, 10):
                            if f"{r['label']} {i}" not in specifications:
                                specifications[f"{r['label']} {i}"] = r['value']
                                break
        except Exception as specs_err:
            print(specs_err)

        p_specs.update(specifications)
        return p_specs

    def get_abs_filepath(self, filename):
        return f"{self.output_file_dir.rstrip('/')}/{filename}".replace('.csv', '.jl')

    def get_product_link(self, item):
        slug = clean("".join(c for c in item['Full Product Name'] if c.isalnum() or c.isspace())).replace(' ', '-')
        url = self.product_url_t.format(mfr_no=item['MFR #'], mfr_name=item['MFR Name'], title_slug=slug)
        return f'{url.rstrip("/")}/'

    def get_meta(self, item):
        meta = deepcopy(self.meta)
        meta['item'] = {'meta': item}
        return meta

    def write_to_jl(self, item):
        with open(self.get_abs_filepath(item['meta']['filepath']), 'a+') as fp:
            json.dump(item, fp)
            fp.write('\n')
        return item

    def get_jl_writer(self, filepath):
        if not os.path.exists(filepath):
            return open(filepath, mode='w', encoding='utf-8')
        return open(filepath, mode='a', encoding='utf-8')

    def delete_file(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    def get_input_meta(self):
        listing_urls_meta = []

        for i, r in enumerate(get_csv_records('../input/input_category_urls_meta.csv'), start=1):
            if not r:
                continue
            url = f"https://www.insight.com/api/product-search/search?{r['Link'].split('.html?')[-1]}"
            url_t = url.replace('start=0', 'start={start_offset}')

            r.pop('Number of records', '')
            r["category_url"] = url_t
            r["filepath"] = f"{r['Insight Category'].strip()}_{i}.csv"

            listing_urls_meta.append(r)

        return listing_urls_meta


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(InsightSpider)
    process.start()
