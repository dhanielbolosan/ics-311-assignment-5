from dijkstra import dijkstra

def distribute_resource(graph, source_island, resource_quantity, canoe_capacity):
    # Calculate shortest paths from source island
    shortest_paths = dijkstra(graph, source_island)
    
    # Sort islands by distance from the source
    sorted_islands = sorted(shortest_paths.items(), key=lambda x: x[1])

    distribution = []
    remaining_resources = resource_quantity

    for island, distance in sorted_islands:
        if island == source_island or remaining_resources <= 0:
            continue

        # Determine how much to distribute to this island
        to_distribute = min(remaining_resources, canoe_capacity)
        
        # Append distribution details to the plan
        distribution.append({
            'to': island,
            'distance': distance,
            'quantity': to_distribute  # Corrected key name to 'quantity'
        })
        remaining_resources -= to_distribute
    
    return distribution