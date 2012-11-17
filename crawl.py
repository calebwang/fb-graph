import networkx as nx
from networkx import bipartite as bp
import facebook
import matplotlib.pyplot as plt

auth = 'AAAAAAITEghMBAAAeONjOrPvCKg1ePiZCwEV4fo2cuNC9fSEy3ZA9tA7ZCADRpBXt8bpWu9tsd7PFKLKFNUDQi9sgZCZCVhyFCNWYZBZABnjZApPIbmR8xV9f'
#lol no actual facebook authentication
#lol python comments look like hashtags

g = facebook.GraphAPI(auth)
friend_graph = nx.Graph()
bp_graph = nx.Graph() #bipartite friend/likes?

def get_friends():
    data = g.get_connections('me', 'friends')['data']
    return data

def make_friends(data):
    """I'm pretty sure I think this is way funnier than it should be"""
    friends = []
    for friend in data[0:40]:
        uid, name = friend['id'], friend['name'] 
        friends.append(Friend(uid, name))
    return friends

def add_friend_nodes(friends):
    for f in friends:
        friend_graph.add_node(f.name, uid=f.uid)
        bp_graph.add_node(f.name, uid=f.uid, bipartite = 0)

def add_likes(friends):
    """Adds page nodes and edges between friends and pages"""
    for f in friends:
        print f.name
        likes = f.get_likes() 
        print [l.name for l in likes]
        if len(likes) == 0:
            bp_graph.remove_node(f.name)
        for l in likes:
            if not bp_graph.has_node(l.name):
                bp_graph.add_node(l.name, uid = l.uid, bipartite = 1)
            bp_graph.add_edge(f.name, l.name)

def get_friend_graph(bp_graph):
    pass

class Page:

    def __init__(self, uid, name):
        self.name = name
        self.uid = uid

class Friend:
    def __init__(self, uid, name):
        self.name = name
        self.uid = uid
        self.likes = []

    def get_likes(self):
        likes = g.get_connections(self.uid, 'music')['data']
        for l in likes:
            self.likes.append(Page(l['id'], l['name']))
        return self.likes
        
if __name__ == '__main__':
    data = get_friends()
    print data
    friends = make_friends(data)
    add_friend_nodes(friends)
    add_likes(friends)
    bp.color(bp_graph)
    people = set(f for f,d in bp_graph.nodes(data=True) if d['bipartite']==0)
    graph = bp.projected_graph(bp_graph, people)
    print bp_graph.edges()
    print '\n'
    print bp.clustering(bp_graph)
    nx.draw(bp_graph)
    plt.show()
