from math import log
from typing import List
from gem5.components.processors.abstract_generator import (
    AbstractGenerator,
    partition_range,
)
from gem5.components.processors.abstract_generator_core import (
    AbstractGeneratorCore,
)
from gem5.components.processors.linear_generator_core import (
    LinearGeneratorCore,
)
from gem5.components.processors.random_generator_core import (
    RandomGeneratorCore,
)
from gem5.utils.override import overrides


def get_num_linear_cores(num_cores: int) -> int:
    """
    Returns the largest power of two that is smaller than num_cores
    """
    if num_cores & (num_cores - 1) == 0:
        return num_cores // 2
    else:
        return 2 ** int(log(num_cores, 2))


class HybridGenerator(AbstractGenerator):
    def __init__(
        self,
        num_cores: int = 1,
        duration: str = "1ms",
        rate: str = "100GB/s",
        block_size: int = 64,
        min_addr: int = 0,
        max_addr: int = 32768,
        rd_perc: int = 100,
        data_limit: int = 0,
    ) -> None:
        super().__init__(
            cores=self._create_cores(
                num_cores=num_cores,
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=min_addr,
                max_addr=max_addr,
                rd_perc=rd_perc,
                data_limit=data_limit,
            )
        )

    def _create_cores(
        self,
        num_cores: int,
        duration: str,
        rate: str,
        block_size: int,
        min_addr: int,
        max_addr: int,
        rd_perc: int,
        data_limit: int,
    ) -> List[AbstractGeneratorCore]:
        num_linear_cores = get_num_linear_cores(num_cores)
        addr_ranges = partition_range(min_addr, max_addr, num_linear_cores)
        linear_cores = [
            LinearGeneratorCore(
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=r[0],
                max_addr=r[1],
                rd_perc=rd_perc,
                data_limit=data_limit,
            )
            for r in addr_ranges
        ]
        random_cores = [
            RandomGeneratorCore(
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=min_addr,
                max_addr=max_addr,
                rd_perc=rd_perc,
                data_limit=data_limit,
            )
            for _ in range(num_cores - num_linear_cores)
        ]
        return linear_cores + random_cores

    @overrides(AbstractGenerator)
    def start_traffic(self) -> None:
        for core in self.cores:
            core.start_traffic()
