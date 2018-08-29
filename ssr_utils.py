#!/usr/bin/env python

import base64
import re


def _base64decode(cipher=''):
    if not cipher:
        return ''
    # Padding and decoding
    cipher = cipher + '=' * (4 - len(cipher) % 4)
    plain = base64.urlsafe_b64decode(cipher)
    return plain


def _base64encode(pain=''):
    if not pain:
        return ''
    # Encoding and remove padding
    cipher = base64.urlsafe_b64encode(pain)
    cipher = cipher.rstrip('=')
    return cipher


def url2json(url=''):
    """Convert the SSR URL to JSON."""
    # The url must start with 'ssr://'
    if not url.find('ssr://') == 0:
        return None

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


def json2url(jdata={}):
    # Check keywords and compose the paintext
    for keyword in ('server', 'port', 'protocol', 'method', 'obfs', 'password'):
        if keyword not in jdata:
            print '%s is missing in the json code.' % keyword
            return None

    text = ':'.join(
        map(lambda x: jdata[x], ('server', 'port', 'protocol', 'method', 'obfs')))
    text = text + ':' + _base64encode(jdata['password'])

    print text
    exit()

    for param in ('protoparam', 'obfsparam', 'remarks', 'group', 'udpport', 'uot'):
    pass






if __name__ == '__main__':

    j = url2json(url)
    u = json2url(j)
    print u
    exit(0)
