from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import logging
from collections import deque
# https://docs.python.org/2/library/collections.html#collections.deque
import json
import ast
import signal
import sys

# Citation:
# 1.http://www.bogotobogo.com/python/python_graph_data_structures.php
# 2.https://docs.python.org/3/tutorial/datastructures.html
# 3.https://zhuanlan.zhihu.com/p/33929261
# 4.https://zhuanlan.zhihu.com/p/28759710
# 5.https://zhuanlan.zhihu.com/p/29933456


def getagefromstring(agespanstring):
    return agespanstring[-3:-1]

redditFile = urlopen("https://en.wikipedia.org/wiki/Morgan_Freeman")
redditHtml = redditFile.read()
redditFile.close()

soup = BeautifulSoup(redditHtml, 'html.parser')
#print(soup)
spans = soup.find_all('span', attrs={'class': 'noprint ForceAgeToShow'})
for span in spans:
    print (getagefromstring(span.get_text()))