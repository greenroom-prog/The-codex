#!/bin/bash
while true; do
    echo "Starting Atlas at $(date)"
    python3 atlas_live.py
    echo "Atlas stopped at $(date). Restarting in 5 seconds..."
    sleep 5
done
