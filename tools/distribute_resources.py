from tools.dijkstra import dijkstra

'''
used for problem #2,
distributes resources from a source island to other islands equally
'''
def distribute_resource(graph, source_island, total_quantity, canoe_capacity):
    distribution = []
    remaining_quantity = total_quantity
    source_data = graph[source_island]

    # sorted list of destinations based on distance
    sorted_destinations = sorted(
        ((destination, distance) for destination, distance in source_data.items() if destination != source_island),
        key=lambda x: x[1]
    )

    # calculate number of destinations & quantity per destination
    num_destinations = len(sorted_destinations)
    quantity_per_destination = remaining_quantity / num_destinations if num_destinations > 0 else 0

    # iterate through each destination and distribute
    for destination, distance in sorted_destinations:
        if remaining_quantity <= 0:
            break
        
        send_quantity = min(quantity_per_destination, canoe_capacity, remaining_quantity)
        
        distribution.append({
            'destination': destination,
            'distance': distance,
            'quantity': send_quantity
        })

        remaining_quantity -= send_quantity

    return distribution