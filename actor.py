import json, ast

class Actor:
    def __init__(self, age, name, movies_set, weight):
        self.age=age
        self.name=name
        self.movies=movies_set
        self.weight=weight