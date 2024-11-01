from haversine import haversine

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