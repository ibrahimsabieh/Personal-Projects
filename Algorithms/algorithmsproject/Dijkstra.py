import numpy as np
import time
import resource
from config import dataset
import pandas as pd
from tabulate import tabulate


def dijkstra(adj_matrix, start, end):
    num_nodes = len(adj_matrix)
    distances = [float("inf")] * num_nodes
    predecessors = [None] * num_nodes
    distances[start] = 0

    unvisited = list(range(num_nodes))

    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current_node)

        if current_node == end:
            return distances[end], reconstruct_path(
                predecessors, start, end
            )  # Return distance and path

        for neighbor in range(num_nodes):
            if adj_matrix[current_node][neighbor] > 0:
                distance = distances[current_node] + adj_matrix[current_node][neighbor]

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node

    return (
        float("inf"),
        [],
    )  # Return infinity and an empty path if no path to the end node is found


def reconstruct_path(predecessors, start, end):
    path = []
    while end is not None:
        path.insert(0, end)
        end = predecessors[end]
    return path


def run(testcase, start, end, num_runs=5):
    average_times = []
    average_memory = []
    average_distance = []
    total_nodes = []

    for _ in range(num_runs):
        results = []
        time_start = time.process_time()

        shortest_distance, nodes_traveled = dijkstra(dataset(testcase), start, end)

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
    return (
        # tabulate(df, headers="keys", tablefmt="psql")
        # + f"\nAverage Time: {avg_time:.5f} secs, Average Memory: {avg_mem:.5f} MByte"
        # f"\n{testcase} Shortest Distance Traveled: {int(avg_dis)}"
        f"\n{testcase} Nodes Traveled: {nodes_traveled}"
    )


print(run("Bestcase", 4, 17))
print(run("Worstcase", 6, 24))
print(run("Smallest", 2, 4))
print(run("Longest", 0, 88))
print(run("Blockedcase", 0, 24))
