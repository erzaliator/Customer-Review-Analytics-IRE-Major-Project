#!/usr/bin/env python
#-*- coding: utf-8 -*-
from crawler.core.base import *

import time
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def amazon_prd_ids(search_query, proxies=None, mx=500):
    prd_ids = []
    search_query = search_query.replace(" ", "+")

    base_search_url = "http://www.amazon.com/s/ref=sr_pg_2?page=%s&keywords="+search_query+"&ie=UTF8" 
    pagn = "1"
    while True:
        prd_search_url = base_search_url % pagn
        logger.info('fetch ids from %s' % prd_search_url)

        print "sleeping..."
        time.sleep(2)
        print "woke up.."
        try:
            soup = get_soup(prd_search_url, proxies)
        except:
            continue
        if not soup:
            continue
        
        res = soup.find_all("li", class_="s-result-item celwidget")
        for each in res:
            prd_ids.append(each['data-asin'])

        if soup.find_all("span", class_="pagnRA") and len(prd_ids) < mx:
            pagn = str(int(pagn) + 1)
        else:
            break
    return prd_ids




def amazon_reviews(prd_id, proxies=None, mx=1000):
    prd_reviews = []
    base_review_url = "http://www.amazon.com/product-reviews/" + prd_id + "/?ie=UTF8&showViewpoints=0&pageNumber=" + "%s" + "&sortBy=bySubmissionDateDescending" 
    pagn = "1"
    while True:
        prd_review_url = base_review_url % pagn
        logger.info('fetch reviews from %s' % prd_review_url)

        print "sleeping..."
        time.sleep(2)
        print "woke up.."
        revs_html = get_response(prd_review_url, proxies)
        if not revs_html:
            continue
        reviews, nxt = extract_reviews(unicode(str(revs_html),
                                          errors="ignore"), prd_id)

        if reviews:
            prd_reviews.extend(reviews)
        if nxt == 1 and len(prd_reviews) < mx:
            print len(prd_reviews)
            pagn = str(int(pagn) + 1)
        else:
            break
    return prd_reviews

def extract_reviews(data, pid):
    reviews = []

    data = remove_extra_spaces(data)
    data = remove_script(data)
    data = remove_style(data)

    soup = BeautifulSoup(data, "html.parser")
    #model_match = re.search(r'product\-reviews/([A-Z0-9]+)/ref\=cm_cr_pr', str)
    revs_soup = soup.find(id="cm_cr-review_list")
    rev_list = revs_soup.find_all("div", class_="a-section review")
    for rev in rev_list:
        text = rev.find_all("div", class_="a-row review-data")[0].find_all("span")[0].text 
        rating = rev.find_all("span", class_="a-icon-alt")[0].text
        rating = rating.split(' ')[0]
        reviews.append((text, rating))
    nxt = 0
    if soup.find("li", class_="a-last") and soup.find("li", class_="a-last").find("a"):
        nxt = 1
    return (reviews, nxt)


