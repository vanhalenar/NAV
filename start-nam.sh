#!/bin/bash
# Keep write end of FIFO open so jalv stdin doesn't block
#jalv -i ~/.lv2/nam-state-fender.lv2
# Open write end in background to unblock the read end
tail -f /dev/null > /run/jalv-nam-input &
TAIL_PID=$!

# Now open jalv with the FIFO as stdin
/usr/local/bin/jalv ~/.lv2/nam-state-fender.lv2 < /run/jalv-nam-input

# Clean up tail when jalv exits
kill $TAIL_PID
