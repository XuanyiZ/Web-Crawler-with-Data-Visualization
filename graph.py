from collections import OrderedDict


class Graph:
    def __init__(self, actors, movies):
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
        return self.actors_dict[name]


    def get_movie_vertex(self, name):
        return self.movies_dict[name]


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