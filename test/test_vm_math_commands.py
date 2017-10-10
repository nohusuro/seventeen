
#!/usr/bin/env python

import unittest
from vm17.vm17 import VM17

class VM17_MathCommand_Tests(unittest.TestCase):
  def setUp(self):
    self.vm = VM17()

  def test_add_with_numbers_command(self):
    self.vm.stack.push(10)
    self.vm.stack.push(23)
    self.vm.add()
    self.assertEqual(33, self.vm.stack.pop())

  def test_sub__with_numbers_command(self):
    self.vm.stack.push(20)
    self.vm.stack.push(2)
    self.vm.sub()
    self.assertEqual(18, self.vm.stack.pop())

  def test_mod_with_numbers_command(self):
    self.vm.stack.push(23)
    self.vm.stack.push(5)
    self.vm.mod()
    self.assertEqual(3, self.vm.stack.pop())

  def test_xor_with_numbers_command(self):
    self.vm.stack.push(10)
    self.vm.stack.push(7)
    self.vm.xor()
    self.assertEqual(13, self.vm.stack.pop())

