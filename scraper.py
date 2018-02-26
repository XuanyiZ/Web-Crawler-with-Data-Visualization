from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import urllib.error
import re
import logging
from collections import deque
# https://docs.python.org/2/library/collections.html#collections.deque
import json
import ast
import signal
import sys
import helperfuncs

# Concept:
# Each actor has a list of movies that they have acted in,
# with the “href” of the movie linking to the respective Wikipedia page.
#
# Each movie has a list of actors starring in it,
# with an “href” of the actor linking to the respective Wikipedia page.
#
# Start with one page, for e.g., that of Morgan Freeman. Maintain a queue
# and keep adding the new hrefs that you find in the queue.
# Scrape till the queue is empty/till you’ve reached a desirable limit.

def sig_handler(signum, frame):
    logging.fatal("Process killed by signal " + str(signum) + " at " + frame)
    sys.exit()

#only python dict can be dump to json object
def scrape():
    signal.signal(signal.SIGINT, sig_handler)
    #starturl = "Ellie Bamber"
    starturl = "Morgan_Freeman"
    urlqueue = deque()
    urlqueue.append(starturl)
    #urlqueue.append("Morgan_Freeman")


    movies_info_dict = dict() #stop when len > 128
    actors_info_dict = dict() #stop when len > 258

    while len(urlqueue)>0 and (len(movies_info_dict)<125 or len(actors_info_dict)<250):
        cururl=urlqueue.popleft()
        logging.info(" Processing https://en.wikipedia.org/wiki/" + cururl)
        print(" Processing https://en.wikipedia.org/wiki/" + cururl)
        if(cururl in movies_info_dict.keys()) or (cururl in actors_info_dict.keys()):
            logging.debug(cururl + " already exists in the dictionary.")
            print(cururl + " already exists in the dictionary.")
            continue
        try:
            response = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + cururl)
        except urllib.error.HTTPError:
            logging.warning("the url: https://en.wikipedia.org/wiki/" + cururl + " 404 not found")
            continue
        except urllib.error.URLError:
            logging.warning("the url: https://en.wikipedia.org/wiki/" + cururl + " is not formatted")
            continue


        soup = BeautifulSoup(response.read(), 'html.parser')
        if helperfuncs.ismovie(soup):
            name=helperfuncs.get_actor_or_movie_name(soup)
            logging.info("Found the movie called " + name)
            print("Found the movie called " + name)
            scrape_onemovie(movies_info_dict, actors_info_dict, urlqueue, soup, cururl)

        elif helperfuncs.isactor(soup):
            name=helperfuncs.get_actor_or_movie_name(soup)
            logging.info("Found the actor called " + name)
            print("Found the actor called " + name)
            scrape_oneactor(movies_info_dict, actors_info_dict, urlqueue, soup, cururl)

        else:
            logging.warning("The given url " + cururl + " is neither actor nor movie.")


        print(len(movies_info_dict))
        print(len(actors_info_dict))
        continue

    outfile1 = open('movies.json', 'w')
    outfile1.write(json.dumps(movies_info_dict, sort_keys=True, indent=4))
    outfile2 = open('actors.json', 'w')
    outfile2.write(json.dumps(actors_info_dict, sort_keys=True, indent=4))
    logging.info("movies_info_dict is full of " + str(len(movies_info_dict))+ "items")
    print("movies_info_dict is full of " + str(len(movies_info_dict))+ "items")
    logging.info("actors_info_dict is full of " + str(len(actors_info_dict)) + "items")
    print("actors_info_dict is full of " + str(len(actors_info_dict)) + "items")

def scrape_onemovie(movies_info_dict, actors_info_dict, urlqueue, soup, cururl):
    curactors_list_temp=helperfuncs.get_starring_actors(soup)
    #if u want to cut scraping time within 10 mins, delete this if
    #if(len(curactors_list_temp)==0):
        #return
    curactors_list=filteractorlist(curactors_list_temp)
    curreleaseyear=helperfuncs.get_movie_year(soup)
    curname=helperfuncs.get_actor_or_movie_name(soup)
    curgross=helperfuncs.get_movie_gross(soup)
    movies_info_dict[curname]=[curreleaseyear,curgross,curactors_list]
    for elem in curactors_list:
        urlqueue.append(elem)

    return


def scrape_oneactor(movies_info_dict, actors_info_dict, urlqueue, soup, cururl):
    curname=helperfuncs.get_actor_or_movie_name(soup)
    curage=helperfuncs.get_actor_age(soup)
    curmovie_list_temp=helperfuncs.get_actor_cast_movies(soup)
    #if u want to cut scraping time within 10 mins, delete this if
    #if (len(curmovie_list_temp) == 0):
        #return
    curmovie_list=filtermovielist(curmovie_list_temp)
    actors_info_dict[curname]=[curage,curmovie_list]
    for elem in curmovie_list:
        #if "Texas" in elem:
            #print(cururl)
            #logging.warning(cururl)
        urlqueue.append(elem)

def filteractorlist(cur_list):
    new_list=[]
    for elem in cur_list:
        if "php" in elem:
            continue
        elif "?" in elem:
            continue
        elif "&" in elem:
            continue
        elif "#" in elem:
            continue
        elif "/" in elem:
            continue
        elif "%" in elem:
            continue
        elif "=" in elem:
            continue
        elif "1" in elem:
            continue
        elif "2" in elem:
            continue
        elif "3" in elem:
            continue
        elif "4" in elem:
            continue
        elif "5" in elem:
            continue
        elif "6" in elem:
            continue
        elif "7" in elem:
            continue
        elif "8" in elem:
            continue
        elif "9" in elem:
            continue
        elif "0" in elem:
            continue
        else:
            new_list.append(elem)

    return new_list


def filtermovielist(cur_list):
    new_list=[]
    for elem in cur_list:
        if "php" in elem:
            continue
        elif "?" in elem:
            continue
        elif "IMDb" in elem:
            continue
        elif "witter" in elem:
            continue
        elif "OC" in elem:
            continue
        elif "All" in elem:
            continue
        elif "www" in elem:
            continue
        elif "%" in elem:
            continue
        elif "/" in elem:
            continue
        elif "#" in elem:
            continue
        elif "ward" in elem:
            continue
        elif "ote" in elem:
            continue
        else:
            new_list.append(elem)

    return new_list