#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests

# For supporting socks4/5 proxy;
# It is a fork of the Requests module, with additional SOCKS support
import requesocks
import lxml.etree
from urllib2 import HTTPError
from bs4 import BeautifulSoup
from StringIO import StringIO

import logging

from crawler.core.utils import *

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

lxml_parser = lxml.etree.HTMLParser()


session = requesocks.session()


def parse_lxml(content):
    """ from gist: https://gist.github.com/kanzure/5385691

    A possible safer way to parse HTML content with lxml. This will
    presumably not break on poorly formatted HTML.
    """

    if not isinstance(content, StringIO):
        if not isinstance(content, str) and not isinstance(content,
                                                           unicode):
            raise Exception("input content must be a str or StringIO"
                            "instead of " + str(type(content)))
        content = StringIO(content)

    lxml_tree = lxml.etree.parse(content, lxml_parser)
    return lxml_tree


def parse_soup(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        return soup
    except HTTPError, e:
        logger.error("%d: %s" % (e.code, e.msg))
        return

def get_data(url, proxies=None):
    data = requests.get(url).read()
    return data

def get_response(url, proxies=None):
    try:
        if proxies:
            if url.startswith('http:') and 'http' in proxies:
                prox = proxies['http']
                if prox.startswith('socks'):
                    session.proxies = proxies
                    r = session.get(url)
                else:  # http proxy
                    r = requests.get(url, proxies = proxies)
            elif url.startswith('https:') and 'https' in proxies:
                prox = proxies['https']
                if prox.startswith('socks'):
                    session.proxies = proxies
                    r = session.get(url)
                else:
                    r = requests.get(url, proxies = proxies)
            else:  # ohter types of requests, e.g., ftp
                r = requests.get(url, proxies = proxies)

        else:  # without proxy
            r = requests.get(url)
    except ValueError as e:
        logger.error('Url is invalid: %s' % url)
        return
    except requests.exceptions.ConnectionError:
        logger.error("Error connecting to %s" % url)
        return

    if r.status_code != 200:
        logger.error('Status code is %d on %s' % (r.status_code, url))
        return

    return r.content


def get_soup(url, proxies=None):
    html = get_response(url, proxies)
    return parse_soup(html)
