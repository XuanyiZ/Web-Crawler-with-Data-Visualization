import graph
import json
import unittest

class TestGraph(unittest.TestCase):

    movies_info = json.load(open('movies-fine.json'))
    actors_info = json.load(open('actors-fine.json'))
    # print(movies_info)
    my_graph = graph.Graph(actors_info, movies_info)


    my_graph.find_movie_grossed("Paper Moon (film)")
    assert 30900000.0==my_graph.find_movie_grossed("Paper Moon (film)")
    my_graph.find_movie_grossed("Running Man")
    assert 0==my_graph.find_movie_grossed("Running Man")


    my_graph.find_actor_movielist("Jackie Curtis")
    assert 4==len(my_graph.find_actor_movielist("Jackie Curtis"))
    my_graph.find_actor_movielist("Obama")
    assert []==my_graph.find_actor_movielist("Obama")


    my_graph.find_movie_actorlist("Panic in the Streets (film)")
    assert 4==len( my_graph.find_movie_actorlist("Panic in the Streets (film)"))
    my_graph.find_movie_actorlist("SMTM6")
    assert []==my_graph.find_movie_actorlist("SMTM6")

    my_graph.find_oldest_x_actors(3)
    assert ['Eva Marie Saint', 'Carleton Carpenter', 'Sidney Poitier']==my_graph.find_oldest_x_actors(3)
    my_graph.find_oldest_x_actors(888)
    assert []==my_graph.find_oldest_x_actors(888)

    my_graph.find_topgross_x_actors(6)
    assert ['Henry_Thomas', 'Robert_MacNaughton', 'Drew_Barrymore', 'Dee_Wallace', 'Anthony_Gonzalez_(actor)', 'Tom_Cruise']==my_graph.find_topgross_x_actors(6)
    my_graph.find_topgross_x_actors(666)
    assert []==my_graph.find_topgross_x_actors(666)

    my_graph.movies_in_the_year(1950)
    assert 5==len(my_graph.movies_in_the_year(1950))
    my_graph.movies_in_the_year(1800)
    assert 0==len(my_graph.movies_in_the_year(1800))


    my_graph.actors_in_the_year(1983)
    assert 72==(len(my_graph.actors_in_the_year(1983)))
    my_graph.actors_in_the_year(1500)
    assert 0 == (len(my_graph.actors_in_the_year(1500)))




    my_graph.built_age_gross_plot()

    my_graph.built_hub_plot()

    print(my_graph.get_actor_age("Ethan Hawke"))
    print(my_graph.find_hub_actor(1))



    test = json.load(open('data.json',encoding='utf-8'))
    my_graph.actors_dict=test[0]
    my_graph.movies_dict=test[1]
    my_graph.built_graph_visualization()

