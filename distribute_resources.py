from dijkstra import dijkstra

'''
used for problem #2,
distributes resources from a source island to other islands equally while taking into account the canoe capacity and number of canoes sent
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

        # determine quantity to send
        send_quantity = min(quantity_per_destination, remaining_quantity)

        # calculate how many canoes are needed to be send
        canoes_sent = (send_quantity + canoe_capacity - 1) // canoe_capacity

        # calculate actual quantity that can be sent with the available canoes
        actual_send_quantity = min(send_quantity, canoes_sent * canoe_capacity)

        distribution.append({
            'destination': destination,
            'distance': distance,
            'quantity': send_quantity,
            'canoes_sent': canoes_sent
        })

        remaining_quantity -= actual_send_quantity

    return distribution