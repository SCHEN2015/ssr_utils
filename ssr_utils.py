#!/usr/bin/env python

import base64
import re


def _base64decode(cipher=''):
    if not cipher:
        return ''
    # Padding and decoding
    data = cipher + '=' * (4 - len(cipher) % 4)
    plain = base64.urlsafe_b64decode(data)
    return plain


def url2json(url=''):
    """Convert the SSR URL to JSON."""
    # The url must start with 'ssr://'
    if not url.find('ssr://') == 0:
        return 1

    # Decode the payload
    payload = url[6:]
    text = _base64decode(payload)

    # Parse the SSR keywords
    ssr_regex = re.compile(r'(.*)\:(\d+)\:(.*)\:(.*)\:(.*)\:(.*)/\?(.*)')
    (server, port, protocol, method, obfs,
     password_base64, params_base64) = ssr_regex.findall(text)[0]

    jdata = {'server': server, 'port': port,
             'protocol': protocol, 'method': method, 'obfs': obfs,
             'password': _base64decode(password_base64)}

    # Deal with additional parameters
    for param in params_base64.split('&'):
        (key, value) = param.split('=')
        if key in ('protoparam', 'obfsparam', 'remarks', 'group'):
            value = _base64decode(value)
        jdata[key] = value

    return jdata


def json2url():
    pass


def json2url():
    pass


if __name__ == '__main__':
    url2json(url=url)
    exit(0)
