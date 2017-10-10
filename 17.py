#!/usr/bin/env python

import sys
import signal
import re
from vm17.vm17 import VM17

if __name__ == '__main__':

  if len(sys.argv) < 2:
    print("Usage: %s file" % (sys.argv[0]))
    sys.exit(-1)

  def signal_handler(signal, frame):
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)

  interpreter = VM17(debug=False)
  interpreter.load(sys.argv[1])
  interpreter.run()
