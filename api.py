import graph
import json
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import random
import helperfuncs
import networkx as nx
from flask import Flask, jsonify, request,abort, make_response

# Reference
# 1. excellent tutorial: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


#!flask/bin/python
app = Flask(__name__)
file_orig = 'api-orig.json'
file_mod = 'api-mod.json'
movies_info = json.load(open('movies-fine.json'))
actors_info = json.load(open('actors-fine.json'))
my_graph = graph.Graph(actors_info, movies_info)
test = json.load(open('api-mod.json',encoding='utf-8'))
my_graph.actors_dict=test[0]
my_graph.movies_dict=test[1]


@app.route('/')
def index():
    return "Hello, World!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# DELETE actors
@app.route('/actors/<actor_name>', methods=['DELETE'])
def delete_actor(actor_name):

    status = my_graph.delete_actor(actor_name)
    if status == -1:
        return jsonify("not found"), 404
    else:
        my_graph.updata_mem()
        my_graph.reconstruct_graph()
        return jsonify("deleted"), 200


# DELETE movies
@app.route('/movies/<movie_name>', methods=['DELETE'])
def delete_movie(movie_name):

    status = my_graph.delete_movie(movie_name)
    if status == -1:
        return jsonify("not found"), 404
    else:
        my_graph.updata_mem()
        my_graph.reconstruct_graph()
        return jsonify("deleted"), 200


# POST actors--Create and add a new record / insert a new item into database
@app.route('/actors', methods=['POST'])
def post_actor():

    url=request.url
    name=my_graph.post_url_parse(url)
    if(len(name)<1):
        abort(400)
    val=my_graph.generate_actor_instance(name)
    my_graph.actor_dict_add_record(name,val)
    my_graph.updata_mem()
    my_graph.reconstruct_graph()
    return jsonify("posted"), 201


# POST movies--Create and add a new record / insert a new item into database
@app.route('/movies', methods=['POST'])
def post_movie():
    url=request.url
    name=my_graph.post_url_parse(url)
    if (len(name) < 1):
        abort(400)
    val=my_graph.generate_movie_instance(name)
    my_graph.movie_dict_add_record(name,val)
    my_graph.updata_mem()
    my_graph.reconstruct_graph()
    return jsonify("posted"), 201


# GET actors
@app.route('/actors/<actor_name>', methods=['GET'])
def get_actor(actor_name):

    status = my_graph.get_actor_vertex(actor_name)
    if status == -1:
        return jsonify("not found"), 404
    else:
        my_graph.updata_mem()
        my_graph.reconstruct_graph()
        return jsonify(status), 200


# GET movies
@app.route('/movies/<movie_name>', methods=['GET'])
def get_movie(movie_name):
    status = my_graph.get_movie_vertex(movie_name)
    if status == -1:
        return jsonify("not found"), 404
    else:
        my_graph.updata_mem()
        my_graph.reconstruct_graph()
        return jsonify(status), 200



# GET actors
@app.route('/actors', methods=['GET'])
def get_actor_cond():
    url=request.url
    key,val=my_graph.get_url_parse(url)
    ans=my_graph.get_actor_vertex(val[1:-1]) #qudiao yinhao
    ans2=my_graph.get_actor_vertex_cond(key,val)
    print(ans2)
    my_graph.updata_mem()
    my_graph.reconstruct_graph()
    return jsonify(ans2), 201


# GET movies
@app.route('/movies', methods=['GET'])
def get_movie_cond():
    url=request.url
    key,val=my_graph.get_url_parse(url)
    ans=my_graph.get_movie_vertex(val[1:-1]) #qudiao yinhao
    ans2=my_graph.get_movie_vertex_cond(key,val)
    print(ans2)
    my_graph.updata_mem()
    my_graph.reconstruct_graph()
    return jsonify(ans2), 201



# PUT actors
@app.route('/actors/<actor_name>', methods=['PUT'])
def put_actor_cond(actor_name):
    url=request.url
    print(actor_name) #Alex
    print(url) #http://127.0.0.1:5000/actors/Alex?age=52
    key,val=my_graph.get_url_parse(url)
    my_graph.update_actor_record(key,val,actor_name)
    my_graph.updata_mem()
    my_graph.reconstruct_graph()
    return jsonify("Put"), 201




# PUT movies
@app.route('/movies/<movie_name>', methods=['PUT'])
def put_movie_cond(movie_name):
    url=request.url
    print(movie_name)
    print(url)
    key,val=my_graph.get_url_parse(url)
    my_graph.update_movie_record(key,val,movie_name)
    my_graph.updata_mem()
    my_graph.reconstruct_graph()
    return jsonify("Put"), 201









if __name__ == '__main__':
    app.run(debug=True)