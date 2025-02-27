#!/bin/bash

. "$(git rev-parse --show-toplevel)/.env"

for cputype in "timing"; do
  for arch in "x86" "riscv"; do
    echo "Running $arch - $workload"
    gem5.opt --outdir="m5out-cc-${arch}" main.py --arch="${arch}" --workload="roi" --cpu-type="$cputype" --l2-cache-size="64KiB" --l2-cache-size="1MiB"

    if [ $? -ne 0 ]; then
        echo "gem5.opt failed for $arch"
        exit 1
    fi
  done
done
