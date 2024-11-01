from data_reader import load_islands_data
import math

# https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
def haversine(lat1, lon1, lat2, lon2):

    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def print_data(islands_data):
    for island in islands_data['islands']:
        print(f"Island: {island['name']}")
        print(f"  Latitude: {island['latitude']}")
        print(f"  Longitude: {island['longitude']}")
        print(f"  Population: {island['population']:,}")
        print("  Resources:")
        for resource in island['resources']:
            print(f"    - {resource['resource_name']}: {resource['quantity']}")

def distance(islands_data):
    islands = islands_data['islands']
    for i in range(len(islands)):
        for j in range(i + 1, len(islands)):
            island1 = islands[i]
            island2 = islands[j]
            distance = haversine(island1['latitude'], island1['longitude'], island2['latitude'], island2['longitude'])
            print(f"Distance between {island1['name']} and {island2['name']}: {distance:.2f} km")

def main():
    islands_data = load_islands_data('data.json')
    print_data(islands_data)
    distance(islands_data)

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