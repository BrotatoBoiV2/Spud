from nodes import *

TESTS = [IntegerNode(2), OperatorNode("+"), IntegerNode(2)]

def test_join_parts(parts):
  # iterate through the parts and join them together and output the right type.
  index = 0

  while index < len(parts):
    part = parts[index]
    # print(part)
    print(type(part))

    if len(parts) > 1:
    
      if isinstance(parts[index+1], OperatorNode):
        if isinstance(part, IntegerNode) and isinstance(parts[index+2], IntegerMode):
          return parts[index+1].execute(part.execute(), parts[index+2].execute())

        elif isinstance(part, StringNode) and isinstance(parts[index+2], StringNode):
          return parts[index+1].execute(part.execute(), parts[index+2].execute())

        elif isinstance(part, VariableNode) and isinstance(parts[index+2], VariableNode):
          return parts[index+1].execute(part.evaluate(), parts[index+2].evaluate())

      else:
        #error
        pass

    else:
      if isinstance(part, IntegerNode) or isinstance(part, StringNode) or isinstance(part, VariableNode):
        return part.execute()

    index += 1 
    

print(type(test_join_parts(TESTS)))
