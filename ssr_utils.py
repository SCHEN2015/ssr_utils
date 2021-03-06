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
    """Convert the JSON to URL."""
    # Check the SSR keywords
    for keyword in ('server', 'port', 'protocol', 'method', 'obfs', 'password'):
        if keyword not in jdata:
            print 'keyword "%s" is missing in the json block.' % keyword
            return None

    # Join SSR keywords as paintext
    text_kw = ':'.join(
        map(lambda x: jdata[x], ('server', 'port', 'protocol', 'method', 'obfs')))
    text_kw = text_kw + ':' + _base64encode(jdata['password'])

    # Join additional parameters as paintext
    text_pm = ''
    for key in ('protoparam', 'obfsparam', 'remarks', 'group'):
        if key in jdata:
            text_pm = text_pm + '&' + key + '=' + _base64encode(jdata[key])
        else:
            text_pm = text_pm + '&' + key + '='
    for key in ('udpport', 'uot'):
        if key in jdata:
            text_pm = text_pm + '&' + key + '=' + jdata[key]
        else:
            text_pm = text_pm + '&' + key + '=0'
    text_pm = text_pm.lstrip('&')

    # Combine as the paintext
    text = text_kw + '/?' + text_pm

    # Encoding as payload
    payload = _base64encode(text)

    # Compose the URL
    url = 'ssr://' + payload

    return(url)


def rss2urls():
    pass


def urls2rss():
    pass


def urls2jsons(url_list):
    """Covert a list of SSR URL to a list of JSON data."""
    if not isinstance(url_list, (list, tuple)):
        return None

    jdata_list = []
    for url in url_list:
        jdata = url2json(url)
        jdata_list.append(jdata)
    return jdata_list


def jsons2urls(jdata_list):
    """Covert a list of SSR JSON data to a list of URL."""
    if not isinstance(jdata_list, (list, tuple)):
        return None

    url_list = []
    for jdata in jdata_list:
        url = json2url(jdata)
        url_list.append(url)
    return url_list


def _unit_test():
    # format:
    # ssr://server:port:protocol:method:obfs:password_base64/?params_base64
    # params_base64:
    # obfsparam=obfsparam_base64&protoparam=protoparam_base64&remarks=remarks_base64&group=group_base64&udpport=udpport&uot=uot[&...]

    url = 'ssr://c3NyLmV4YW1wbGUuY29tOjg4ODg6YXV0aF9jaGFpbl9hOmNoYWNoYTIwOnRsczEuMl90aWNrZXRfYXV0aDpiWGx3WVhOem\
QyOXlaQS8_cHJvdG9wYXJhbT0mb2Jmc3BhcmFtPSZyZW1hcmtzPVRWbFRVMUkmZ3JvdXA9NVp1OTZabUY1WXFnNllDZjU3cV82TGV2JnVkcHBvc\
nQ9MCZ1b3Q9MA'
    jdata = {'udpport': '0', 'protocol': 'auth_chain_a', 'uot': '0', 'server': 'ssr.example.com',
             'port': '8888', 'obfs': 'tls1.2_ticket_auth', 'protoparam': '',
             'remarks': 'MYSSR', 'obfsparam': '', 'password': 'mypassword', 'method': 'chacha20',
             'group': '\xe5\x9b\xbd\xe9\x99\x85\xe5\x8a\xa0\xe9\x80\x9f\xe7\xba\xbf\xe8\xb7\xaf'}

    if jdata == url2json(url) and url == json2url(jdata):
        print 'UnitTest(1): PASS'
    else:
        print 'UnitTest(1): FAIL'

    if [jdata, jdata] == urls2jsons([url, url]) and [url, url] == jsons2urls([jdata, jdata]):
        print 'UnitTest(2): PASS'
    else:
        print 'UnitTest(2): FAIL'


if __name__ == '__main__':
    _unit_test()
