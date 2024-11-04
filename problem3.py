
# ICS 311 Assignment 5
# Problem 3
# Author: Sujung Nam

from tools.database import create_db, reset_db, get_islands_data, update_island_data, get_resources_data, update_resource_data
from tools.graph import create_graph, print_graph
from tools.distribute_resources import distribute_resource
from typing import Dict
from typing import List

class NodeExtraData:
    """
    Extra data to store with each node (island)
    """
    def __init__(self):
        self.index = -1

    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index

class Island:
    """
    Class that represents each island
    """
    def __init__(self, name: str, population: int, resources: Dict[str, int], num_canoes: int):
        self.name = name
        self.routes_from_island = []
        self.population = population
        self.resources = resources
        self.num_canoes = num_canoes
        self.node_extra_data = NodeExtraData()

    def add_route(self, route) -> None:
        self.routes_from_island.append(route)

    def get_name(self) -> str:
        return self.name

    def get_routes_from_island(self) -> List:
        return self.routes_from_island

    def get_population(self) -> int:
        return self.population

    def get_resources(self) -> Dict[str, int]:
        return self.resources

    def get_num_canoes(self) -> int:
        return self.num_canoes

    def get_node_extra_data(self) -> NodeExtraData:
        return self.node_extra_data

    def print(self):
        print(f'> Printing island, name={self.name}, population={self.get_population()}')
        for route in self.get_routes_from_island():
            print(f'  Destination name={route.get_destination().get_name()}, dist={route.get_distance()}')

class Route:
    """
    Class that represents a route from one island to another.
    """
    def __init__(self, source: Island, destination: Island, distance: int):
        self.source = source
        self.destination = destination
        self.distance = distance

    def get_source(self):
        return self.source

    def get_destination(self):
        return self.destination

    def get_distance(self):
        return self.distance

    def print(self):
        print(f'> Printing route, source_name={self.get_source().get_name()}, destination_name={self.get_destination().get_name()}, distance={self.get_distance()}')

class Graph:
    """
    Class that represents the graph of islands and routes.
    """
    def __init__(self):
        self.islands: List[Island] = []
        self.routes: List[Route] = []
        self.islands_dict: Dict[str, Island] = {}
        self.routes_dict: Dict[str, Dict[str, Route]] = {}

    def add_island(self, island: Island):
        island_index = len(self.islands)
        island.get_node_extra_data().set_index(island_index)
        self.islands.append(island)
        self.islands_dict[island.get_name()] = island

    def add_route(self, route: Route):
        self.routes.append(route)
        self.get_island(route.get_source().get_name()).add_route(route)
        source_name = route.get_source().get_name()
        destination_name = route.get_destination().get_name()
        if source_name not in self.routes_dict:
            self.routes_dict[source_name] = {}
        self.routes_dict[source_name][destination_name] = route

    def get_islands(self) -> List[Island]:
        return self.islands

    def get_routes(self) -> List[Route]:
        return self.routes

    def get_island(self, name: str) -> Island:
        return self.islands_dict[name]

    def get_island_at_index(self, index: int) -> Island:
        return self.islands[index]

    def get_route(self, source_name: str, destination_name: str) -> Route:
        if source_name in self.routes_dict:
            if destination_name in self.routes_dict[source_name]:
                return self.routes_dict[source_name][destination_name]
        return None

    def print(self):
        print('> Printing graph')
        for island in self.islands:
            island.print()
        for route in self.routes:
            route.print()

