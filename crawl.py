import networkx as nx
import bottle
import urllib2
import json
from networkx import bipartite as bp
import facebook
import matplotlib.pyplot as plt

#lol no actual facebook authentication
#lol python comments look like hashtags

auth = 'AAAAAAITEghMBAHoLngdj3nopyE6MUDzOtoTxlgvuq7s3MmKltq8s78bJ6E02pkGL7OQrjZAhGDqGVe4ksSawqezW4YXoaJOY8zljfcUO3BWXTX6y3'

class FBGraph:
    def __init__(self, auth):
        self.g = facebook.GraphAPI(auth)
        self.friend_graph = nx.Graph()
        self.bp_graph = nx.Graph() #bipartite friend/likes?

    def get_friends(self):
        data = self.g.get_connections('me', 'friends')['data']
        return data

    def make_friends(self, data):
        """I'm pretty sure I think this is way funnier than I should"""
        friends = []
        for friend in data[0:50]:
            uid, name = friend['id'], friend['name'] 
            friends.append(Friend(uid, name, self.g))
        return friends

    def add_friend_nodes(self, friends):
        for f in friends:
            self.friend_graph.add_node(f.name, uid=f.uid)
            self.bp_graph.add_node(f.name, uid=f.uid, bipartite = 0)

    def add_likes(self, friends):
        """Adds page nodes and edges between friends and pages"""
        for f in friends:
            print f.name
            likes = f.get_likes() 
            print [l.name for l in likes]
            #if len(likes) == 0:
            #    bp_graph.remove_node(f.name)
            for l in likes:
                if not self.bp_graph.has_node(l.name):
                    self.bp_graph.add_node(l.name, uid = l.uid, bipartite = 1)
                self.bp_graph.add_edge(f.name, l.name)

    def get_friend_graph(self):
        pages = set(f for f,d in self.bp_graph.nodes(data=True) if d['bipartite']==1)
        people = set(f for f,d in self.bp_graph.nodes(data=True) if d['bipartite']==0)
        for page in pages:
            fans = self.bp_graph.neighbors(page)
            for fan1 in fans:
                for fan2 in fans:
                    self.join_friends(fan1, fan2)
        return self.friend_graph
                       
    def join_friends(self, f1, f2):
        if f1 != f2:
            if not self.friend_graph.has_edge(f1, f2):
                self.friend_graph.add_edge(f1, f2, weight = 0) 
            self.friend_graph[f1][f2]['weight'] += 1

    def run(self):
        data = self.get_friends()
        for line in data:
            print line
        friends = self.make_friends(data)
        self.add_friend_nodes(friends)
        self.add_likes(friends)
        friend_graph = self.get_friend_graph()
        print '\n'
        print nx.clustering(friend_graph)
        print '\n'
        for edge in sorted(friend_graph.edges(data=True), key= lambda x: -1*x[2].get('weight', 1)):
            print edge
        nx.draw_random(friend_graph)
        plt.show()

class Page:

    def __init__(self, uid, name):
        self.name = name
        self.uid = uid

class Friend:

    def __init__(self, uid, name, fb_inst):
        self.name = name
        self.uid = uid
        self.likes = []
        self.g = fb_inst

    def get_likes(self):
        likes = self.g.get_connections(self.uid, 'likes')['data']
        for l in likes:
            self.likes.append(Page(l['id'], l['name']))
        return self.likes
 
def main():
    graph = FBGraph(auth)
    data = graph.get_friends()
    for line in data:
        print line
    friends = graph.make_friends(data)
    graph.add_friend_nodes(friends)
    graph.add_likes(friends)
    friend_graph = graph.get_friend_graph()
    print '\n'
    print nx.clustering(friend_graph)
    print '\n'
    for edge in sorted(friend_graph.edges(data=True), key= lambda x: -1*x[2].get('weight', 1)):
        print edge
    nx.draw_random(friend_graph)
    plt.show()
    plt.savefig('graph.png')

if __name__ == '__main__':
    main()
