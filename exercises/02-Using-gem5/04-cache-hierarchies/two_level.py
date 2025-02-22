from gem5.components.boards.test_board import TestBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.random_generator import RandomGenerator
from gem5.simulate.simulator import Simulator

max_addr = 256 * 2**10
board = TestBoard(
  clk_freq="3GHz",
  generator=RandomGenerator(
    num_cores=1,
    rd_perc=75,
    max_addr=max_addr,
    duration="1ms",
  ),
  memory=SingleChannelDDR4_2400(), # understand better the total size of these devices, but it seems the default for the dual channel is 32GiB
  cache_hierarchy=PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB",
    l1i_size="32KiB",
    l2_size="256KiB",
  ),
)

sim = Simulator(board=board)
sim.run()

