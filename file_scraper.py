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
import HashRabinKarp
from HashRabinKarp import HashString
from threading import Thread
import posixpath
from urllib.parse import urlparse
DEFAULT_MAX_DEPTH = 10
DEFAULT_NUMBER_OF_THREADS = 4
VisitedURL = HashString()
keywords = []
q = deque()
default_path = "./url.txt"
global output_path
global output    
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
      response = urllib.request.urlopen(req)
      if response.info()['Content-Type'].find("text/html") != -1:
        return response
  except Exception as detail:
      print(detail)
      print("TryReadUrl:Couldn't load file:"+url)
      
def DownloadPdf(url):
  global output_path
  if not output_path or (len(output_path) == 0):
    return
  try:
    path = urllib.parse.urlsplit(url).path.split('/')[-1]
    filename = posixpath.basename(path)
    local_filename, headers = urllib.request.urlretrieve(url, output_path + "\\"+filename)
  except Exception as detail:
    print(detail)
  return
cntr = 0
def do_parsing(data):
    try:
      print(threading.current_thread())
      url, depth = data
      global q
      global VisitedURL
      global keywords
      global output
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
      global cntr
      pageData = str(fr.read())
      cntr = cntr+1
      idx = 0
      urls = []
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
              if not VisitedURL.query(nexturl):
                VisitedURL.add(nexturl)
                output.write(nexturl+"\n")
                Thread(target = DownloadPdf, args = (nexturl,)).start()
                continue
          if nexturl.find("http")!=0:
            nexturl = baseURL+nexturl
          if not VisitedURL.query(nexturl):
            VisitedURL.add(nexturl)
            urls.append([nexturl,depth+1])
      return urls
    except Exception as detail:
       print(detail)
       pass       
def crawl_from_url(pool):
  global DEFAULT_NUMBER_OF_THREADS
  global q
  global output
  while len(q):
    urlsToMap = []
    number_of_urls = min(len(q), DEFAULT_NUMBER_OF_THREADS)
    for i in range(0, number_of_urls):
      global DEFAULT_MAX_DEPTH
      url, depth = q.popleft()
      if depth < DEFAULT_MAX_DEPTH:
        urlsToMap.append((url,depth))
    for item in (result for result in pool.map(do_parsing, urlsToMap) if result != None):
      q.extend(item)
    output.flush()
    os.fsync(output.fileno())       
def main(arguments):
    global DEFAULT_NUMBER_OF_THREADS
    global keywords
    global VisitedURL
    global output
    global default_path
    global DEFAULT_MAX_DEPTH
    global output_path
    parser = argparse.ArgumentParser(description='Scrape the web from a seed url to find the documents matching particular keyword')
    parser.add_argument('keywords', metavar='N', type=str, nargs='+',help='keywords to look for')
    parser.add_argument('-S', type=str,required=True, help="seed url")
    parser.add_argument('-t', type=int, help="number of threads, default = " + str(DEFAULT_NUMBER_OF_THREADS), default=DEFAULT_NUMBER_OF_THREADS)
    parser.add_argument('-path', type=str, help="path to the output file , default = "+default_path, default=default_path)
    parser.add_argument('-depth', type=int, help="depth to which need to visit , default = "+str(DEFAULT_MAX_DEPTH), default=DEFAULT_MAX_DEPTH)
    parser.add_argument('-output', type=str, help="Download folder path , default = ./", default="")
    arguments = parser.parse_args()
    DEFAULT_NUMBER_OF_THREADS = arguments.t
    keywords = arguments.keywords
    DEFAULT_MAX_DEPTH = arguments.depth
    q.append((arguments.S, 0))
    pool = concurrent.futures.thread.ThreadPoolExecutor(max_workers=DEFAULT_NUMBER_OF_THREADS)
    default_path = arguments.path
    output_path = arguments.output
    output = open(default_path, 'w')
    crawl_from_url(pool)
    
if __name__ == "__main__":
    main(sys.argv)

