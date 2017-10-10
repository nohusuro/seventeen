#!/usr/bin/env python

import unittest
testmodules = [
  'test.test_stack',
  'test.test_vm_command_parser',
  'test.test_vm_control_flow',
  'test.test_vm_io_commands',
  'test.test_vm_math_commands',
  'test.test_vm_store_commands',
]

suite = unittest.TestSuite()

for t in testmodules:
  try:
    # If the module defines a suite() function, call it to get the suite.
    mod = __import__(t, globals(), locals(), ['suite'])
    suitefn = getattr(mod, 'suite')
    suite.addTest(suitefn())
  except (ImportError, AttributeError):
    # else, just load all the test cases from the module.
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner(verbosity=2).run(suite)
