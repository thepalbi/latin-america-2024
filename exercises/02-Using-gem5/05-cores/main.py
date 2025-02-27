import argparse
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource, obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
import m5
from processors import BigProcessor, LittleProcessor

parser = argparse.ArgumentParser()
parser.add_argument("--cpu-type", dest="cpu_type", choices=["o3", "o3little", "o3big", "timing"], required=True, help="CPU type to simulate.")
parser.add_argument("--l1-cache-size", dest="l1cachesize", type=str, required=True, help="Size of the l1d and l1i caches.")
parser.add_argument("--l2-cache-size", dest="l2cachesize", type=str, required=True, help="Size of the l2 cache.")
parser.add_argument("--workload", dest="workload", choices=["roi", "default"], required=True, help="Workload to use.")
args = parser.parse_args()


match args.cpu_type:
  case "o3big":
    proc = BigProcessor()
  case "o3little":
    proc = LittleProcessor()
  case "o3":
    proc = SimpleProcessor(
      cpu_type=CPUTypes.O3,
      isa=ISA.X86,
      num_cores=1,
    )
  case "timing":
    proc = SimpleProcessor(
      cpu_type=CPUTypes.TIMING, # read from cpu_type
      isa=ISA.X86,
      num_cores=1,
    )
  case _:
    raise ValueError("Invalid CPU type selected")


workload = obtain_resource("riscv-matrix-multiply-run")

board = SimpleBoard(
  clk_freq="3GHz",
  processor=proc,
  memory=SingleChannelDDR4_2400(),
  cache_hierarchy=PrivateL1SharedL2CacheHierarchy(
    l1d_size=args.l1cachesize,
    l1i_size=args.l1cachesize,
    l2_size=args.l2cachesize,
  ),
)

if args.workload == "roi":
  board.set_se_binary_workload(BinaryResource(
    local_path="/home/pablo/phd/latin-america-2024/gem5-resources/src/matrix-multiply-roi/matrix-multiply",
  ))
else:
  board.set_se_binary_workload(BinaryResource(
    local_path="/home/pablo/phd/latin-america-2024/gem5-resources/src/matrix-multiply/matrix-multiply",
  ))

def reset_and_dump_generator():
  print("Resetting stats and dumping them")
  m5.stats.reset()
  m5.stats.dump()
  yield False

sim = Simulator(
  board=board,
  on_exit_event={
    ExitEvent.WORKBEGIN: reset_and_dump_generator(), # why in here we call the function. Doesn't that yield at once?
    ExitEvent.WORKEND: reset_and_dump_generator(),
  },
)
sim.run()
