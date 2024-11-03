import heapq

# dijkstra algorithm using min-heap for better performance
def dijkstra(graph, source):
    # initialize distances from source as infinity (distance is currently unknown), source distance as 0, and min heap
    distances = {vertex: float('inf') for vertex in graph}
    distances[source] = 0
    min_heap = [(0, source)]

    visited = set()

    while min_heap:
        # pop vertex w/ smallest distance
        current_distance, current_vertex = heapq.heappop(min_heap)

        # skip if vertex has been visited
        if current_vertex in visited:
            continue 

        # mark vertex as visited
        visited.add(current_vertex)

        # explore neighbors of current vertex
        for neighbor, weight in graph[current_vertex].items():
            # calculate new distance to neighbor
            distance = current_distance + weight

            # update distance if new distance is shorter
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(min_heap, (distance, neighbor))

    return distances