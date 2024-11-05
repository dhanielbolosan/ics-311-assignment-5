# https://www.geeksforgeeks.org/python-itertools-combinations-function/
from itertools import combinations
from tools.haversine_formula import haversine

# creates the graph used for the problems
def create_graph(islands_data):
    graph = {}

    # populate graph with islands
    for island in islands_data:
        graph[island['name']] = {}

    # use itertools combinations to create unique pairs of islands
    for island1, island2 in combinations(islands_data, 2):
        # extract coordinates for two islands
        lat1, long1 = island1['latitude'], island1['longitude']
        lat2, long2 = island2['latitude'], island2['longitude']

        # calculate distance between two islands using haversine
        distance = haversine(lat1, long1, lat2, long2)

        graph[island1['name']][island2['name']] = distance
        graph[island2['name']][island1['name']] = distance
    
    return graph

    '''
    # faster way to implement this?
    for i in range(len(islands_data)):
        for j in range(len(islands_data)):
            if i != j:
                island1 = islands_data[i]
                island2 = islands_data[j]

                # extract coordinates
                lat1, lon1 = island1['latitude'], island1['longitude']
                lat2, lon2 = island2['latitude'], island2['longitude']

                # calculate distance
                distance = haversine(lat1, lon1, lat2, lon2)

                graph[island1['name']][island2['name']] = distance
                graph[island2['name']][island1['name']] = distance

    return graph
    '''

def print_graph(graph):
    for island, edges in graph.items():
        print(f"Edges from {island}:")
        sorted_edges = sorted(edges.items(), key=lambda x: x[1])
        for destination, distance in sorted_edges:
            if destination != island:
                print(f"  - {destination}: {distance:.2f} km")
        print()