class TestData1:
    def __init__(self):
        self.graph = Graph()
        # Add islands
        island_a = Island("A", 100, {"coffee": 10}, 2)
        island_b = Island("B", 200, {"apple": 20}, 0)
        island_c = Island("C", 300, {"banana": 30}, 0)
        island_d = Island("D", 400, {"orange": 40}, 0)
        island_e = Island("E", 500, {"kiwi": 50}, 0)
        islands = [island_a, island_b, island_c, island_d, island_e]
        for island in islands:
            self.graph.add_island(island)
        # Add routes
        route_from_a_to_b = Route(island_a, island_b, 10)
        route_from_a_to_c = Route(island_a, island_c, 15)
        route_from_c_to_d = Route(island_c, island_d, 25)
        route_from_d_to_a = Route(island_d, island_a, 30)
        route_from_d_to_e = Route(island_d, island_e, 35)
        routes = [route_from_a_to_b, route_from_a_to_c, route_from_c_to_d, route_from_d_to_a, route_from_d_to_e]
        for route in routes:
            self.graph.add_route(route)

    def get_graph(self):
        return self.graph

    def print(self):
        self.graph.print()

class Problem3Solver:
    """
    Class for solving problem 3.
    """
    def __init__(self, graph: Graph, source: Island, resource_time: int, num_canoes: int):
        self.graph = graph
        self.source = source
        self.resource_time = resource_time
        self.num_canoes = num_canoes
        # Output of Floyd-Warshall algorithm
        self.dist = []
        self.prev = []

    def run_floyd_warshall(self):
        # Floyd-Warshall algorithm, which computes the shortest distance from every pair of nodes, and also the
        # shortest path.
        # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
        dist: List[List[int]] = []
        prev: List[List[Island]] = []
        islands = self.graph.get_islands()
        num_islands = len(islands)
        for i in range(num_islands):
            l1 = []
            l2 = []
            for j in range(num_islands):
                l1.append(None)
                l2.append(None)
            dist.append(l1)
            prev.append(l2)

        routes = self.graph.get_routes()
        for route in routes:
            source = route.get_source()
            destination = route.get_destination()
            source_index = source.get_node_extra_data().get_index()
            destination_index = destination.get_node_extra_data().get_index()
            dist[source_index][destination_index] = route.get_distance()
            prev[source_index][destination_index] = source
        for island in islands:
            island_index = island.get_node_extra_data().get_index()
            dist[island_index][island_index] = 0
            prev[island_index][island_index] = island
        for k in range(num_islands):
            for i in range(num_islands):
                for j in range(num_islands):
                    if dist[i][k] is not None and dist[k][j] is not None:
                        if dist[i][j] is None or dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            prev[i][j] = prev[k][j]
        self.dist = dist
        self.prev = prev

    def get_path(self, source: Island, destination: Island):
        source_index = source.get_node_extra_data().get_index()
        destination_index = destination.get_node_extra_data().get_index()
        if self.prev[source_index][destination_index] is None:
            return []
        path: List[Island] = [destination]
        while source is not destination:
            destination = self.prev[source_index][destination.get_node_extra_data().get_index()]
            path.append(destination)
        path.reverse()
        return path

    def solve(self):
        # Run Floyd Warshall
        self.run_floyd_warshall()
        # Sort the islands to visit by round-trip time (increasing)
        target_islands_trip_data_list = []
        islands = self.graph.get_islands()
        num_islands = len(islands)
        source_index = self.source.get_node_extra_data().get_index()
        for island_index in range(num_islands):
            if island_index == source_index:
                continue
            round_trip_distance = self.dist[source_index][island_index]
            if self.dist[island_index][source_index] is None:
                round_trip_distance = None
            elif round_trip_distance is not None:
                round_trip_distance += self.dist[island_index][source_index]
            if round_trip_distance is None:
                round_trip_distance = float('inf')
            island = self.graph.get_island_at_index(island_index)
            target_islands_trip_data_list.append((island, round_trip_distance, self.get_path(self.source, island), self.get_path(island, self.source), self.dist[source_index][island_index] is not None, self.dist[island_index][source_index] is not None))
        target_islands_trip_data_list.sort(key=lambda t : t[1])

        # Print solution
        print()
        print('> Printing the order of islands to send the resource (in increasing order of round-trip time)')
        available_canoes_counter = self.num_canoes
        visitable_islands = [self.graph.get_island_at_index(source_index).get_name()]
        for i in range(len(target_islands_trip_data_list)):
            target_island_trip_data = target_islands_trip_data_list[i]
            target_island = target_island_trip_data[0]
            target_island_name = target_island.get_name()
            target_island_distance_to_island = self.dist[source_index][target_island.get_node_extra_data().get_index()]
            target_island_round_trip_distance = target_island_trip_data[1]
            target_island_path_to_island = [e.get_name() for e in target_island_trip_data[2]]
            target_island_path_from_island = [e.get_name() for e in target_island_trip_data[3]]
            can_reach_target_island = target_island_trip_data[4]
            can_come_back_from_target_island = target_island_trip_data[5]
            if not can_reach_target_island:
                print(f'Unreachable island: {target_island_name}')
            elif not can_come_back_from_target_island:
                if available_canoes_counter == 0:
                    print(f'Unreachable island due to no remaining canoes: {target_island_name}')
                else:
                    available_canoes_counter -= 1
                    print(f'{i + 1}. Sending resource to target island {target_island_name} (round-trip distance: {target_island_round_trip_distance})\n  (Distance to island: {target_island_distance_to_island}, Path to island: {target_island_path_to_island}, Path from island: {target_island_path_from_island})')
                    print()
                    visitable_islands.append(target_island_name)
            else:
                print(
                    f'{i + 1}. Sending resource to target island {target_island_name} (round-trip distance: {target_island_round_trip_distance})\n  (Distance to island: {target_island_distance_to_island}, Path to island: {target_island_path_to_island}, Path from island: {target_island_path_from_island})')
                print()
                visitable_islands.append(target_island_name)

        # Summarize
        print('> Printing summary')
        print(f'  Order of islands where the resource reached: {visitable_islands}')
        not_covered_island_names = set()
        for island in islands:
            not_covered_island_names.add(island.get_name())
        for visitable_island in visitable_islands:
            not_covered_island_names.remove(visitable_island)
        if len(not_covered_island_names) > 0:
            print(f'  Islands that the resource could not be distributed to: {list(not_covered_island_names)}')

