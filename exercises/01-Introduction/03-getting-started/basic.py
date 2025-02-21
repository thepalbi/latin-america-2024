from gem5.prebuilt.demo.x86_demo_board import X86DemoBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator

board = X86DemoBoard()
board.set_workload(
  obtain_resource('x86-ubuntu-24.04-boot-no-systemd'),
)

def exit_event_handler():
    print('first exit event: Kernel booted')
    yield False
    print('second exit event: In after boot')
    yield False
    print('third exit event: After run script')
    yield True

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: exit_event_handler(),
    },
)
simulator.run(20_000_000_000) # 20 billion ticks or 20 ms

