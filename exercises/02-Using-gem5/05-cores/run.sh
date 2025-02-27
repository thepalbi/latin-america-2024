#!/bin/bash

. "$(git rev-parse --show-toplevel)/.env"

for cputype in "timing"; do
  for workload in "roi" "default"; do
    echo "Running $cputype - $workload"
    gem5.opt --outdir="m5out-${workload}" main.py --workload="${workload}" --cpu-type="$cputype" --l1-cache-size="64KiB" --l2-cache-size="1MiB"

    if [ $? -ne 0 ]; then
        echo "gem5.opt failed for $cputype"
        exit 1
    fi
  done
done
