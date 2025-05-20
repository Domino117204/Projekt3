#!/bin/bash

PROGRAM=./program
REPRESENTATIONS=("matrix" "list" "table")
ACTIONS=("find" "kahn" "tarjan")

mkdir -p results

for rep in "${REPRESENTATIONS[@]}"; do
    for action in "${ACTIONS[@]}"; do
        OUTFILE="results/${action}_${rep}.csv"
        echo "nodes,time" > "$OUTFILE"
        for exp in {5..12}; do
            nodes=$((2**exp))
            echo "Benchmarking $action for $nodes nodes ($rep)..."

            result=$(python3 benchmark_once.py "$nodes" "$rep" "$action")
            time_val=$(echo "$result" | grep "TIME:" | awk '{print $2}')

            if [[ -n "$time_val" ]]; then
                echo "$nodes,$time_val" >> "$OUTFILE"
            else
                echo "$nodes,ERROR" >> "$OUTFILE"
            fi
        done
    done
done
