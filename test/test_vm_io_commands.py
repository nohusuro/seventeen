
#!/usr/bin/env python

import sys
import io
import unittest
import unittest.mock
from vm17.vm17 import VM17

class VM17_IOCommand_Tests(unittest.TestCase):
  def setUp(self):
    self.vm = VM17()

  def test_io_read_num(self):
    with unittest.mock.patch('builtins.input', return_value='10'):
      self.vm.read_num()
      self.assertEqual(10, self.vm.stack.pop())

  def test_io_print_num(self):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    self.vm.stack.push(45)
    self.vm.print_num()
    sys.stdout = sys.__stdout__
    self.assertEqual('45', captured_output.getvalue())

  def test_io_print_byte(self):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    self.vm.stack.push(45)
    self.vm.stack.push(103)
    self.vm.stack.push(97)
    self.vm.stack.push(108)
    self.vm.stack.push(102)
    self.vm.print_byte()
    self.vm.print_byte()
    self.vm.print_byte()
    self.vm.print_byte()
    self.vm.print_byte()

    sys.stdout = sys.__stdout__
    self.assertEqual('flag-', captured_output.getvalue())
