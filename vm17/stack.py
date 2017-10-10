class Stack:
  def __init__(self):
    self.stack = []

  def push(self, item):
    self.stack.append(item)

  def pop(self):
    return self.stack.pop()

  def peek(self):
    return self.stack[len(self.stack)-1]

  def count(self):
    return len(self.stack)
