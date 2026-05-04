#!/bin/bash
tail -f /dev/null > /run/jalv-ir-input &
TAIL_PID=$!

/usr/bin/jalv urn:brummer:ImpulseLoader < /run/jalv-ir-input &
JALV_PID=$!

until jack_lsp 2>/dev/null | grep -q "ImpulseLoader"; do
    sleep 0.1
done

sleep 1

# Use the same file descriptor, don't open/close it
exec 3>/run/jalv-ir-input
echo "preset urn:brummer:impulseloader-state-orange" >&3

wait $JALV_PID
kill $TAIL_PID
exec 3>&-
