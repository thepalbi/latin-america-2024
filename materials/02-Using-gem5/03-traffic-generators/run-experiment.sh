#!/bin/bash

for rate in 16 32 64; do
  for rd_pct in 50 100; do
    for gen_class in "linear" "random"; do
      echo "Running experiment with rate=${rate}GiB/s and read percentage=${rd_pct}% generator=${gen_class}"
      gem5 -q memory-test.py --rate="${rate}GiB/s" --rd_pct=${rd_pct} --generator="${gen_class}" 2> /dev/null
    done
 done
done
