import networkx as nx
import facebook

auth = 'AAAAAAITEghMBALCmvfgLxA4T9uHsXBAhV8riHx5uzy20rxhr4ce6TYrMIL0V3aU5DVctl3uuDLRb4PAemfwq5kajxZA4qzFqun6KGn1rPBIiX80wt'
#lol no actual facebook authentication
#lol python comments look like hashtags

g = facebook.GraphAPI(auth)
friend_graph = nx.Graph()
like_graph = nx.Graph()
bp_graph = nx.Graph() #bipartite friend/likes?

def get_friends():
    data = g.get_connections('me', 'friends')['data']
    return data

def make_friends(data):
    """I'm pretty sure I think this is way funnier than it should be"""
    friends = []
    for friend in data:
        uid, name = friend['id'], friend['data'] 
        friends.append(Friend(uid, name))
    return friends

def add_friend_nodes(friends):
    for f in friends:
        friend_graph.add_node(f.uid, name=f.name)
        bp_graph.add_node(f.uid, name=f.name, bipartite = 0)

def add_likes(friends):
    """Adds page nodes and edges between friends and pages"""
    for f in friends:
        likes = f.get_likes() 
        for l in likes:
            if not bp_graph.has_node(l.uid):
                bp_graph.add_node(l.uid, name = l.name, bipartite = 1)
            bp_graph.add_edge(f.uid, l.uid)


class Page:

    def __init__(self, uid, name):
        self.name = name
        self.uid = uid

class Friend:
    likes = []
    def __init__(self, uid, name):
        self.name = name
        self.uid = uid

    def get_likes(self):
        likes = g.get_connections(uid, 'music')['data']
        for l in likes:
            self.likes.append(Page(l['id'], l['name']))
        return self.likes
        
if __name__ == '__main__':
    data = get_friends()
    friends = make_friends(data)
    add_friends_nodes(friends)
    add_likes(friends)

