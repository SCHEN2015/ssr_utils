#!/usr/bin/env python

import requests
import ssr_utils


class RSS_Reader():
    def __init__(self, url):
        self.rss_content = self.load_rss(url)

    def load_rss(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.content
        else:
            return ''



if __name__ == '__main__':
    rss_url = raw_input('RSS? ')
    reader = RSS_Reader(rss_url)
    rss = reader.rss_content
    lines=ssr_utils._base64decode(rss)
    jdata_list = []
    for line in lines.splitlines():
        print line
        jdata_list.append(ssr_utils.url2json(line))
    print jdata_list
