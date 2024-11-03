from haversine_formula import haversine

def create_graph(islands_data):
    graph = {}

    for island in islands_data:
        graph[island['name']] = {}

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

def print_graph(graph):
    for island, edges in graph.items():
        print(f"Edges from {island}:")
        for destination, distance in edges.items():
            if destination != island:
                print(f"  - {destination}: {distance:.2f} km")
        print()