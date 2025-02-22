#!/bin/bash

num_cores=2
memory_type="ddr4"

for rate in 16 32 64; do
  for rd_pct in 50 100; do
    for gen_class in "hybrid" "linear" "random"; do
      echo "---- EXP memory=${memory_type} num_cores=${num_cores} rate=${rate}GiB/s rd_pct=${rd_pct}% generator=${gen_class}"
      gem5 -q memory-test.py --num_cores=${num_cores} --rate="${rate}GiB/s" --rd_pct=${rd_pct} --generator="${gen_class}" --memory="${memory_type}" 2> fail.log
      if [ $? -ne 0 ]; then
        echo "---- FAIL"
        cat fail.log
        exit 1
      fi
    done
 done
done
