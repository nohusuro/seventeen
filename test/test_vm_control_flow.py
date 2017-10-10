#!/usr/bin/env python

import unittest
from vm17.vm17 import VM17

class VM17_ControlFlow_Tests(unittest.TestCase):
  def setUp(self):
    self.vm = VM17()
    self.success_label = "success_label"
    self.failure_label = "failure_label"
    self.other_label = "other_label"

    self.vm.code_lines.append(self.failure_label + ":")
    self.vm.code_lines.append(self.success_label + ":")
    self.vm.code_lines.append(self.other_label + ":")

  def test_get_eip_for_label(self):
    self.assertEqual(0, self.vm.get_eip_for_label(self.failure_label))
    self.assertEqual(1, self.vm.get_eip_for_label(self.success_label))
    self.assertEqual(2, self.vm.get_eip_for_label(self.other_label))

  def test_call_pushes_eip_to_stack(self):
    self.vm.stack.push(self.other_label)
    self.vm.call()
    self.assertEqual(2, self.vm.eip)

  def test_jump(self):
    self.vm.stack.push(self.other_label)
    self.vm.jump()

  def test_ifz_command_for_failure_branch(self):
    self.vm.stack.push(0)
    self.vm.stack.push(self.failure_label)
    self.vm.stack.push(self.success_label)
    self.vm.ifz()
    self.assertEqual(0, self.vm.eip)

  def test_ifz_command_for_success_branch(self):
    self.vm.stack.push(1)
    self.vm.stack.push(self.failure_label)
    self.vm.stack.push(self.success_label)
    self.vm.ifz()
    self.assertEqual(1, self.vm.eip)

  def test_ifg_command_for_failure_branch(self):
    pass
    #self.vm.stack.push(0)
    #self.vm.stack.push('failure_label')
    #self.vm.stack.push('success_label')
    #self.vm.ifg()
    #self.assertEqual('failure_label', self.vm.stack.pop())

  def test_ifg_command_for_success_branch(self):
    pass
    #self.vm.stack.push(1)
    #self.vm.stack.push('failure_label')
    #self.vm.stack.push('success_label')
    #self.vm.ifg()
    #self.assertEqual('success_label', self.vm.stack.pop())
