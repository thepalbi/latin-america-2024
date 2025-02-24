from gem5.components.boards.test_board import TestBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.random_generator import RandomGenerator
from gem5.simulate.simulator import Simulator
from cache import PrivateL1PrivateL2SharedL3CacheHierarchy

from argparse import ArgumentParser

parser = ArgumentParser(description="Select cache hierarchy")
parser.add_argument(
    "--cache",
    choices=["l2", "l3"],
    required=True,
    help="Select the cache hierarchy to use: l2 or l3",
)
parser.add_argument(
    "--max_addr",
    type=int,
    default=256 * 2**10,
    help="Maximum address to generate",
)
args = parser.parse_args()

if args.cache == "l2":
    cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
        l1d_size="32KiB",
        l1i_size="32KiB",
        l2_size="256KiB",
    )
elif args.cache == "l3":
    cache_hierarchy = PrivateL1PrivateL2SharedL3CacheHierarchy(
        l1d_size="32KiB",
        l1d_assoc=8,
        l1i_size="32KiB",
        l1i_assoc=8,
        l2_size="256KiB",
        l2_assoc=4,
        l3_size="512KiB",
        l3_assoc=16,
    )
else:
    raise ValueError("Invalid cache hierarchy selected")

board = TestBoard(
    clk_freq="3GHz",
    generator=RandomGenerator(
        num_cores=1,
        rd_perc=75,
        max_addr=args.max_addr,
        duration="1ms",
    ),
    memory=SingleChannelDDR4_2400(),
    cache_hierarchy=cache_hierarchy,
)

sim = Simulator(board=board)
sim.run()
