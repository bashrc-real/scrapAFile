import file_scraper
import concurrent
from concurrent import futures
import threading
import argparse

DEFAULT_NUMBER_OF_THREADS = 8

if __name__ == "__main__":
    pool = concurrent.futures.thread.ThreadPoolExecutor(max_workers=DEFAULT_NUMBER_OF_THREADS)
    parser = argparse.ArgumentParser(description='Download the files from the urls provided by the input path')
    parser.add_argument('-path', type=str, help="path to the input file with list of urls", required=True)
    parser.add_argument('-outputPath', type=str, help="output path for downloading the files", required = True)
    arguments = parser.parse_args()
    f = open(arguments.path)
    for item in (result for result in pool.map(lambda x : file_scraper.DownloadToPath(x, arguments.outputPath), (line.strip() for line in f)) if result != None):
        pass
