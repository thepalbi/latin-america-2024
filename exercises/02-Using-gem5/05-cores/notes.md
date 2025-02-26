With 32KiB L1D and L1I caches

| Configuration       | simSeconds | simTicks     | hostSeconds | IPC       |
|---------------------|------------|--------------|-------------|-----------|
| m5out-atomic        | 0.038158   | 38157658000  | 8.82        | 0.889851  |
| m5out-minor         | 0.040445   | 40445238000  | 34.75       | 0.839521  |
| m5out-o3            | 0.024247   | 24247270000  | 40.20       | 1.400348  |
| m5out-timing        | 0.057480   | 57480330000  | 15.06       | 0.590718  |

Compared to 64KiB cache size for l1d,i

| Configuration       | simSeconds | simTicks     | hostSeconds | IPC       |
|---------------------|------------|--------------|-------------|-----------|
| m5out-atomic        | 0.038158   | 38157658000  | 8.88        | 0.889851  |
| m5out-minor         | 0.037057   | 37056833000  | 33.95       | 0.916285  |
| m5out-o3            | 0.020618   | 20618167000  | 38.97       | 1.646830  |
| m5out-timing        | 0.053616   | 53615686000  | 14.80       | 0.633297  |

Comparing custom sizes of o3:

**IPC**

| Configuration       | IPC       |
|---------------------|-----------|
| m5out-o3big         | 1.400691  |
| m5out-o3little      | 0.714932  |
| m5out-o3            | 1.400348  |

**Times**

| Configuration       | simSeconds | hostSeconds |
|---------------------|------------|-------------|
| m5out-o3big         | 0.024241   | 41.52       |
| m5out-o3little      | 0.047494   | 51.71       |
| m5out-o3            | 0.024247   | 40.58       |

The speedup of big over little is 1.245 # https://en.wikipedia.org/wiki/Speedup
