#!/bin/bash
tail -f /dev/null > /run/jalv-nam-input &
TAIL_PID=$!

/usr/bin/jalv http://github.com/mikeoliphant/neural-amp-modeler-lv2 < /run/jalv-nam-input &
JALV_PID=$!

until jack_lsp 2>/dev/null | grep -q "Neural Amp Modeler"; do
    sleep 0.1
done

sleep 1

# Use the same file descriptor, don't open/close it
exec 3>/run/jalv-nam-input
echo "preset urn:nam:orange-clean" >&3

wait $JALV_PID
kill $TAIL_PID
exec 3>&-
