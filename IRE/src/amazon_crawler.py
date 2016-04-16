#!/usr/bin/env python
#-*- coding: utf-8 -*-
from crawler.contrib.amazon import *
import sys
from optparse import OptionParser
import os
import time
from pprint import pprint
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


usage = "usage %prog [options] arg"
parser = OptionParser(usage=usage)
parser.add_option('-s', "--seed", dest="initial search url",
                  help="the initial search url")
parser.add_option("-o", "--output", dest="output_dir",
              help="write out to DIR")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

(options, args) = parser.parse_args()

def main():

    proxies = {'http': 'http://proxy.iiit.ac.in:8080', 'https': 'https://proxy.iiit.ac.in:8080'}
    reviews = {}
    q = sys.argv[1]
    n = 2
    mx = 2
    prd_ids = amazon_prd_ids(q, proxies=proxies, mx=int(n))
    cnt = 0
    for each in prd_ids:
        reviews[each] = amazon_reviews(each, proxies=proxies, mx=int(mx))
        cnt+=1
        if cnt >= int(n):
            break
    with open(sys.argv[2], "w") as fout:
	pprint(reviews, stream=fout)
    print "Done :D!!!"
   
if __name__ == "__main__":
    main()