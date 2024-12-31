import matplotlib.pyplot as plt
import numpy as np

# Data
cases = ["Bestcase", "Blocked", "Longest", "Smallest", "Worstcase"]
algorithms = ["A*", "Dijkstra", "Floyd's"]

# Average Time and Memory data for each algorithm and case
average_time = {
    "A*": [0.00199, 0.00113, 0.00243, 0.00141, 0.00108],
    "Dijkstra": [0.00220, 0.00049, 0.01029, 0.00035, 0.00067],
    "Floyd's": [0.00527, 0.00585, 0.33282, 0.00039, 0.00570],
}

average_memory = {
    "A*": [84.575, 84.64062, 84.64062, 84.64062, 84.63438],
    "Dijkstra": [84.1375, 84.3875, 84.29375, 84.1875, 84.1875],
    "Floyd's": [105.7, 105.85938, 105.85938, 105.85938, 105.83437],
}

# Create the line graph
fig, ax1 = plt.subplots(figsize=(12, 6))

ax2 = ax1.twinx()

colors = ["b", "g", "r"]

for i, algo in enumerate(algorithms):
    time_data = average_time[algo]
    memory_data = average_memory[algo]

    ax1.plot(cases, time_data, marker="o", label=f"{algo} (Time)", color=colors[i])
    ax2.plot(
        cases,
        memory_data,
        marker="x",
        label=f"{algo} (Memory)",
        color=colors[i],
        linestyle="--",
    )

# Order the x-axis as specified
ax1.set_xticks(np.arange(len(cases)))
ax1.set_xticklabels(cases, fontsize=16)  # Set the font size for the x-axis labels

# Set memory increments on the y-axis and adjust the maximum value
ax2.set_yticks(np.arange(70, 121, 5))
ax2.set_ylim(70, 120)

# Increase font size
ax1.set_xlabel("Cases", fontsize=18)
ax1.set_ylabel("Average Time (secs)", fontsize=18, color="black")
ax2.set_ylabel("Average Memory (MByte)", fontsize=18, color="black")
ax1.set_title("Average Time and Memory Usage for Different Algorithms", fontsize=18)
ax1.legend(fontsize=14, loc="upper left")
ax2.legend(fontsize=14, loc="upper right")

plt.grid(True)
plt.show()
