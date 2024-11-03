#interactive program for problem #2
from database import create_db, reset_db, get_islands_data, update_island_data, get_resources_data, update_resource_data
from graph import create_graph, print_graph
from distribute_resources import distribute_resource

def display_islands(islands):
    print("Islands:")
    for index, island in enumerate(islands):
        print(f"  {index + 1}. {island['name']}")

def display_resources(island):
    resources = get_resources_data(island['id'])
    if resources:
        print(f"Resources on {island['name']}:")
        for index, resource in enumerate(resources):
            print(f"{index + 1}. {resource[0]}: {resource[1]:,} kgs")
        else: print(f"No resources available on {island['name']}")

def main():
    create_db()
    reset_db()

    islands_data = get_islands_data()
    graph = create_graph(islands_data)

    while True:
        display_islands(islands_data)

        try:
            island_choice = int(input("Choose an island to distribute resources:"))
            source_island = islands_data[island_choice - 1]
            print(f"Selected island: {source_island['name']}")

            display_resources(source_island)
            resource_choice = int(input("Choose a resource to distribute:"))
            resource_name, initial_quantity = get_resources_data(source_island['id'])[resource_choice - 1]
            print(f"Selected resource: {resource_name} (Quantity: {initial_quantity:,} kgs)")

            canoe_capacity = source_island['canoe_capacity']
            if initial_quantity <= 0:
                print("No resources to distribute.")
                continue

            distribution = distribute_resource(graph, source_island['name'], initial_quantity, canoe_capacity)

            print("Distributing:")
            for entry in distribution:
                print(f"Sending {entry['quantity']:,} kgs to {entry['destination']} (Distance: {entry['distance']:.2f} km)")
                
        except (ValueError, IndexError):
            print("Invalid input. Please try again.")
            continue

if __name__ == "__main__":
    main()