def solve_problem_3_test():
    test_data_1 = TestData1()
    graph = test_data_1.get_graph()
    solver = Problem3Solver(graph, graph.get_island("A"), 10, 2)
    solver.solve()

def get_graph_from_database(island_data_list, distances_data):
    graph = Graph()
    for island_data in island_data_list:
        resource_data_list = get_resources_data(island_data['id'])
        resources = {}
        for resource_data in resource_data_list:
            resources[resource_data[0]] = resource_data[1]
        island = Island(island_data['name'], island_data['population'], resources, island_data['canoes'])
        graph.add_island(island)

    for source_island_name in distances_data:
        for destination_island_name in distances_data[source_island_name]:
            route = Route(graph.get_island(source_island_name), graph.get_island(destination_island_name), distances_data[source_island_name][destination_island_name])
            graph.add_route(route)

    return graph

def display_islands(islands):
    print("> Displaying islands:")
    for index, island in enumerate(islands):
        print(f"  Island #{index + 1}: {island['name']}")
    print()

def solve_problem_3():
    print('Solving problem #3, using Floyd-Warshall algorithm')

    try:
        # Initialize database
        create_db()
        reset_db()

        # Create graph
        island_data_list = get_islands_data()
        distances_data = create_graph(island_data_list)
        graph = get_graph_from_database(island_data_list, distances_data)
        display_islands(island_data_list)

        # Process user input
        source_island_name = input('> (1/3) Enter the source island name (e.g., Hawaii, or Samoa): ')
        resource_prep_time = int(input('> (2/3) Enter the time it takes for a resource to be ready (e.g., 1000): '))
        num_canoes = int(input('> (3/3) Enter the number of canoes (e.g., 2): '))

        # Solve
        solver = Problem3Solver(graph, graph.get_island(source_island_name), resource_prep_time, num_canoes)
        solver.solve()
    except (ValueError, IndexError):
        print("Invalid input. Please try again.")

if __name__ == '__main__':
    solve_problem_3()
