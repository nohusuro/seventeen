
#!/usr/bin/env python

import unittest
from vm17.vm17 import VM17

class VM17_StoreCommand_Tests(unittest.TestCase):
  def setUp(self):
    self.vm = VM17()

  def test_vm_data_is_dict_type(self):
    self.assertEqual(self.vm.data, {})

  def test_store_new_variable(self):
    self.vm.stack.push('100')
    self.vm.stack.push('r')
    self.vm.store()
    self.assertEqual(0, self.vm.stack.count())
    self.assertEqual('100', self.vm.data['r'])

  def test_vstore(self):
    self.vm.stack.push(100)
    self.vm.stack.push(1)
    self.vm.vstore()
    self.assertEqual(1, self.vm.vector[100])
