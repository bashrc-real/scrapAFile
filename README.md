# scrapAFile
A basic multithreaded configurable web crawler in python for crawling files of a particular type
Currently under beta. For example to get a list of pdf's from [[this]](http://programming-motherfucker.com/become.html "this") awesome resource:
````
$python file_scraper.py pdf -S <list of space seperated urls> -t 4 -depth 3 -output <folder to download files>
````
The list of urls can be given as space seperated urls.
Note: This script is not honoring robots.txt right now and isn't entirely honest about user agent string either. I will open an issue for that.
