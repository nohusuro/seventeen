import sys
import re
from getpass import getpass
from vm17.stack import Stack
from vm17.getch import getch

class VM17:
  def __init__(self, debug=False):
    self.__eip = 0
    self.debug = debug

    self.stack = Stack()
    self.data = {}
    self.vector = {}
    self.labels = {}

    self.code_lines = []

    self.commands = {
      'add': lambda: self.add(),
      'sub': lambda: self.sub(),
      'mod': lambda: self.mod(),
      'xor': lambda: self.xor(),
      'store': lambda: self.store(),
      'vstore': lambda: self.vstore(),
      'vload': lambda: self.vload(),
      'dup': lambda: self.dup(),
      'read_num': lambda: self.read_num(),
      'print_num': lambda: self.print_num(),
      'print_byte': lambda: self.print_byte(),
      'read_byte': lambda: self.read_byte(),
      'jump': lambda: self.jump(),
      'call': lambda: self.call(),
      'ifz': lambda: self.ifz(),
      'ifg': lambda: self.ifg(),
      'exit': lambda: self.exit(),
    }

  #
  # Loading and execution
  #
  def load(self, file):
    self.__init__(self.debug)
    with open(file) as f:
      script = f.read()
      self.code_lines = re.sub('/\*(?:.|[\r\n])*?\*/', '', script)
      self.code_lines = self.code_lines.splitlines()
      self.code_lines = list(filter(None, self.code_lines))

    if self.debug:
      print("Loaded %d lines of code from %s\n" % (len(self.code_lines), file))


  def run(self):
    while self.__eip < len(self.code_lines):
      self.exec()

      if self.debug:
        pass
        getpass("")

  #
  # Interpreter
  #
  def exec(self):
    part = ''
    line = ''
    try:
      eip = self.__eip
      line = self.code_lines[self.__eip]
      parts = list(filter(None, line.split(' ')))

      if self.debug:
        print("> Ln#%d: %s" % (self.__eip, line))

      for part in parts:
        if part[-1] == ':':
          label = part[0:-1]
          self.labels[label] = self.__eip
          continue

        if part in self.commands:
          cmd = self.commands[part]()
          continue

        try:
          data = int(part)
        except:
          if len(parts) == 1:
            data = self.resolve_variable_or_return_input(part)
          else:
            data = part

        self.stack.push(data)

      if self.__eip == eip:
        self.__eip += 1

    except Exception as e:
      print("Script terminated prematurely")
      print("Exception with instruction %s on Ln#%d : %s" % (part, self.__eip, line))
      print(e)
      sys.exit(-1)

  #
  # Mathematical Operations
  #

  def add(self):
    b = self.resolve_variable_or_return_input(self.stack.pop())
    a = self.resolve_variable_or_return_input(self.stack.pop())

    self.stack.push(a + b)
    if self.debug:
      print(">>> Pushed %d + %d onto the stack:  %d" % (a, b, self.stack.peek()))

  def sub(self):
    b = self.resolve_variable_or_return_input(self.stack.pop())
    a = self.resolve_variable_or_return_input(self.stack.pop())

    self.stack.push(a - b)
    if self.debug:
      print(">>> Pushed %d - %d onto the stack:  %d" % (a, b, self.stack.peek()))

  def mod(self):
    b = self.resolve_variable_or_return_input(self.stack.pop())
    a = self.resolve_variable_or_return_input(self.stack.pop())

    self.stack.push(a % b)
    if self.debug:
      print(">>> Pushed %d %% %d onto the stack:  %d" % (a, b, self.stack.peek()))

  def xor(self):
    b = self.resolve_variable_or_return_input(self.stack.pop())
    a = self.resolve_variable_or_return_input(self.stack.pop())

    self.stack.push(a ^ b)
    if self.debug:
      print(">>> Pushed %d ^ %d onto the stack:  %d" % (a, b, self.stack.peek()))

  #
  # Storage Operations
  #
  def store(self):
    name = self.stack.pop()
    value = self.resolve_variable_or_return_input(self.stack.pop())
    self.data[name] = value

    if (self.debug):
      print(">>> Set variable %s to %s" % (name, value))

  def vstore(self):
    value = self.resolve_variable_or_return_input(self.stack.pop())
    offset = self.resolve_variable_or_return_input(self.stack.pop())

    self.vector[offset] = value

    if (self.debug):
      print(">>> Set vector offset %s to value %s" % (offset, value))

  def vload(self):
    offset = self.resolve_variable_or_return_input(self.stack.pop())

    self.stack.push(self.vector[offset])

    if (self.debug):
      print(">>> Pushed value %s from vector offset %d to the stack" % (self.stack.peek(), offset))

  def dup(self):
    self.stack.push(self.stack.peek())
    if self.debug:
      print(">> Duplicated value on the stack %s" % (self.stack.peek()))

  #
  # IO Operations
  #
  def read_num(self):
    self.stack.push(int(input("")))

  def read_byte(self):
    ch = sys.stdin.read(1)
    if ch:
      self.stack.push(ord(ch))
    else:
      self.stack.push(0)

  def print_num(self):
    x = self.resolve_variable_or_return_input(self.stack.pop())
    sys.stdout.write(str(x))

  def print_byte(self):
    b = self.stack.pop()
    sys.stdout.write(chr(b))

  #
  # Control Flow Operations
  #
  def jump(self):
    ref = self.stack.pop()
    self.__eip = self.get_eip_for_label(ref)

    if self.__eip == -1:
      self.__eip = int(self.resolve_variable_or_return_input(ref))

  def call(self):
    label = self.stack.pop()
    self.stack.push(self.__eip + 1)
    self.__eip = self.get_eip_for_label(label)

    if self.__eip == -1:
      self.__eip = int(self.resolve_variable_or_return_input(ref))

    if self.debug:
      print(">>> Pushed eip %d onto stack and jumped to eip %d with label %s" % (self.stack.peek(), self.__eip, label))

  def ifz(self):
    non_zero_label = self.stack.pop()
    on_zero_label = self.stack.pop()
    sv = self.stack.pop()
    value = int(self.resolve_variable_or_return_input(sv))

    if self.debug:
      print(">>> Value is %d taking jump %s" % (value, on_zero_label if value == 0 else non_zero_label))

    if value == 0:
      self.__eip = self.get_eip_for_label(on_zero_label)
    else:
      self.__eip = self.get_eip_for_label(non_zero_label)

  def ifg(self):
    not_greater_label = self.stack.pop()
    greater_label = self.stack.pop()
    value = int(self.stack.pop())

    if value > 0:
      self.__eip = self.get_eip_for_label(greater_label)
    else:
      self.__eip = self.get_eip_for_label(not_greater_label)


  def exit(self):
    sys.exit(0)

  #
  # Helpers
  #
  def resolve_variable_or_return_input(self, ref):
    result = ref
    try:
      result = self.data[ref]
    except:
      pass

    return result


  def get_eip_for_label(self, label):
    for index, line in enumerate(self.code_lines):
      if line.startswith(str(label) + ":"):
        return index

    return -1

  #
  # Registers
  #
  @property
  def eip(self):
    return self.__eip
