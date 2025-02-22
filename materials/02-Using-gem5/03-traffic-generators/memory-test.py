"""
This script creates a simple system with a traffic generator to test memory

$ gem5 memory-test.py
"""

import argparse

from gem5.components.boards.test_board import TestBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.simple import SingleChannelSimpleMemory
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.memory.multi_channel import ChanneledMemory
from gem5.components.memory.dram_interfaces.lpddr5 import (
    LPDDR5_6400_1x16_BG_BL32,
)
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.components.processors.random_generator import RandomGenerator
from gem5.simulate.simulator import Simulator

parser = argparse.ArgumentParser()
parser.add_argument("--rate", type=str, help="Rate of the generator.")
parser.add_argument(
    "--rd_pct", type=int, help="Read request percentage of the generator."
)
args = parser.parse_args()

memory = SingleChannelSimpleMemory(
    latency="20ns",
    bandwidth="32GB/s",
    latency_var="0s",
    size="1GiB",
)
board = TestBoard(
    clk_freq="3GHz",
    generator=LinearGenerator(
        num_cores=1,
        rate=args.rate,
        rd_perc=args.rd_pct,
    ),
    memory=memory,
    cache_hierarchy=NoCache(),
)

simulator = Simulator(board=board)
simulator.run()
stats = simulator.get_simstats()
seconds = stats.simTicks.value / stats.simFreq.value
total_bytes = (
    stats.board.processor.cores[0].generator.bytesRead.value
    + stats.board.processor.cores[0].generator.bytesWritten.value
)
latency = (
    stats.board.processor.cores[0].generator.totalReadLatency.value
    / stats.board.processor.cores[0].generator.totalReads.value
)
print(f"Total bandwidth: {total_bytes / seconds / 2**30:0.2f} GiB/s")
print(f"Average latency: {latency / stats.simFreq.value * 1e9:0.2f} ns")
