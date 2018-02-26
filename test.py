import random
import scraper
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import helperfuncs


def test_ismovie():
    redditFile = urlopen("https://en.wikipedia.org/wiki/Now_You_See_Me_(film)")
    #redditFile = urlopen("https://en.wikipedia.org/wiki/Morgan_Freeman")
    redditHtml = redditFile.read()
    redditFile.close()

    soup = BeautifulSoup(redditHtml, 'html.parser')
    # print(soup)
    spans = soup.find_all('th', text='Cinematography')
    for span in spans:
        print(span)
        print(len(spans))

#test_ismovie()

def test_isactor():
    #redditFile = urlopen("https://en.wikipedia.org/wiki/Now_You_See_Me_(film)")
    redditFile = urlopen("https://en.wikipedia.org/wiki/Gal_Gadot")
    redditHtml = redditFile.read()
    redditFile.close()

    soup = BeautifulSoup(redditHtml, 'html.parser')
    boo=helperfuncs.isactor(soup)
    print(boo)
    ans = soup.find_all("td", {'class': 'role'})
    for span in ans:
        print(span.get_text()=="Actress")
        print(len(ans))

#test_isactor()


def test_get_starring_actors():
    File = urlopen("https://en.wikipedia.org/wiki/Wanted_(2008_film)")
    #File = urlopen("https://en.wikipedia.org/wiki/Morgan_Freeman")
    redditHtml = File.read()
    File.close()

    soup = BeautifulSoup(redditHtml, 'html.parser')
    print(helperfuncs.get_actor_age(soup))
    print(helperfuncs.get_actor_or_movie_name(soup))
    l=helperfuncs.get_starring_actors(soup)
    print(l)
    print(helperfuncs.get_movie_gross(soup))
    print(helperfuncs.get_movie_year(soup))
    print(set(helperfuncs.get_actor_cast_movies(soup)))

test_get_starring_actors()

scraper.scrape()