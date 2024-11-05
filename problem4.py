#@Author Kimberly Nguyen
import sys
import heapq
from database import create_db, get_islands_data
from graph import create_graph

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, from_island, to_island, weight):
        if from_island not in self.adjacency_list:
            self.adjacency_list[from_island] = []
        self.adjacency_list[from_island].append((to_island, weight))
        
    def get_neighbors(self, island):
        return self.adjacency_list.get(island, [])

def dijkstra(graph, experiences, start):
    queue = [(0, start, set())]  # (total_time, island_id, experiences_collected)
    visited = {}
    best_experiences = {}
    paths = {start: []}  # Store the path taken to reach each island

    #
    while queue:
        total_time, current, exp_total = heapq.heappop(queue)

        if current in visited and visited[current] <= total_time:
            continue
        visited[current] = total_time
        
        # Update the best experiences for the current island
        best_experiences[current] = exp_total

        # Add new experiences for this island
        current_experiences = experiences.get(current, set())
        new_experiences = exp_total.union(current_experiences)

        for neighbor, travel_time in graph.get_neighbors(current):
            new_time = total_time + travel_time
            
            # If we find a shorter path to the neighbor, update it
            if neighbor not in visited or new_time < visited[neighbor]:
                heapq.heappush(queue, (new_time, neighbor, new_experiences))
                paths[neighbor] = paths[current] + [current]  # Track the path taken

    return visited, best_experiences, paths

def find_optimal_experience(distances, experiences_collected, paths):
    optimal_island = None
    max_experiences = 0
    min_time = sys.maxsize

    for island, time in distances.items():
        experience_count = len(experiences_collected.get(island, set()))
        # Check for the optimal experience collection criteria
        if (experience_count > max_experiences) or (experience_count == max_experiences and time < min_time):
            max_experiences = experience_count
            min_time = time
            optimal_island = island
            
    return optimal_island, max_experiences, min_time, paths[optimal_island] + [optimal_island] if optimal_island else []

def display_islands(islands):
    print("Here is a list of islands: ")
    for index, island in enumerate(islands):
        print(f"  Island #{index + 1}: {island['name']}")
    print()

def main():
    create_db() 
    
    island_data_list = get_islands_data()
    graph = Graph()
    paths = {
        'Hawaii': {'Samoa', 'Tonga', 'New Zealand'},
        'Rapanui': {'Tonga'},
        'New Zealand': {'Samoa', 'Tonga', 'Hawaii'},
        'Samoa': {'Hawaii', 'Tonga'},
        'Tonga': {'Hawaii', 'Samoa', 'New Zealand', 'Rapanui'}
    }

    # Sample experiences with weights
    exps = [
        ('Hawaii', 'Samoa', 1),
        ('Hawaii', 'Tonga', 2),
        ('Hawaii', 'New Zealand', 3),
        ('Rapanui', 'Tonga', 4),
        ('New Zealand', 'Samoa', 2),
        ('New Zealand', 'Tonga', 2),
        ('Samoa', 'Tonga', 1),
        ('Tonga', 'Rapanui', 4),
    ]

    for from_island, to_island, weight in exps:
        graph.add_edge(from_island, to_island, weight)
        graph.add_edge(to_island, from_island, weight)

    # Display islands
    display_islands(island_data_list)

    # User input for starting island
    try:
        starting_island = input("Where would you like to travel to first? ")
        
        # Run Dijkstra's algorithm
        distances, experiences_collected, paths = dijkstra(graph, paths, starting_island)
        
        # Find optimal area to travel to maximize experiences in the least time
        optimal_island, max_experiences, min_time, optimal_path = find_optimal_experience(distances, experiences_collected, paths)
        
        #Shows the path taken
        if optimal_island:
            print(f"The optimal area to travel to for the most experiences in the least amount of time is {optimal_island}.")
            print(f"You can gain {max_experiences} experiences in {min_time} hour(s).")
            print("The path taken to reach this destination is:")
            print(" -> ".join(optimal_path)) 

    except KeyError:
        print("Error! The island you entered does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
