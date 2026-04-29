#!/bin/bash

wait_for_port() {
    local port=$1
    local timeout=30
    local elapsed=0
    until jack_lsp 2>/dev/null | grep -q "$port"; do
        sleep 0.5
        elapsed=$((elapsed + 1))
        if [ $elapsed -ge $timeout ]; then
            echo "Timed out waiting for port $port"
            exit 1
        fi
    done
}

wait_for_port "Neural Amp Modeler:input"
wait_for_port "ImpulseLoader:in0"

echo "All ports ready"

jack_connect system:capture_2 "Neural Amp Modeler:input"
jack_connect "Neural Amp Modeler:output" ImpulseLoader:in0
jack_connect ImpulseLoader:out0 system:playback_1
jack_connect ImpulseLoader:out0 system:playback_2

echo "All ports connected"
