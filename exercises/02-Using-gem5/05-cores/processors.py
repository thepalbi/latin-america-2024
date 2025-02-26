
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from m5.objects import RiscvO3CPU


class BigO3(RiscvO3CPU):
  def __init__(self):
    super().__init__()
    self.fetchWidth = 8
    self.decodeWidth = 8
    self.renameWidth = 8
    self.issueWidth = 8
    self.wbWidth = 8
    self.commitWidth = 8
    self.numROBEntries = 256
    self.numPhysIntRegs = 512
    self.numPhysFloatRegs = 512


class BigCore(BaseCPUCore):
  def __init__(self):
    core = BigO3()
    super().__init__(core, ISA.RISCV)


class BigProcessor(BaseCPUProcessor):
  def __init__(self):
    super().__init__([BigCore()])


class LittleO3(RiscvO3CPU):
  def __init__(self):
    super().__init__()
    self.fetchWidth = 4
    self.decodeWidth = 4
    self.renameWidth = 4
    self.issueWidth = 4
    self.wbWidth = 4
    self.commitWidth = 4
    self.numROBEntries = 30
    self.numPhysIntRegs = 40
    self.numPhysFloatRegs = 40

class LittleCore(BaseCPUCore):
  def __init__(self):
    core = LittleO3()
    super().__init__(core, ISA.RISCV)


class LittleProcessor(BaseCPUProcessor):
  def __init__(self):
    super().__init__([LittleCore()])
