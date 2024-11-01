from data_reader import load_islands_data
from graph import haversine, create_graph, print_graph

def print_data(islands_data):
    for island in islands_data['islands']:
        print(f"Island: {island['name']}")
        print(f"  Latitude: {island['latitude']}")
        print(f"  Longitude: {island['longitude']}")
        print(f"  Population: {island['population']:,}")
        print("  Resources:")
        for resource in island['resources']:
            print(f"    - {resource['resource_name']}: {resource['quantity']}")

def main():
    # loading & printing data
    islands_data = load_islands_data('data.json')
    print_data(islands_data)

    # create & printing graph
    graph = create_graph(islands_data)
    print_graph(graph)

    # testing manipulating .json file
    for island in islands_data['islands']:
        if island['name'] == 'Hawaii':
            island['population'] *= 2
            island['canoes'] += 50

            for resource in island['resources']:
                if resource['resource_name'] == 'Coffee':
                    resource['quantity'] *= 5

    # printing Hawaii's modified data
    for island in islands_data['islands']:
        if island['name'] == 'Hawaii':
            print("\nModified Data for Hawaii:")
            print(f"Island: {island['name']}")
            print(f"  Latitude: {island['latitude']}")
            print(f"  Longitude: {island['longitude']}")
            print(f"  Population: {island['population']:,}")
            print(f"  Canoes: {island['canoes']}")
            print("  Resources:")
            for resource in island['resources']:
                print(f"    - {resource['resource_name']}: {resource['quantity']}")


if __name__ == '__main__':
    main()