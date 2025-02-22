#!/bin/bash

for rate in 16 32 64; do
  for rd_pct in 50 100; do
  echo "Running experiment with rate=${rate}GiB/s and read percentage=${rd_pct}%"
  gem5 -q memory-test.py --rate="${rate}GiB/s" --rd_pct=${rd_pct} 2> /dev/null
 done
done
