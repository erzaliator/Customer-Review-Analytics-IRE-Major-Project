#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os, sys, re

from lxml.html.clean import clean_html
from lxml.html.soupparser import fromstring

import logging


logger = logging.getLogger('crawler.' + __name__)
logger.setLevel(logging.DEBUG)

def santitize_html(html):
    html = clean_html(html)
    return html

def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)


def remove_script(data):
    p = re.compile(r'<script .*?>.*?</script>')
    return p.sub(' ', data)

def remove_style(data):
    p = re.compile(r'<style .*?>.*?</style>')
    return p.sub(' ', data)

def remove_cont_withtags(data):
    style_reg = re.compile(r"\<style.*?\<\/style\>")
    data = style_reg.sub("", data)

    li_reg = re.compile(r"\<li.*?\<\/li\>")
    data = li_reg.sub("", data)

    table_reg = re.compile(r"\<table.*?\<\/table\>")
    data = table_reg.sub("", data)

    td_reg = re.compile(r"\<td.*?\<\/td\>")
    data = td_reg.sub("", data)
    
    div_reg = re.compile(r"\<div.*?\<\/div\>")
    data = div_reg.sub("", data)

    ul_reg = re.compile(r"\<ul.*?\<\/ul\>")
    data = ul_reg.sub("", data)

    a_reg = re.compile(r"\<a.*?\>.*?\<\/a\>")
    data = a_reg.sub("", data)


    data = re.sub(r"\<\/div\>", "", data)
    data = re.sub(r"\<div.*?\>.*?\<", "", data)
    data = re.sub(r"\<\/table\>", "", data)
    data = re.sub(r"\<\/td\>", "", data)
    data = re.sub(r"\<\/tr\>", "", data)

    data = re.sub(r"\<br \/\>", "\n", data)
    data = re.sub(r"[\s]+?\<", " ", data)
    data = re.sub(r"\n+", "\n", data)
    return data
