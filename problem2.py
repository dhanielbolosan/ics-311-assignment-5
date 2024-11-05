# interactive program for problem #2
from tools.database import create_db, reset_db, get_islands_data, update_island_data, get_resources_data, update_resource_data
from tools.graph import create_graph, print_graph
from tools.distribute_resources import distribute_resource

# print islands
def display_islands(islands):
    print("Islands:")
    for index, island in enumerate(islands):
        print(f"  {index + 1}. {island['name']}")
    print()

# print resources of an island
def display_resources(island):
    resources = get_resources_data(island['id'])
    if resources:
        print(f"Resources on {island['name']}:")
        for index, resource in enumerate(resources):
            print(f"    {index + 1}. {resource[0]}: {resource[1]:,} kgs")
    else: print(f"No resources available on {island['name']}")
    print()

def main():
    # create & reset database to initial state
    create_db()
    reset_db()

    # create island data and graph
    islands_data = get_islands_data()
    graph = create_graph(islands_data)

    display_islands(islands_data)

    # get user input
    try:
        # select an island
        island_choice = int(input("Choose an island to distribute resources: "))
        source_island = islands_data[island_choice - 1]
        print(f"Selected island: {source_island['name']}")

        print()
        display_resources(source_island)
        
        # select a resource
        resource_choice = int(input("Choose a resource to distribute: "))
        resource_name, initial_quantity = get_resources_data(source_island['id'])[resource_choice - 1]
        print(f"Selected resource: {resource_name}")

        # get canoe capacity & distribute resources
        canoe_capacity = source_island['canoe_capacity']
        distribution = distribute_resource(graph, source_island['name'], initial_quantity, canoe_capacity)

        # print results
        print(f"\nDistributing {initial_quantity:,} kgs of {resource_name} from {source_island['name']}, Canoes used: {int(distribution[0]['canoes_sent'])}")
        for entry in distribution:
            print(f"Sending {entry['quantity']:.2f} kgs to {entry['destination']} (Distance: {entry['distance']:.2f} km)")

    # handle exceptions     
    except (ValueError, IndexError):
            print("Invalid input. Please try again.")
