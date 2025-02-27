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

## custom benchmark

```
pablo@pablok:~/phd/latin-america-2024/exercises/02-Using-gem5/05-cores$ grep "board.processor.cores.core.commitStats0.numOps" m5out-default/* m5out-roi/*
m5out-default/stats.txt:board.processor.cores.core.commitStats0.numOps     41314070                       # Number of ops (including micro ops) committed (thread level) (Count)
m5out-default/stats.txt:board.processor.cores.core.commitStats0.numOpsNotNOP            0                       # Number of Ops (including micro ops) Simulated (Count)
m5out-roi/stats.txt:board.processor.cores.core.commitStats0.numOps            0                       # Number of ops (including micro ops) committed (thread level) (Count)
m5out-roi/stats.txt:board.processor.cores.core.commitStats0.numOpsNotNOP            0                       # Number of Ops (including micro ops) Simulated (Count)
m5out-roi/stats.txt:board.processor.cores.core.commitStats0.numOps            0                       # Number of ops (including micro ops) committed (thread level) (Count)
m5out-roi/stats.txt:board.processor.cores.core.commitStats0.numOpsNotNOP            0                       # Number of Ops (including micro ops) Simulated (Count)
m5out-roi/stats.txt:board.processor.cores.core.commitStats0.numOps       268955                       # Number of ops (including micro ops) committed (thread level) (Count)
m5out-roi/stats.txt:board.processor.cores.core.commitStats0.numOpsNotNOP            0                       # Number of Ops (including micro ops) Simulated (Count)
```

- % of instruction in ROI vs. full benchmark: 0.006510009786012368 ~ 0.65%
- cache hit ratio:
  - ROI
    - l1d: 0,999114794005
    - l2 (ReadExc): 0,652173913043
    - l2 (ReadShared): 0,809701492537

## custom benchmark compared to RISC-V

```
m5out-cc-riscv/stats.txt:board.processor.cores.core.commitStats0.numOps       225053                       # Number of ops (including micro ops) committed (thread level) (Count)
m5out-cc-x86/stats.txt:board.processor.cores.core.commitStats0.numOps       268938                       # Number of ops (including micro ops) committed (thread level) (Count)
```

This represents a 1,19499851146 speedup in amount of instrs

```
# cache numbers under ROI
# RISC-V
m5out-cc-riscv/stats.txt:board.cache_hierarchy.l1dcaches.ReadReq.hits::total        61016                       # number of ReadReq hits (Count)
m5out-cc-riscv/stats.txt:board.cache_hierarchy.l1dcaches.ReadReq.accesses::total        61086                       # number of ReadReq accesses(hits+misses) (Count)
m5out-cc-riscv/stats.txt:board.cache_hierarchy.l2cache.ReadExReq.hits::total           11                       # number of ReadExReq hits (Count)
m5out-cc-riscv/stats.txt:board.cache_hierarchy.l2cache.ReadExReq.accesses::total           21                       # number of ReadExReq accesses(hits+misses) (Count)
m5out-cc-riscv/stats.txt:board.cache_hierarchy.l2cache.ReadSharedReq.hits::total          656                       # number of ReadSharedReq hits (Count)
m5out-cc-riscv/stats.txt:board.cache_hierarchy.l2cache.ReadSharedReq.accesses::total          763                       # number of ReadSharedReq accesses(hits+misses) (Count)

# x86
m5out-cc-x86/stats.txt:board.cache_hierarchy.l1dcaches.ReadReq.hits::total        61064                       # number of ReadReq hits (Count)
m5out-cc-x86/stats.txt:board.cache_hierarchy.l1dcaches.ReadReq.accesses::total        61133                       # number of ReadReq accesses(hits+misses) (Count)
m5out-cc-x86/stats.txt:board.cache_hierarchy.l2cache.ReadExReq.hits::total           17                       # number of ReadExReq hits (Count)
m5out-cc-x86/stats.txt:board.cache_hierarchy.l2cache.ReadExReq.accesses::total           25                       # number of ReadExReq accesses(hits+misses) (Count)
m5out-cc-x86/stats.txt:board.cache_hierarchy.l2cache.ReadSharedReq.hits::total          650                       # number of ReadSharedReq hits (Count)
m5out-cc-x86/stats.txt:board.cache_hierarchy.l2cache.ReadSharedReq.accesses::total          801                       # number of ReadSharedReq accesses(hits+misses) (Count)
```

| Architecture | L1D Hit Ratio       | L2-Ex Hit Ratio       | L2-Shared Hit Ratio       |
|--------------|---------------------|-----------------------|---------------------------|
| RISC-V       | 0.9988540745833743  | 0.5238095238095238    | 0.8597640891218873        |
| x86          | 0.9988713133659398  | 0.68                  | 0.8114856429463171        |
