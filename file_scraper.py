#!/usr/bin/env python
import urllib
import urllib.request
import re
import sys
import os
import collections
import random
from collections import deque
import argparse
import multiprocessing
import concurrent
from concurrent import futures
import threading
DEFAULT_MAX_DEPTH = 10
DEFAULT_NUMBER_OF_THREADS = 4
VisitedURL = set()
keywords = []
q = deque()
    
def TryReadUrl(url):
  try:
      user_agents = ["Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; Avant Browser; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)"
      ,"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 3.5.21022; InfoPath.2)"
      ,"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Avant Browser; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30618; InfoPath.1)"
      ,"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.4; ,Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; chromeframe; Avant Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; InfoPath.1; .NET CLR 3.0.4506."
      ,"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB5; Avant Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
      ,"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Avant Browser; Avant Browser; .NET CLR 2.0.50727)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT; Avant Browser; Avant Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; Avant Browser)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; Avant Browser; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; ,Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 3.5.21022; InfoPath.2)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; GTB6.3; ,Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 3.5.21022; InfoPath.2)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Avant Browser; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30618; InfoPath.1)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; ,Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Avant Browser; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322; InfoPath.2)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Avant Browser; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30618; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Avant Browser; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; Tablet PC 2.0)"
      ,"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Avant Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727), Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"]
      user_agent = user_agents[random.randint(1, len(user_agents)) - 1]
      header={'User-Agent':user_agent}
      req = urllib.request.Request(url, headers=header)
      return urllib.request.urlopen(req)

  except Exception as detail:
      print(detail)
      print("TryReadUrl:Couldn't load file:"+url)
      return ""


def do_parsing(data):
    print(threading.current_thread())
    url, depth = data
    global q
    global VisitedURL
    global keywords
    idx = url.find("://")
    assert idx!=-1
    endidx = url.find("/",idx+len("://"))
    if endidx!=-1:
      baseURL=url[0:endidx+1]
    else:
      baseURL = url
    fr = TryReadUrl(url)
    if  not fr:
      return
    pageData = str(fr.read())
    for key in keywords:
      if pageData.find(key):
        #print(url)
        break
    idx = 0
    while idx!=-1:
      patToSearch = "href=\""
      idx = pageData.find(patToSearch,idx)
      if idx!=-1:
        idx = idx+ len(patToSearch)
        endidx = pageData.find("\"",idx)
        nexturl = pageData[idx:endidx]
        idx = endidx+1
        for key in keywords:
          key = "." + key
          innerIdx = nexturl.find(key);
          outerIdx = nexturl.rfind("http",0,innerIdx)
          if innerIdx !=-1 and outerIdx != -1:
            nexturl = nexturl[outerIdx:innerIdx] +key
            if nexturl not in VisitedURL:
              VisitedURL.update(nexturl)
              print(nexturl+"========\n")
              continue
        if nexturl.find("http")!=0:
          nexturl = baseURL+nexturl
        if nexturl not in VisitedURL:
          VisitedURL.update(nexturl)
          q.extend([[nexturl,depth+1]])
        if len(VisitedURL) > 100000:
          VisitedURL.clear()

def crawl_from_url(pool):
  global DEFAULT_NUMBER_OF_THREADS
  global q
  while len(q):
    urlsToMap = []
    number_of_urls = min(len(q), DEFAULT_NUMBER_OF_THREADS)
    for i in range(0, number_of_urls):
      global DEFAULT_MAX_DEPTH
      url, depth = q.popleft()
      if depth < DEFAULT_MAX_DEPTH:
        urlsToMap.append((url,depth))
    for result in pool.map(do_parsing, urlsToMap):
      result = result
           
def main(arguments):
    global DEFAULT_NUMBER_OF_THREADS
    global keywords
    global VisitedURL
    parser = argparse.ArgumentParser(description='Scrape the web from a seed url to find the documents matching particular keyword')
    parser.add_argument('keywords', metavar='N', type=str, nargs='+',help='keywords to look for')
    parser.add_argument('-S', type=str,required=True, help="seed url")
    parser.add_argument('-t', type=int, help="number of threads, default = " + str(DEFAULT_NUMBER_OF_THREADS), default=DEFAULT_NUMBER_OF_THREADS)
    arguments = parser.parse_args()
    DEFAULT_NUMBER_OF_THREADS = arguments.t
    keywords = arguments.keywords
    q.append((arguments.S, 0))
    pool = concurrent.futures.thread.ThreadPoolExecutor(max_workers=DEFAULT_NUMBER_OF_THREADS)
    crawl_from_url(pool)
    
if __name__ == "__main__":
    main(sys.argv)

