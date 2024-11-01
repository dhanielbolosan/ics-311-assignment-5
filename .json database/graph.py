import math

# https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
def haversine(lat1, lon1, lat2, lon2):

    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def create_graph(islands_data):
    graph = {}
    islands = islands_data['islands']

    for island in islands: graph[island['name']] = {}

    for i in range(len(islands)):
        for j in range(len(islands)):
            if i != j:
                island1 = islands[i]
                island2 = islands[j]
                distance = haversine(island1['latitude'], island1['longitude'], island2['latitude'], island2['longitude'])

                graph[island1['name']][island2['name']] = distance

                graph[island2['name']][island1['name']] = distance
    
    return graph


def print_graph(graph):
    for island1, edges in graph.items():
        print(f"Edges from {island1}:")
        for island2, distance in edges.items():
            print(f"  - {island2}: {distance:.2f} km")