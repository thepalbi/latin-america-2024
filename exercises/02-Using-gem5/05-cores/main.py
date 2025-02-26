import argparse
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from processors import BigProcessor, LittleProcessor

parser = argparse.ArgumentParser()
parser.add_argument("--cpu-type", dest="cpu_type", choices=["o3", "o3little", "o3big"], required=True, help="CPU type to simulate.")
parser.add_argument("--caches-size", dest="cachesize", type=str, required=True, help="Size of the l1d and l1i caches.")
args = parser.parse_args()


match args.cpu_type:
  case "o3big":
    proc = BigProcessor()
  case "o3little":
    proc = LittleProcessor()
  case "o3":
    proc = SimpleProcessor(
      cpu_type=CPUTypes.O3,
      isa=ISA.RISCV,
      num_cores=1,
    )
  case _:
    raise ValueError("Invalid CPU type selected")


workload = obtain_resource("riscv-matrix-multiply-run")

board = SimpleBoard(
  clk_freq="1GHz",
  processor=proc,
  memory=SingleChannelDDR4_2400(),
  cache_hierarchy=PrivateL1CacheHierarchy(
    l1d_size=args.cachesize,
    l1i_size=args.cachesize,
  ),
)
board.set_workload(workload)
sim = Simulator(board)
sim.run()
