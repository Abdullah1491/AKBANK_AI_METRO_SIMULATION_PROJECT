from collections import defaultdict, deque
from typing import List, Tuple, Dict, Optional
import heapq

#  The Station class represents each metro station.
class Station:
    def __init__(self, idx: str, name: str, line: str):
        self.idx = idx
        self.name = name
        self.line = line
        self.neighbors: List[Tuple['Station', int]] = [] # Neighboring stations and the time between them

    # Adds a new neighboring station (along with the travel time between the two stations)
    def add_neighbor(self, station: 'Station', time: int):
        self.neighbors.append((station, time))

# Class that manages the metro network
class MetroNetwork:
    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.lines: Dict[str, List[Station]] = defaultdict(list)

    # Adds a new station
    def add_station(self, idx: str, name: str, line: str) -> None:
        if idx not in self.stations:
            station = Station(idx, name, line)
            self.stations[idx] = station
            self.lines[line].append(station)

    # Adds a connection between two stations (along with the travel time)
    def add_connection(self, station1_id: str, station2_id: str, time: int) -> None:
        station1 = self.stations[station1_id]
        station2 = self.stations[station2_id]
        station1.add_neighbor(station2, time)
        station2.add_neighbor(station1, time)

    # Calculates the average travel time for a specified line
    def get_line_average_time(self, line: str) -> float:
        stations = self.lines[line]
        total_time = 0
        num_segments = len(stations) - 1
        if num_segments <= 0:
            return 0
        
        # Sum the time between consecutive stations on the line.
        for i in range(len(stations)-1):
            current = stations[i]
            next_station = stations[i+1]
            for neighbor, time in current.neighbors:
                if neighbor == next_station:
                    total_time += time
                    break
        return total_time / num_segments
    
    # Heuristic function that estimates the distance between two stations.
    def heuristic(self, current: Station, target: Station) -> int:
        if current.line == target.line:
            try:
                line_stations = self.lines[current.line]
                current_idx = line_stations.index(current)
                target_idx = line_stations.index(target)
                avg_time = self.get_line_average_time(current.line)
                return int(abs(current_idx - target_idx) * avg_time)
            except ValueError:
                return 0
        else:
            min_transfer = float('inf')
            for neighbor, time in current.neighbors:
                if neighbor.line == target.line:
                    transfer_time = time + self.heuristic(neighbor, target)
                    if transfer_time < min_transfer:
                        min_transfer = transfer_time
            return min_transfer if min_transfer != float('inf') else 0
        
    # Finds a route with the minimum number of transfers (Breadth-First Search - BFS).
    def find_min_transfers(self, start_id: str, target_id: str) -> Optional[List[Station]]:
        if start_id not in self.stations or target_id not in self.stations:
            return None
        
        start = self.stations[start_id]
        target = self.stations[target_id]
        
        queue = deque([(start, [start])])             # Queue for BFS (station, path taken so far).
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            if current == target:                     # Return the path when the destination is reached.
                return path
            
            for neighbor, _ in current.neighbors:
                if neighbor not in visited:           # Add unvisited stations.
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return None        # Return None if the destination cannot be reached.
                        
    # Algorithm to find the fastest route (A* Algorithm).
    def find_fastest_route(self, start_id: str, target_id: str) -> Optional[Tuple[List[Station], int]]:
        if start_id not in self.stations or target_id not in self.stations:
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]
        
        def h(station: Station) -> int:
            return self.heuristic(station, target)

        heap = []
        heapq.heappush(heap, (0 + h(start), id(start), start, [start], 0))
        best_cost = {id(start): 0}      # Store the best-known costs.
        
        while heap:
            current_priority, _, current, path, total_time = heapq.heappop(heap)
            
            if current == target:
                return (path, total_time)
            
            if total_time > best_cost.get(id(current), float('inf')):
                continue
            
            for neighbor, time in current.neighbors:
                new_time = total_time + time
                if id(neighbor) not in best_cost or new_time < best_cost[id(neighbor)]:
                    best_cost[id(neighbor)] = new_time
                    new_path = path + [neighbor]
                    priority = new_time + h(neighbor)
                    heapq.heappush(heap, (priority, id(neighbor), neighbor, new_path, new_time))
        
        return None         # Return None if the destination cannot be reached.

# Example Usage
if __name__ == "__main__":
    metro = MetroNetwork()
    
    # Adding Stations
    # Red Line
    metro.add_station("K1", "Kızılay", "Red Line")
    metro.add_station("K2", "Ulus", "Red Line")
    metro.add_station("K3", "Demetevler", "Red Line")
    metro.add_station("K4", "OSB", "Red Line")
    
    # Blue Line
    metro.add_station("M1", "AŞTİ", "Blue Line")
    metro.add_station("M2", "Kızılay", "Blue Line")
    metro.add_station("M3", "Sıhhiye", "Blue Line")
    metro.add_station("M4", "Gar", "Blue Line")
    
    # Orange Line
    metro.add_station("T1", "Batıkent", "Orange Line")
    metro.add_station("T2", "Demetevler", "Orange Line")
    metro.add_station("T3", "Gar", "Orange Line")
    metro.add_station("T4", "Keçiören", "Orange Line")
    
    # Adding connections
    # Red Line
    metro.add_connection("K1", "K2", 4)
    metro.add_connection("K2", "K3", 6)
    metro.add_connection("K3", "K4", 8)
    
    # Blue Line
    metro.add_connection("M1", "M2", 5)
    metro.add_connection("M2", "M3", 3)
    metro.add_connection("M3", "M4", 4)
    
    # Orange Line
    metro.add_connection("T1", "T2", 7)
    metro.add_connection("T2", "T3", 9)
    metro.add_connection("T3", "T4", 5)
    
    # Transfer Connections
    metro.add_connection("K1", "M2", 2)
    metro.add_connection("K3", "T2", 3)
    metro.add_connection("M4", "T3", 2)
    
    # Test scenarios
    print("\n=== Test Senaryoları ===")
    
    # Scenario 1: AŞTİ to OSB
    print("\n1. AŞTİ to OSB:")
    route = metro.find_min_transfers("M1", "K4")
    if route:
        print("Minimum transfer route:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("M1", "K4")
    if result:
        route, time = result
        print(f"Fastest route ({time} minutes):", " -> ".join(i.name for i in route))
    
    # Scenario 2: Batıkent to Keçiören
    print("\n2. Batıkent to Keçiören:")
    route = metro.find_min_transfers("T1", "T4")
    if route:
        print("Minimum transfer route:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("T1", "T4")
    if result:
        route, time = result
        print(f"Fastest route ({time} minutes):", " -> ".join(i.name for i in route))
    
    # Scenario 3: Keçiören to AŞTİ
    print("\n3. Keçiören to AŞTİ:")
    route = metro.find_min_transfers("T4", "M1")
    if route:
        print("Minimum transfer route:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("T4", "M1")
    if result:
        route, time = result
        print(f"Fastest route ({time} minutes):", " -> ".join(i.name for i in route))