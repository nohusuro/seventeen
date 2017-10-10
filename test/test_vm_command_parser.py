#!/usr/bin/env python

import sys
import io
import unittest
import unittest.mock
from vm17.vm17 import VM17

class VM17_CommandParser_Tests(unittest.TestCase):
  def setUp(self):
    self.vm = VM17()

  #
  # Mathematical Operations
  #
  def test_exec_math_add(self):
    self.vm.stack.push(10)
    self.vm.stack.push(10)
    self.vm.code_lines.append("add")
    self.vm.exec()
    self.assertEqual(20, self.vm.stack.peek())

    self.vm.code_lines.append("5 add")
    self.vm.exec()
    self.assertEqual(25, self.vm.stack.pop())

    self.vm.code_lines.append("2 5 add")
    self.vm.exec()
    self.assertEqual(7, self.vm.stack.pop())

  def test_exec_math_sub(self):
    self.vm.stack.push(20)
    self.vm.stack.push(3)
    self.vm.code_lines.append("sub")
    self.vm.exec()
    self.assertEqual(17, self.vm.stack.peek())

    self.vm.code_lines.append("9 sub")
    self.vm.exec()
    self.assertEqual(8, self.vm.stack.pop())

    self.vm.code_lines.append("100 37 sub")
    self.vm.exec()
    self.assertEqual(63, self.vm.stack.pop())

  def test_exec_math_mod(self):
    self.vm.stack.push(20)
    self.vm.stack.push(8)
    self.vm.code_lines.append("mod")
    self.vm.exec()
    self.assertEqual(4, self.vm.stack.peek())

    self.vm.code_lines.append("3 mod")
    self.vm.exec()
    self.assertEqual(1, self.vm.stack.pop())

    self.vm.code_lines.append("100 37 mod")
    self.vm.exec()
    self.assertEqual(26, self.vm.stack.pop())

  def test_exec_math_xor(self):
    self.vm.stack.push(99)
    self.vm.stack.push(13)
    self.vm.code_lines.append("xor")
    self.vm.exec()
    self.assertEqual(110, self.vm.stack.peek())

    self.vm.code_lines.append("7 xor")
    self.vm.exec()
    self.assertEqual(105, self.vm.stack.pop())

    self.vm.code_lines.append("12 20 xor")
    self.vm.exec()
    self.assertEqual(24, self.vm.stack.pop())

  def test_exec_math_check(self):
    self.vm.code_lines.append("10 12 add")
    self.vm.code_lines.append("2 sub")
    self.vm.code_lines.append("6 mod")
    self.vm.code_lines.append("7 xor")
    self.vm.run()
    self.assertEqual(5, self.vm.stack.pop())

  #
  # Storage Operations
  #
  def test_exec_storage_store(self):
    self.vm.stack.push(5)
    self.vm.stack.push("num")
    self.vm.code_lines.append("store")
    self.vm.exec()
    self.assertEqual(5, self.vm.data["num"])

    self.vm.stack.push(2)
    self.vm.code_lines.append("num store")
    self.vm.exec()
    self.assertEqual(2, self.vm.data["num"])

    self.vm.code_lines.append("5 num store")
    self.vm.exec()
    self.assertEqual(5, self.vm.data["num"])

  def test_exec_storage_vstore_vload(self):
    self.vm.stack.push(4)
    self.vm.stack.push(5)
    self.vm.code_lines.append("vstore")
    self.vm.exec()
    self.assertEqual(5, self.vm.vector[4])

    self.vm.stack.push(2)
    self.vm.code_lines.append("1 vstore")
    self.vm.exec()
    self.assertEqual(1, self.vm.vector[2])

  def test_exec_storage_dup(self):
    start_count = self.vm.stack.count()
    self.vm.code_lines.append("99 dup")
    self.vm.exec()
    self.assertEqual(start_count + 2, self.vm.stack.count())
    self.assertEqual(99, self.vm.stack.pop())
    self.assertEqual(99, self.vm.stack.pop())

  def test_exec_storage_check(self):
    self.vm.code_lines.append("10 1 vstore")
    self.vm.code_lines.append("11 2 vstore")
    self.vm.code_lines.append("10 vload")
    self.vm.code_lines.append("11 vload")
    self.vm.code_lines.append("add")
    self.vm.code_lines.append("x store")
    self.vm.code_lines.append("x")
    self.vm.run()
    self.assertEqual(3, self.vm.stack.pop())

  def test_exec_store_check2(self):
    self.vm.code_lines.append("1 x store")
    self.vm.code_lines.append("x")
    self.vm.code_lines.append("0 x store")
    self.vm.run()
    self.assertEqual(1, self.vm.stack.pop())

  def test_exec_storage_vector_init(self):
    self.vm.code_lines.append("start jump")
    self.vm.code_lines.append("sub_init_vector:")
    self.vm.code_lines.append("r store")
    self.vm.code_lines.append("v store")
    self.vm.code_lines.append("init_vector_loop: dup v vstore")
    self.vm.code_lines.append("1 sub")
    self.vm.code_lines.append("dup init_vector_done init_vector_loop ifz")
    self.vm.code_lines.append("init_vector_done: r jump")
    self.vm.code_lines.append("start: 5 1 sub_init_vector call")
    self.vm.run()
    self.assertEqual(5, len(self.vm.vector))
    self.assertEqual(1, self.vm.vector[5])
    self.assertEqual(1, self.vm.vector[4])
    self.assertEqual(1, self.vm.vector[3])
    self.assertEqual(1, self.vm.vector[2])
    self.assertEqual(1, self.vm.vector[1])

  #
  # IO Operations
  #
  def test_exec_io_read_num(self):
    self.vm.code_lines.append("read_num x store")
    with unittest.mock.patch('builtins.input', return_value='10'):
      self.vm.exec()
      self.assertEqual(10, self.vm.data['x'])

  def test_exec_print_num(self):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    self.vm.code_lines.append("45")
    self.vm.code_lines.append("print_num")
    self.vm.run()
    sys.stdout = sys.__stdout__
    self.assertEqual('45', captured_output.getvalue())

  def test_exec_print_byte(self):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    self.vm.code_lines.append("45 103 97 108 102")
    self.vm.exec()
    self.vm.code_lines.append("print_byte print_byte print_byte print_byte print_byte")
    self.vm.exec()
    sys.stdout = sys.__stdout__
    self.assertEqual('flag-', captured_output.getvalue())

  #
  # Control Flow Operations
  #
  def test_exec_control_ifz_is_zero(self):
    self.vm.code_lines.append("0 done start ifz")
    self.vm.code_lines.append("skip jump")
    self.vm.code_lines.append("done: 10 result store")
    self.vm.code_lines.append("skip:")
    self.vm.run()
    self.assertEqual(10, self.vm.data["result"])

  def test_exec_control_ifz_is_not_zero(self):
    self.vm.code_lines.append("1 done start ifz")
    self.vm.code_lines.append("skip jump")
    self.vm.code_lines.append("start: 20 result store")
    self.vm.code_lines.append("skip:")
    self.vm.run()
    self.assertEqual(20, self.vm.data["result"])

  def test_exec_call(self):
    self.vm.code_lines.append("end jump")
    self.vm.code_lines.append("func1: 10 15 add")
    self.vm.code_lines.append("skip jump")
    self.vm.code_lines.append("end: func1 call")
    self.vm.code_lines.append("skip:")
    self.vm.run()
    self.assertEqual(25, self.vm.stack.pop())

  def test_exec_control_labels(self):
    self.assertTrue('label1' not in self.vm.labels)
    self.vm.code_lines.append('label1:')
    self.vm.exec()
    self.assertTrue('label1' in self.vm.labels)

  #
  # Other checks
  #
  def test_exec_numbers(self):
    self.vm.code_lines.append("45 103 97 108 102")
    self.vm.exec()
    self.assertEqual(102, self.vm.stack.pop())
    self.assertEqual(108, self.vm.stack.pop())
    self.assertEqual(97, self.vm.stack.pop())
    self.assertEqual(103, self.vm.stack.pop())
    self.assertEqual(45, self.vm.stack.pop())
