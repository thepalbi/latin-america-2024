#!/bin/bash

. "$(git rev-parse --show-toplevel)/.env"

for cputype in "atomic" "timing" "minor" "o3"; do
    echo "Running $cputype"
    gem5.opt --outdir="m5out-${cputype}" main.py --cpu-type="$cputype" --caches-size="64KiB"

    if [ $? -ne 0 ]; then
        echo "gem5.opt failed for $cputype"
        exit 1
    fi
done
