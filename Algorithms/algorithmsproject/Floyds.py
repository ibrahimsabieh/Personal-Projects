import numpy as np
import time
import resource
from config import dataset
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt


def floyd_warshall_with_path(adj_matrix):
    num_nodes = len(adj_matrix)
    distances = np.copy(adj_matrix)
    predecessors = np.full((num_nodes, num_nodes), -1, dtype=int)

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    predecessors[i][j] = k  # Store the intermediate node k

    return distances, predecessors


def reconstruct_path(predecessors, start, end):
    if predecessors[start][end] == -1:
        return [start, end]
    intermediate = predecessors[start][end]
    path1 = reconstruct_path(predecessors, start, intermediate)
    path2 = reconstruct_path(predecessors, intermediate, end)
    return path1[:-1] + path2


def run(testcase, start, end):
    count = 0
    ttime = []
    tmem = []
    average_distance = []
    total_nodes = []
    while count < 5:
        count = count + 1
        results = []
        time_start = time.process_time()

        all_shortest_distances, predecessors = floyd_warshall_with_path(
            dataset(testcase)
        )

        shortest_distance = all_shortest_distances[start][end]

        if shortest_distance < float("inf"):
            results.append(f"{start} to {end}: {shortest_distance}")
            shortest_path = reconstruct_path(predecessors, start, end)
            results.append(f"{shortest_path}")

            time_elapsed = time.process_time() - time_start

            memMb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0 / 1024.0
            results.append("{:.5f} secs {:.5f} MByte".format(time_elapsed, memMb))

            df = pd.DataFrame(
                results,
                index=["Shortest Distance", "Nodes Traveled", "Time/Memory"],
                columns=[testcase + " Data"],
            )

            ttime.append(time_elapsed)
            tmem.append(memMb)
            average_distance.append(shortest_distance)
            total_nodes.append(shortest_path)

        else:
            print(f"No path from {start} to {end}")

            time_elapsed = time.process_time() - time_start
            memMb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0 / 1024.0
            results.append("{:.5f} secs {:.5f} MByte".format(time_elapsed, memMb))

    avg_time = sum(ttime) / len(ttime)
    avg_mem = sum(tmem) / len(tmem)
    avg_dis = sum(average_distance) / len(average_distance)
    return (
        # tabulate(df, headers="keys", tablefmt="psql")
        # f"\nAverage Time: {avg_time:.5f} secs, Average Memory: {avg_mem:.5f} MByte"
        # f"\n{testcase} Shortest Distance Traveled: {int(avg_dis)}"
        f"\n{testcase} Nodes Traveled: {shortest_path}"
    )


print(run("Bestcase", 4, 17))
print(run("Worstcase", 6, 24))
print(run("Smallest", 2, 4))
print(run("Longest", 0, 88))
print(run("Blockedcase", 0, 24))
