from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import random
import helperfuncs
import networkx as nx
import json

class Graph:
    def __init__(self, actors, movies):
        # self.data_list = json.load(open('data.json',encoding='utf-8'))
        # self.actors_dict = self.data_list[0]
        # self.movies_dict = self.data_list[1]
        self.actors_dict = actors
        self.movies_dict = movies


    def add_actor_vertex(self, name, age, mlist):
        self.actors_dict[name]=[age, mlist]


    def add_movie_vertex(self, name, year, money, alist):
        self.movies_dict[name]=[year, money, alist]


    def create_edge(self, moviename, actorname):
        case1=moviename in self.movies_dict.keys()
        case2=actorname in self.actors_dict.keys()
        if case1 and case2:
            self.movies_dict[moviename][2].append(actorname)
            self.actors_dict[actorname][1].append(moviename)


    def get_actor_vertex(self, name):
        if name in self.actors_dict.keys():
            return self.actors_dict[name]
        else:
            return -1


    def get_actor_vertex_cond(self,key,val):
        ans=[]
        if(key=="name"):
            val=val[1:-1]
        for actname in self.actors_dict.keys():
            if (key == "name"):
                if self.actors_dict[actname][key] == (val):
                    ans.append(self.actors_dict[actname])
            else:
                if self.actors_dict[actname][key]==int(val):
                    ans.append(self.actors_dict[actname])
        return ans


    def get_movie_vertex_cond(self,key,val):
        ans=[]
        if(key=="name"):
            val=val[1:-1]
        for actname in self.movies_dict.keys():
            if (key == "name"):
                if self.movies_dict[actname][key] == (val):
                    ans.append(self.movies_dict[actname])
            else:
                if self.movies_dict[actname][key]==int(val):
                    ans.append(self.movies_dict[actname])
        return ans



    def get_actor_age(self, name):
        if name not in self.actors_dict.keys():
            return 32
        return self.actors_dict[name][0]


    def calcweight(money, age):
        return money / 10 * age / 100 * (random.random() + 0.01)


    def get_movie_vertex(self, name):
        if name in self.movies_dict.keys():
            return self.movies_dict[name]
        else:
            return -1


    #Find how much a movie has grossed
    def find_movie_grossed(self, moviename):
        if moviename in self.movies_dict.keys():
            value=self.movies_dict[moviename][1]
            print(moviename+ " has grossed "+str(value)+ " dollars")
            return value
        else:
            print("movie not in database")
            return 0


    #List which movies an actor has worked in
    def find_actor_movielist(self, actorname):
        if actorname in self.actors_dict.keys():
            mlist=self.actors_dict[actorname][1]
            print(actorname+ " has worked in ")
            print(mlist)
            print("these movies as above")
            return mlist
        else:
            print("actor not in database")
            return []


    #List which actors worked in a movie
    def find_movie_actorlist(self, moviename):
        if moviename in self.movies_dict.keys():
            aclist=self.movies_dict[moviename][2]
            print("the following actors has acted in a movie called"+moviename)
            print(aclist)
            return aclist
        else:
            print("movie not in database")
            return []


    #List the top X actors with the most total grossing value
    def find_topgross_x_actors(self, n):
        temp_dict=dict()
        if n <= 0 or n > len(self.actors_dict):
            print("invalid X input")
            return []
        else:
            for k,v in self.movies_dict.items():
                temp_dict[k]=[v[1],v[2]]
            #print(temp_dict)
            n_richest_actors = OrderedDict(sorted(temp_dict.items(), key=lambda x: x[1], reverse=True))
            #print(n_richest_actors)
            n_richest_actor_list = []
            for key, value in n_richest_actors.items():
                for name in value[1]:
                    n_richest_actor_list.append(name)

            print("richest " +str(n)+" actors are ")
            print(n_richest_actor_list[:n])
            return n_richest_actor_list[:n]






    #citation: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    #List the oldest X actors
    def find_oldest_x_actors(self, n):
        if n <= 0 or n > len(self.actors_dict):
            print("invalid X input")
            return []
        else:
            print(self.actors_dict)
            n_oldest_actors = OrderedDict(sorted(self.actors_dict.items(), key=lambda x: x[1], reverse=True))
            #print(top_actors)
            n_oldest_actor_list = []
            for key, value in n_oldest_actors.items():
                n_oldest_actor_list.append(key)

            print("oldest " +str(n)+" actors are ")
            print(n_oldest_actor_list[:n])
            return n_oldest_actor_list[:n]






    #List all the movies for a given year
    def movies_in_the_year(self, year):
        if year<0:
            print("invalid year input")
            return []

        l=[]
        for k,v in self.movies_dict.items():
            #print(self.movies_dict)
            if v[0]==year:
                l.append(k)
        if len(l)<1:
            print("no movies in " + str(year))
            return []
        else:
            print("movies in " + str(year)+" are ")
            print(l)
            return l


    #List all the actors for a given year
    def actors_in_the_year(self, year):
        if year<0:
            print("invalid year input")
            return []
        l=[]
        for k,v in self.actors_dict.items():
            if (2018-v[0])==year:
                l.append(k)
        if len(l)<1:
            print("no actors in " + str(year))
            return []
        else:
            print("actors in " + str(year)+" are ")
            print(l)
            return l

    def find_hub_actor(self,n=1):
        connection=dict()
        for key in self.movies_dict.keys():
            actotlist=self.movies_dict[key][2]
            for actor in actotlist:
                if actor not in connection.keys():
                    connection[actor]=0
                connection[actor]+=1
        #print(connection)
        n_hub_actors = OrderedDict(sorted(connection.items(), key=lambda x: x[1], reverse=True))
        print(n_hub_actors)
        n_hub_actor_list = []
        for key, value in n_hub_actors.items():
            n_hub_actor_list.append(key)

        return n_hub_actor_list[:n]


    def find_actor_connection_dict(self):
        connection=dict()
        for key in self.movies_dict.keys():
            actotlist=self.movies_dict[key][2]
            for actor in actotlist:
                if actor not in connection.keys():
                    connection[actor]=0
                connection[actor]+=1
        #print(connection)
        n_hub_actors = OrderedDict(sorted(connection.items(), key=lambda x: x[1], reverse=True))
        print(n_hub_actors)
        return connection
        #return n_hub_actors


    def get_actor_gross(self, name):
        accumulator=100000
        for moviename in self.movies_dict.keys():
            actotlist=self.movies_dict[moviename][2]
            if name in actotlist:
                actorage=self.get_actor_age(name)
                tempmoney=self.movies_dict[moviename][1]
                portionmoney=helperfuncs.calcweight(tempmoney,actorage)
                accumulator=accumulator+portionmoney

        return accumulator



    def accu_grossing_val(self, lowerbound, upperbound):
        grossing_value = 0
        for actor, val in self.actors_dict.items():
            age = self.get_actor_age(actor)
            if lowerbound <= age <= upperbound:
                grossing_value += self.get_actor_gross(actor)
        return grossing_value


    def built_age_gross_plot(self):
        range = ('0--20', '20--30', '30--40', '40--50', '50--60', '60--70', '70--100')
        x_pos = np.arange(len(range))
        val = [self.accu_grossing_val(0, 20),self.accu_grossing_val(20, 30),self.accu_grossing_val(30, 40),
               self.accu_grossing_val(40, 50),self.accu_grossing_val(50, 60),self.accu_grossing_val(60, 70),
            self.accu_grossing_val(70, 100)]
        plt.figure(1,figsize=(20, 20))
        plt.bar(x_pos, val, align='center')
        plt.xticks(x_pos, range)
        plt.title('Age-Grossing-Correlation-plot')
        plt.xlabel('Age Group')
        plt.ylabel('Grossing Value')
        plt.savefig('data-analysis-age-gross-correlation.png')
        return 0


    def built_hub_plot(self):
        actor_conncection_dict=self.find_actor_connection_dict()
        actor_list = []
        connection_freq_list = []

        for actor, info in actor_conncection_dict.items():
            actor_list.append(actor)
            if actor not in actor_conncection_dict.keys():
                connection_freq_list.append(0)
            else:
                connection_freq_list.append(actor_conncection_dict[actor])

        D = len(actor_list)
        x = np.linspace(0, D, D)
        y = np.array(connection_freq_list)
        plt.figure(2)
        plt.scatter(x, y, s=np.pi * 2, c=(0.1, 0.5, 0.4), alpha=0.3)
        plt.title('Connection Scatter plot')
        plt.xlabel('actor')
        plt.ylabel('connection frequency')
        plt.savefig('connection.png')
        return

    #Below Reference:Rika321
    ########################################################################


    def built_graph_visualization(self):
        actor_list = []
        movie_list = []
        connections = dict()
        for key, val in self.actors_dict.items():
            actor_list.append(key)
        for key, val in self.movies_dict.items():
            movie_list.append(key)

            for actor in val['actors']:
                if actor in actor_list:
                    connections[(key, actor)] = val['box_office']
                #connections[actor] = self.get_actor_gross(actor)
        # for key in connections.keys():
        #     connections[key]=1
        # for key, val in self.movies_dict.items():
        #     actotlist = self.movies_dict[key][2]
        #     for actor in actotlist:
        #         connections[actor] = self.get_actor_gross(actor)

        G = nx.Graph()
        G.add_nodes_from(actor_list)
        G.add_nodes_from(movie_list)
        #print("connections")
        #print(connections)
        for key, val in connections.items():
            #print("keyval")
            #print(key)
            #print(val)
            G.add_edge(key[0], key[1])

        self.save_graph(G, actor_list, movie_list, connections)
        return

    def save_graph(self, graph, actor_list, movie_list, connections):
        plt.figure(num=None, figsize=(30, 30))
        plt.axis('off')
        fig = plt.figure(5)
        pos = nx.random_layout(graph)
        nx.draw_networkx_nodes(graph, pos, actor_list, node_color='g',
                               node_size=10)
        nx.draw_networkx_nodes(graph, pos, movie_list, node_color='b',
                               node_size=10)
        #print("connections")
        #print(connections)

        for co, wei in connections.items():
            small = dict()
            small[co] = 1
            nx.draw_networkx_edges(graph, pos, small, width=wei/100000000, alpha=0.8, edge_color='r')

        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xlabel('green is actor node')
        plt.ylabel('blue is movie node')
        plt.title('Grpah Data Visualization')
        plt.savefig("graph.png")


    def delete_actor(self, name):
        if name in self.actors_dict.keys():
            self.actors_dict.pop(name,None)
            return 0
        else:
            return -1


    def delete_movie(self, name):
        if name in self.movies_dict.keys():
            self.movies_dict.pop(name,None)
            return 0
        else:
            return -1


    def updata_mem(self):
        data_list = [self.actors_dict, self.movies_dict]
        outfile = open("api-mod.json", 'w')
        outfile.write(json.dumps(data_list, sort_keys=True, indent=4))
        return 0

    def reconstruct_graph(self):
        test = json.load(open('api-mod.json', encoding='utf-8'))
        self.actors_dict = test[0]
        self.movies_dict = test[1]


    def generate_actor_instance(self,name):
        instance={
            "json_class": "Actor",
            "name": name,
            "age": random.randint(20,90),
            "total_gross": random.randint(1000,100000),
            "movies": []
        }
        return instance

    def generate_movie_instance(self,name):
        instance={
            "json_class": "Movie",
            "name": name,
            "wiki_page": "https://en.wikipedia.org/wiki/"+name,
            "box_office": random.randint(10000,10000000),
            "year": random.randint(1900,2018),
            "actors": []
        }
        return instance

    def actor_dict_add_record(self,namekey,valinstance):
        self.actors_dict[namekey]=valinstance
        return 0


    def movie_dict_add_record(self,namekey,valinstance):
        self.movies_dict[namekey]=valinstance
        return 0


    def post_url_parse(self, url):
        return url[35:-1]


    def get_url_parse(self,url):
        a,b=url.split("?")
        key,val=b.split("=")
        print(key)
        print(val)
        return key,val


    def update_actor_record(self,key,val,name):
        if(key=="name"):
            val=val[1:-1]
        if(key=="name"):
            self.actors_dict[name][key] = (val)
        else:
            self.actors_dict[name][key]=int(val)
        return 0


    def update_movie_record(self,key,val,name):
        if(key=="name"):
            val=val[1:-1]
        if(key=="name"):
            self.movies_dict[name][key] = (val)
        else:
            self.movies_dict[name][key]=int(val)
        return 0