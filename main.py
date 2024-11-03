from database import create_db, reset_db, get_islands_data, update_island_data, get_resources_data, update_resource_data
from graph import create_graph, print_graph

def print_island_data(islands):
    printed_islands = set()

    for island in islands:
        # print islands & prevent repeating
        if island['name'] not in printed_islands:
            printed_islands.add(island['name'])
            print(f"Island: {island['name']}")
            print(f"  Latitude: {island['latitude']}")
            print(f"  Longitude: {island['longitude']}")
            print(f"  Population: {island['population']:,}")
            print(f"  Canoes: {island['canoes']:,}")
            
            # check & print if resources are available
            resources = get_resources_data(island['id'])
            if resources:
                print("  Resources:")
                for resource in resources:
                    print(f"    - {resource[0]}: {resource[1]:,}")
            else:
                print("  Resources: No resources available")

def main():
    # create & reset database to initial state
    create_db()
    reset_db()

    # get & print island data
    islands_data = get_islands_data()
    print_island_data(islands_data)

    # create & printing graph
    graph = create_graph(islands_data)
    print_graph(graph)

   # testing changing an island data w/ samoa
    samoa = next(island for island in islands_data if island['name'] == 'Samoa')

    # update Samoa's population and canoes
    samoa['population'] *= 2
    samoa['canoes'] += 50
    update_island_data(samoa['id'], samoa['population'], samoa['canoes'])

    # update resource quantity
    resources = get_resources_data(samoa['id'])
    coconut_quantity = next((quantity for name, quantity in resources if name == "Coconut"), 0)
    update_resource_data(samoa['id'], "Coconut", coconut_quantity + 1000)

    print("\nChanging Samoa's Data...\n\nModified Data for Samoa:")
    print_island_data([samoa])

if __name__ == '__main__':
    main()
