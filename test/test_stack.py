#!/usr/bin/env python

import unittest
import inspect
from vm17.stack import Stack

class StackTests(unittest.TestCase):
  def setUp(self):
    self.stack = Stack()

  def test_stack_should_be_instance_of_stack(self):
    self.assertIsInstance(self.stack, Stack)

  def test_stack_should_start_empty(self):
    self.assertEqual(0, self.stack.count())

  def test_stack(self):
    start_count = self.stack.count()

    test_val1 = 1
    test_val2 = "test"

    self.stack.push(test_val1)
    self.assertEqual(start_count + 1, self.stack.count()) # Make sure the start count increased by 1
    self.assertEqual(test_val1, self.stack.peek())        # Make sure the element we're expecting is on top
    self.assertEqual(start_count + 1, self.stack.count()) # Make sure peeking didn't remove an element

    self.stack.push(test_val2)
    self.assertEqual(start_count + 2, self.stack.count()) # Make sure the start count increased by 2
    self.assertEqual(test_val2, self.stack.peek())        # Make sure the element we're expecting is on top
                                                          # Don't need to test peek again

    pop_val2 = self.stack.pop()
    self.assertEqual(test_val2, pop_val2)                 # Compare the item we popped to our test value
    self.assertEqual(start_count + 1, self.stack.count()) # Make sure the stack count decremented

    pop_val1 = self.stack.pop()
    self.assertEqual(test_val1, pop_val1)                 # Compare the item we popped to our test value
    self.assertEqual(start_count, self.stack.count())     # Make sure the stack count decremented
