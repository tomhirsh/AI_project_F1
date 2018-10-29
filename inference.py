import training_testing
import numpy as np
import operator
from collections import defaultdict
"""
This script is the "main" script in this project.
Given a list of drivers (their features), the output is the race result (finish line order).
(Using the classifier from training_testing.py and the "remove cycles" algorithm)
The input should be:
[driver_id,...driver_features...]
"""

"""
Graph implementation:
detecting a cycle and doing a Topological sorting
"""
class Graph():
    def __init__(self, vertices): 
        self.graph = defaultdict(list)  # dictionary containing the list of edges
        self.V = vertices  #

    # add edge to the graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        for neighbour in self.graph[v]:
            if not visited[neighbour]:
                if self.isCyclicUtil(neighbour, visited, recStack):
                    return True
            elif recStack[neighbour]:
                return True

        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns True if graph is cyclic else False
    def isCyclic(self):
        visited = [False] * self.V
        recStack = [False] * self.V
        for node in range(self.V):
            if visited[node] == False:
                if self.isCyclicUtil(node,visited,recStack) == True:
                    return True
        return False

    # A recursive function used by topologicalSort
    def topologicalSortUtil(self, v, visited, stack):

        # Mark the current node as visited.
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                self.topologicalSortUtil(i, visited, stack)

                # Push current vertex to stack which stores result
        stack.insert(0, v)

        # The function to do Topological Sort. It uses recursive

    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        visited = [False] * self.V
        stack = []

        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if not visited[i]:
                self.topologicalSortUtil(i, visited, stack)
        return stack

"""
a helper function to get the key order, by feature importance (by weights)
"""
def get_key_order(list_to_sort):
    keys_sorted = {}
    for i in range(len(list_to_sort)):
        keys_sorted[i] = list_to_sort[i]
    keys_sorted = sorted(keys_sorted.items(), key=operator.itemgetter(1), reverse=True)
    #print(keys_sorted)
    out_keys = []
    for x in range(len(list_to_sort)):
        out_keys.append(keys_sorted[x][0])
    #print(out_keys)
    return out_keys


def sort_dict_by_lists(prepared_edges):
    #print(prepared_edges)
    sorted_edges = sorted(prepared_edges.items(), key=operator.itemgetter(1), reverse=True)
    #print(sorted_edges)
    return sorted_edges


def build_sorted_edges(edges, order_importance):
    prepared_edges = {}
    for e in edges:
        #print(edges[e])
        edge = []
        for i in range(len(order_importance)):
            edge.append(edges[e][order_importance[i]])
        prepared_edges[e] = edge
        #print(edge)
    sorted_edges = sort_dict_by_lists(prepared_edges)
    sorted_edges_v = []
    for edge in sorted_edges:
        int_edge = (int(edge[0][0]), int(edge[0][1]))
        sorted_edges_v.append(int_edge)
    return sorted_edges_v


"""
making an object (L1+PROPORTION)
while the first 2 indexes have the drivers id's
"""
def make_object(driver1,driver2):
    driver1_id = driver1[0]
    driver2_id = driver2[0]
    driver1_features = driver1[1:]
    driver2_features = driver2[1:]

    arr_i = np.array(driver1_features, dtype=float)
    arr_j = np.array(driver2_features, dtype=float)
    features_proportion = (np.divide(arr_i, arr_j, out=np.zeros_like(arr_i), where=arr_j != 0))  # handle also divide by zero
    features_proportion = np.round(features_proportion, 2)  # round to 2 digits after the dot
    features_L1 = np.asarray(driver1_features) - np.asarray(driver2_features)

    ids = np.append([driver1_id],[driver2_id])
    features = np.append(features_L1,features_proportion)

    object = np.append(ids,features)
    return object


"""
make the directed, weighted graph G=(V,E)
V contains the drivers id's
E contains the object (specified by two drivers). The direction of e in E is specified by the classification by clf.
the edge (i,j) represents an edge i->j (i beats j, according to clf)
The weight of each e in E is specified by the features of each object, ordering down from the most relevant.
"""
def make_edges(objects, clf):
    E = {}
    for object in objects:
        obj = np.array(object[2:])
        obj = [obj]
        if clf.predict(obj) == 0:
            E[(object[0], object[1])] = object[2:]
        else:
            E[(object[1], object[0])] = object[2:]
    """
    for e in E:
        print(e)
        print(E[e])
    """
    return E

"""
The algorithm:
0. input: G=(V,E) directed with weights on edges [in our case: V = drivers_id, E = objects]
1. make directed graph G'=(V,E'), as E' = None
2. for each e in E, in revert order by weight:
    2.1. if e does not close a cycle:
        2.1.1. add e to E'.
3. Do Topological sort on vertices of G'
4. Return the vertices by the Topological sort

removing cycles (by finding cycles) in https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
Topological sort in https://www.geeksforgeeks.org/topological-sorting/
"""
def get_ordered_vertices(edges, drivers_ids, features_importance):
    order_importance = get_key_order(features_importance)
    # now we need to sort the edges by the feature importance
    # build the features by importance
    # a LIST of the edges (tuple, directed), sorted by weight.
    sorted_edges = build_sorted_edges(edges, order_importance)

    #print(sorted_edges)

    graph = Graph(len(drivers_ids))
    for edge in sorted_edges:
        old_graph = graph
        graph.addEdge(edge[0], edge[1])
        if graph.isCyclic():
            graph = old_graph
    #print(graph.V)
    return graph.topologicalSort()


"""
given a race (drivers list) with the features of each driver and it's id,
the output is the ranking in that race (finish line) - list of drivers ids
"""
def main(drivers_list):
    _, feature_importance, clf = training_testing.train_and_test_with_all_features(84, "BOTH")

    objects = []
    drivers_ids = []
    drivers_keys_exchange = {}

    # we will use the ordering from 0 to len-1 for comfort and afterwards we will exchange again for output.
    for i in range(len(drivers_list)):
        drivers_keys_exchange[i] = drivers_list[i][0]
        drivers_list[i][0] = i

    for i in range(len(drivers_list)-1,0, -1):
        for j in range(i):
            # make and add object
            objects.append(make_object(drivers_list[i],drivers_list[j]))
            # add to drivers_id list
            driver_id1 = int(drivers_list[i][0])
            driver_id2 = int(drivers_list[j][0])
            if driver_id1 not in drivers_ids:
                drivers_ids.append(driver_id1)
            if driver_id2 not in drivers_ids:
                drivers_ids.append(driver_id2)
    #for object in driver_ids:
    #    print(object)

    edges = make_edges(objects, clf)  # is defined by edges
    ordered_vertices = get_ordered_vertices(edges, drivers_ids, feature_importance)

    # exchange the ordered vertices to drivers ids
    for i in range(len(ordered_vertices)):
        ordered_vertices[i] = drivers_keys_exchange[ordered_vertices[i]]
    return ordered_vertices


drivers_list = []
driver = [1,4,3,22,28,4,0,111,7,3]
drivers_list.append(driver)
driver = [2,13,62,117,32,0,7,222,40,3]
drivers_list.append(driver)
driver = [7,12,47,99,30,1,8,212,34,0]
drivers_list.append(driver)

ranking = main(drivers_list)
print(ranking)
