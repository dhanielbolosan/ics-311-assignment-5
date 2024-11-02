from database import create_db, get_islands_data, update_island_data, reset_database, get_resources_data
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
    reset_database()

    # get & print island data
    islands_data = get_islands_data()
    print_island_data(islands_data)

    # create & printing graph
    graph = create_graph(islands_data)
    print_graph(graph)

    # testing changing the database w/ samoa
    samoa = next(island for island in islands_data if island['name'] == 'Samoa')
    original_population = samoa['population']

    if samoa['population'] == original_population:
        samoa['population'] *= 2
        samoa['canoes'] += 50
        update_island_data(samoa['id'], samoa['population'], samoa['canoes'])

    print("\nChanging Samoa's Data...\n\nModified Data for Samoa:")
    print_island_data([samoa])

if __name__ == '__main__':
    main()