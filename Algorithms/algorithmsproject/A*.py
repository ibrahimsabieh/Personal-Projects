import heapq
import numpy as np
import time
import resource
from config import dataset
import pandas as pd
from tabulate import tabulate


class Node:
    def __init__(self, index, parent=None, g_cost=float("inf"), h_cost=0):
        self.index = index
        self.parent = parent
        self.g_cost = g_cost
        self.h_cost = h_cost

    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        if self.f_cost() == other.f_cost():
            return self.g_cost > other.g_cost
        return self.f_cost() < other.f_cost()


def astar(adj_matrix, start, end):
    num_nodes = len(adj_matrix)
    open_set = []
    closed_set = set()
    visited_nodes = {}

    start_node = Node(start, None, 0, adj_matrix[start][end])
    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.index == end:
            path = reconstruct_path(current_node, visited_nodes)
            return current_node.g_cost, path

        if current_node.index in closed_set:
            continue

        closed_set.add(current_node.index)
        visited_nodes[current_node.index] = current_node

        for neighbor in range(num_nodes):
            if adj_matrix[current_node.index][neighbor] > 0:
                g_cost = current_node.g_cost + adj_matrix[current_node.index][neighbor]
                h_cost = adj_matrix[neighbor][
                    end
                ]  # Updated heuristic to actual edge cost
                neighbor_node = Node(neighbor, current_node, g_cost, h_cost)

                if neighbor_node.index not in closed_set:
                    heapq.heappush(open_set, neighbor_node)

    return float("inf"), []


def reconstruct_path(node, visited_nodes):
    path = []
    while node is not None:
        path.insert(0, node.index)
        node = node.parent
    return path


def run(testcase, start, end, num_runs=1):
    average_times = []
    average_memory = []
    average_distance = []
    total_nodes = []

    for _ in range(num_runs):
        results = []
        time_start = time.process_time()

        shortest_distance, nodes_traveled = astar(dataset(testcase), start, end)

        if shortest_distance < float("inf"):
            results.append(f"{start} to {end}: {shortest_distance}")
            results.append(f"{nodes_traveled}")

            time_elapsed = time.process_time() - time_start

            memMb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0 / 1024.0
            results.append("{:.5f} secs {:.5f} MByte".format(time_elapsed, memMb))
            df = pd.DataFrame(
                results,
                index=["Shortest Distance", "Nodes Traveled", "Time/Memory"],
                columns=[testcase + " Data"],
            )
            average_times.append(time_elapsed)
            average_memory.append(memMb)
            average_distance.append(shortest_distance)
            total_nodes.append(nodes_traveled)
        else:
            print(f"No path from {start} to {end}")

            time_elapsed = time.perf_counter() - time_start
            memMb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0 / 1024.0
            results.append("{:.5f} secs {:.5f} MByte".format(time_elapsed, memMb))

    avg_time = sum(average_times) / num_runs
    avg_mem = sum(average_memory) / num_runs
    avg_dis = sum(average_distance) / num_runs
    for i in reversed(nodes_traveled):
        trav = []
        trav.append(dataset(testcase)[i])
    return (
        #tabulate(df, headers="keys", tablefmt="psql")
        # f"\nAverage Time: {avg_time:.5f} secs, Average Memory: {avg_mem:.5f} MByte"
        # f"\n{testcase} Shortest Distance Traveled: {int(avg_dis)}"
        # f"\n{trav}"
         f"\n{testcase} Nodes Traveled: {nodes_traveled}"
    )


print(run("Bestcase", 4, 17))
print(run("Worstcase", 6, 24))
print(run("Smallest", 2, 4))
print(run("Longest", 0, 88))
print(run("Blockedcase", 0, 24))
