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
import math
import random


def ismovie(soup):
    """
    judge whether current soup is from a movie url
    :param soup:
    :return:
    """
    ans=soup.find_all('th', text='Cinematography')
    if(len(ans)>0):
        return True;

    return False

def isactor(soup):
    """
    judge whether current soup is from a actor url
    :param soup:
    """
    ans=soup.find_all("td", {'class': 'role'})
    if(len(ans)>0):
        for elem in ans:
            string=elem.get_text()
            if "Actress" in string:
                return True
            if "Actor" in string:
                return True

    else:
        return False


def get_starring_actors(moviesoup):
    '''
    given a movie page, return a list of actors performing in it
    :param moviesoup:
    :return:
    '''
    actors_list=[]
    info = moviesoup.find_all('span', {'class': 'mw-headline', 'id': 'Cast'})
    #If find_all() can’t find anything, it returns an empty list. If find() can’t find anything, it returns None:
    if len(info)==0:
        return actors_list
    temp = info[0].find_next('ul')
    urls = temp.find_all('a')
    for link in urls:
        actors_list.append(link.get('href')[6:])
    return actors_list#[:4]


def get_movie_gross(moviesoup):
    '''
    given a movie page, return how much it earned
    :param moviesoup:
    :return:
    '''
    gross = moviesoup.find_all('th', text="Box office")
    if len(gross) > 0:
        moneystring=gross[0].find_next('td').get_text()
        money=convertstrtoint(moneystring)
        return money
    else:
        logging.warning('Gross not found, assume $1000000.0')
        return 1000000.0

#citation Rika
def convertstrtoint(moneystr):
    data = re.sub(r'[(\xc2|\xa0|+|=|:|$|,)]', '', moneystr)
    digits = re.findall(r'([\d\.\d]+)', data)
    #print(digits[0])
    try:
        digit = float(digits[0])
    except ValueError:
        digit = 10000
        print("bad value")
    if 'hundred' in data:
        num = digit * 100
    elif 'thousand' in data:
        num = digit * 1000
    elif 'million' in data:
        num = digit * 1000000
    elif 'billion' in data:
        num = digit * 1000000000
    else:
        num = 100000
    return num


def get_movie_year(moviesoup):
    release_div = moviesoup.find('div', text='Release date')
    if release_div is not None:
        date_span = release_div.find_next('span', {'class': 'bday dtstart published updated'})
        if date_span is not None:
            try:
                result = int(date_span.get_text()[:4])
            except ValueError:
                result = 2020
            return result
        else:
            logging.warning('release date not found, assume 2020')
            return 2018
    else:
        logging.warning('release date not found, assume 2020')
        return 2020


def get_actor_or_movie_name(soup):
    name = soup.find_all('title')
    if len(name)>0:
        return name[0].get_text()[:-12]
    else:
        logging.warning('this is not actor or movie soup')
        return "Steve Jobs"


def get_actor_age(actorsoup):
    age_span = actorsoup.find('span', {'class': re.compile('noprint ForceAgeToShow')})
    bday_span = actorsoup.find('span', {'class': re.compile('bday')})
    dday_span = actorsoup.find('span', {'class': re.compile('dday')})
    if age_span is not None:
        return int(age_span.get_text()[-3:-1])
    elif bday_span is not None and dday_span is None:
        bday_val = int(bday_span.get_text()[:4])
        return 2017 - bday_val
    elif bday_span is not None and dday_span is None:
        bday_val = int(bday_span.get_text()[:4])
        dday_val = int(dday_span.get_text()[:4])
        return dday_val - bday_val
    else:
        logging.warning('age not found, assume 35')
        return 35



def search_movie_table(filmography_span, movie_list):
    '''
    helper func for get_actor_cast_movies
    :param filmography_span:
    :param movie_list:
    :return:
    '''
    #if (len(movie_list) > 4):
        #return
    table = filmography_span.find_next('table', {'class': re.compile('wikitable')})
    if table is not None:
        items = table.find_all('a', {'href': re.compile('/wiki/'), 'title': re.compile(''), 'class': ''})
        for i in items:
            if len(i.get('href')) > 7:
                movie_list.append(i.get('href')[6:])
    return


def search_movie_ul(filmography_span, movie_list):
    '''
    helper func for get_actor_cast_movies
    :param filmography_span:
    :param movie_list:
    :return:
    '''
    #if(len(movie_list)>4):
        #return
    ul = filmography_span.find_next('ul')
    if ul is not None:
        items = ul.find_all('a', {'href': re.compile('/wiki/'), 'title': re.compile(''), 'class': ''})
        for i in items:
            if len(i.get('href')) > 7:
                movie_list.append(i.get('href')[6:])
    return



def get_actor_cast_movies(actorsoup):
    '''
    give a actor page, return a list of movies he once acted
    :param actorsoup:
    :return:
    '''
    movie_list=[]
    filmography_span = actorsoup.find('span', {'class': 'mw-headline', 'id': 'Filmography'})
    if filmography_span is not None:
        search_movie_ul(filmography_span, movie_list)
        search_movie_table(filmography_span, movie_list)
    return movie_list#[:4]


def nametourl(namestr):
    '''
    given a move or actor name, return its wiki url
    :param namestr:
    :return:
    '''
    return ("https://en.wikipedia.org/wiki/" + namestr)


def calcweight(money,age):
    return money/10*age/100*(random.random()+0.01)

























