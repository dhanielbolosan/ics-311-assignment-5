from haversine_formula import haversine

def create_graph(islands_data):
    graph = {}

    for island in islands_data:
        graph[island['name']] = {}

    for i in range(len(islands_data)):
        for j in range(len(islands_data)):
            if i != j:
                island1 = islands_data[i]
                island2 = islands_data[j]

                # Extract coordinates
                lat1, lon1 = island1['latitude'], island1['longitude']
                lat2, lon2 = island2['latitude'], island2['longitude']

                # Correctly calculate distance
                distance = haversine(lat1, lon1, lat2, lon2)

                graph[island1['name']][island2['name']] = distance
                graph[island2['name']][island1['name']] = distance

    return graph
    


def print_graph(graph):
    for island1, edges in graph.items():
        print(f"Edges from {island1}:")
        for island2, distance in edges.items():
            print(f"  - {island2}: {distance:.2f} km")