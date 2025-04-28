import os, sys
import re
import math

from dataclasses import dataclass

OPERATOR_PRECEDENCE = {
  "NONE"      :   0,
  "ASSIGNMENT": 100,
  "LOGICAL"   : 200,
  "EQUALITY"  : 300,
  "COMPARISON": 400,
  "CUSTOM"    : 500,
  "TERM"      : 600,
  "FACTOR"    : 700,
  "UNARY"     : 800,
  "PRIMARY"   : 900,
}

SIDE = {
  "LEFT" :  1,
  "BOTH" :  0,
  "RIGHT": -1,
}

@dataclass
class BuiltinOperator():
  precedence: int
  associativity: int
  side: int
  function_body: str

  def __post_init__(self):
    self.function = eval(f"lambda lhs, rhs: {self.function_body}")

builtin_operators = {
  # real operators
  "'eq'": BuiltinOperator(OPERATOR_PRECEDENCE["EQUALITY"], SIDE["RIGHT"], SIDE["BOTH"], "float(lhs == rhs)"),
  "'equal'": BuiltinOperator(OPERATOR_PRECEDENCE["EQUALITY"], SIDE["RIGHT"], SIDE["BOTH"], "float(lhs == rhs)"),
  "'ne'": BuiltinOperator(OPERATOR_PRECEDENCE["EQUALITY"], SIDE["RIGHT"], SIDE["BOTH"], "float(lhs != rhs)"),
  "'neq'": BuiltinOperator(OPERATOR_PRECEDENCE["EQUALITY"], SIDE["RIGHT"], SIDE["BOTH"], "float(lhs != rhs)"),
  "'notequal'": BuiltinOperator(OPERATOR_PRECEDENCE["EQUALITY"], SIDE["RIGHT"], SIDE["BOTH"], "float(lhs != rhs)"),
  "'lt'": BuiltinOperator(OPERATOR_PRECEDENCE["COMPARISON"], SIDE["LEFT"], SIDE["BOTH"], "float(lhs < rhs)"),
  "'lessthan'": BuiltinOperator(OPERATOR_PRECEDENCE["COMPARISON"], SIDE["LEFT"], SIDE["BOTH"], "float(lhs < rhs)"),
  "'le'": BuiltinOperator(OPERATOR_PRECEDENCE["COMPARISON"], SIDE["LEFT"], SIDE["BOTH"], "float(lhs <= rhs)"),
  "'lessequal'": BuiltinOperator(OPERATOR_PRECEDENCE["COMPARISON"], SIDE["LEFT"], SIDE["BOTH"], "float(lhs <= rhs)"),
  "'gt'": BuiltinOperator(OPERATOR_PRECEDENCE["COMPARISON"], SIDE["LEFT"], SIDE["BOTH"], "float(lhs > rhs)"),
  "'greaterthan'": BuiltinOperator(OPERATOR_PRECEDENCE["COMPARISON"], SIDE["LEFT"], SIDE["BOTH"], "float(lhs > rhs)"),
  "'ge'": BuiltinOperator(OPERATOR_PRECEDENCE["COMPARISON"], SIDE["LEFT"], SIDE["BOTH"], "float(lhs >= rhs)"),
  "'greaterequal'": BuiltinOperator(OPERATOR_PRECEDENCE["COMPARISON"], SIDE["LEFT"], SIDE["BOTH"], "float(lhs >= rhs)"),
  
  "'and'": BuiltinOperator(OPERATOR_PRECEDENCE["LOGICAL"], SIDE["LEFT"], SIDE["BOTH"], "float(int(lhs) & int(rhs))"),
  "'nand'": BuiltinOperator(OPERATOR_PRECEDENCE["LOGICAL"], SIDE["LEFT"], SIDE["BOTH"], "~(lhs & rhs)"),
  "'or'": BuiltinOperator(OPERATOR_PRECEDENCE["LOGICAL"], SIDE["LEFT"], SIDE["BOTH"], "float(int(lhs) | int(rhs))"),
  "'xor'": BuiltinOperator(OPERATOR_PRECEDENCE["LOGICAL"], SIDE["LEFT"], SIDE["BOTH"], "float(int(lhs) ^ int(rhs))"),
  
  "'add'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"], SIDE["LEFT"], SIDE["BOTH"], "lhs + rhs"),
  "'plus'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"], SIDE["LEFT"], SIDE["BOTH"], "lhs + rhs"),
  "'sub'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"], SIDE["LEFT"], SIDE["BOTH"], "lhs - rhs"),
  "'minus'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"], SIDE["LEFT"], SIDE["BOTH"], "lhs - rhs"),
  "'mul'": BuiltinOperator(OPERATOR_PRECEDENCE["FACTOR"], SIDE["LEFT"], SIDE["BOTH"], "lhs * rhs"),
  "'times'": BuiltinOperator(OPERATOR_PRECEDENCE["FACTOR"], SIDE["LEFT"], SIDE["BOTH"], "lhs * rhs"),
  "'div'": BuiltinOperator(OPERATOR_PRECEDENCE["FACTOR"], SIDE["LEFT"], SIDE["BOTH"], "lhs / rhs"),
  "'over'": BuiltinOperator(OPERATOR_PRECEDENCE["FACTOR"], SIDE["LEFT"], SIDE["BOTH"], "lhs / rhs"),
  "'pow'": BuiltinOperator(OPERATOR_PRECEDENCE["FACTOR"] + 10, SIDE["RIGHT"], SIDE["BOTH"], "lhs ** rhs"),
  "sqrt'": BuiltinOperator(OPERATOR_PRECEDENCE["FACTOR"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.sqrt(rhs)"),
  
  "not'": BuiltinOperator(OPERATOR_PRECEDENCE["UNARY"], SIDE["LEFT"], SIDE["RIGHT"], "float(-1 ^ int(rhs))"),
  "neg'": BuiltinOperator(OPERATOR_PRECEDENCE["UNARY"], SIDE["LEFT"], SIDE["RIGHT"], "-rhs"),
  
  "cos'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.cos(rhs)"),
  "sin'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.sin(rhs)"),
  "tan'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.tan(rhs)"),
  "acos'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.acos(rhs)"),
  "asin'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.asin(rhs)"),
  "atan'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.atan(rhs)"),

  "ceil'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.ceil(rhs)"),
  "floor'": BuiltinOperator(OPERATOR_PRECEDENCE["TERM"] + 10, SIDE["RIGHT"], SIDE["RIGHT"], "math.floor(rhs)"),
  
  "display'": BuiltinOperator(OPERATOR_PRECEDENCE["NONE"] + 50, SIDE["RIGHT"], SIDE["RIGHT"], "print(\"%.2f\" % rhs)"),
  
  # psuedo operators
  "'is'": BuiltinOperator(OPERATOR_PRECEDENCE["ASSIGNMENT"], SIDE["RIGHT"], SIDE["BOTH"], None),
  "skipif'": BuiltinOperator(OPERATOR_PRECEDENCE["ASSIGNMENT"] + 50, SIDE["RIGHT"], SIDE["RIGHT"], None),
  "return'": BuiltinOperator(OPERATOR_PRECEDENCE["NONE"] + 50, SIDE["RIGHT"], SIDE["RIGHT"], None),
  "goto'": BuiltinOperator(OPERATOR_PRECEDENCE["NONE"] + 50, SIDE["RIGHT"], SIDE["RIGHT"], None),
}

@dataclass
class Operator():
  identifier: str
  line_number: int
  precedence: int
  associativity: int

  takes_lhs: bool
  lhs_identifier: str
  takes_rhs: bool
  rhs_identifier: str

  first_token_index: int

@dataclass
class Token:
  type: str
  line: int
  value: str

TOKEN_PATTERNS = {
  "NUMBER": r"\d+",
  "OPERATOR": r"'?[a-zA-Z_][a-zA-Z0-9_]*'?",
  "MACRO": r"\$[a-zA-Z_][a-zA-Z0-9_]*",
}

TOKEN_REGEX = re.compile(
  f'(?P<MACRO>{TOKEN_PATTERNS["MACRO"]})|'
  f'(?P<NUMBER>{TOKEN_PATTERNS["NUMBER"]})|'
  f'(?P<OPERATOR>{TOKEN_PATTERNS["OPERATOR"]})|'
  r'(?P<LPAREN>\()|'
  r'(?P<RPAREN>\))|'
  r'(?P<LBRACK>\[)|'
  r'(?P<RBRACK>\])|'
  r'(?P<COMMA>,)|'
  r'(?P<DOT>\.)|'
  r'(?P<COLON>:)|'
  r'(?P<SEMICOLON>;)'
)

@dataclass
class Scope():
  identifier: str
  variables: dict
  consumed_token: Token
  current_token_index: int
  return_now = False
  return_value = None
  gotod = False

class Interpreter():
  def __init__(self):
    self.tokens = []

    self.scope_stack = []
    self.return_value = None

    self.user_operators = {}
    
  def tokenize(self, source):
    tokens = []
    lines = source.splitlines()

    for line_number, line in enumerate(lines, start=1):
      position = 0
      while position < len(line):
        match = TOKEN_REGEX.match(line, position)
        if match:
          type = match.lastgroup
          value = match.group(type)
          
          if type == "OPERATOR" and "'" in value:
            if value == "'is'":
              tokens.append(Token("KEYWORD_IS", line_number, value))
            else:
              tokens.append(Token("OPERATOR", line_number, value))
          elif type == "OPERATOR":
            if value == "operator":
              tokens.append(Token("KEYWORD_OPERATOR", line_number, value))
            elif value == "end":
              tokens.append(Token("KEYWORD_END", line_number, value))
            else:
              tokens.append(Token("IDENTIFIER", line_number, value))
          elif type == "NUMBER":
            tokens.append(Token("NUMBER", line_number, value))
          elif type == "MACRO":
            if value == "$here":
              tokens.append(Token("NUMBER", line_number, len(tokens)))
          else:
            tokens.append(Token(type, line_number, value))

          position = match.end()
        elif line[position].isspace():
          position += 1
        else:
          print(f"Unexpected character '{line[position]}' on line {line_number}.")
          exit()
      
    tokens.append(Token("EOF", line_number, "EOF"))
    self.tokens = tokens

  def get_next_token(self):
    if self.scope_stack[-1].current_token_index < len(self.tokens):
      return self.tokens[self.scope_stack[-1].current_token_index]
    else:
      return self.tokens[-1]

  def get_consumed_token(self):
    return self.scope_stack[-1].consumed_token
    
  def advance(self):
    if self.scope_stack[-1].current_token_index < len(self.tokens):
      self.scope_stack[-1].consumed_token = self.get_next_token()
      self.scope_stack[-1].current_token_index += 1
    else:
      self.scope_stack[-1].consumed_token = self.tokens[-1]

  def expect(self, type):
    if self.get_next_token().type != type:
      self.print_call_stack()
      print(f"Unexpected token {self.get_next_token().type}, expected {type} at line {self.get_consumed_token().line}.")
      exit(1)
    self.advance()

  def optional(self, type):
    if self.get_next_token().type != type:
      return False
    self.advance()
    return True
  
  def revert(self):
    pass
  
  def lookup_variable(self, identifier):
    for scope in reversed(self.scope_stack):
      if identifier in scope.variables:
        return scope.variables
    return None

  def print_call_stack(self):
    print("Call Stack:")
    for depth, scope in enumerate(self.scope_stack):
      indent = '  '*depth
      print(f"{indent}{scope.identifier} at line {self.tokens[scope.current_token_index].line}.")

  def execute_psuedo_operator(self, identifier, lhs, rhs):
    if identifier == "return'":
      if len(self.scope_stack) == 1:
        exit(rhs)
      self.scope_stack[-1].return_value = rhs
      self.scope_stack[-1].return_now = True
      return 0.0
    elif identifier == "skipif'":
      if rhs >= 1.0:
        while self.optional("SEMICOLON"):
          if self.get_next_token().type == "EOF" or self.get_next_token().type == "KEYWORD_END":
            break
          self.advance()
        while self.get_next_token().type != "SEMICOLON":
          if self.get_next_token().type == "EOF" or self.get_next_token().type == "KEYWORD_END":
            break
          self.advance()
        return 0.0
    elif identifier == "goto'":
      self.scope_stack[-1].gotod = True
      self.scope_stack[-1].current_token_index = int(rhs)
      while self.optional("SEMICOLON"):
        if self.get_next_token().type == "EOF" or self.get_next_token().type == "KEYWORD_END":
          break
        self.advance()
      return 0.0
  
  def parse_prefix(self):
    if self.optional("NUMBER"):
      integer = self.get_consumed_token().value
      if self.optional("DOT"):
        self.expect("NUMBER")
        return float(integer + '.' + self.get_consumed_token().value)
      else:
        return float(integer)
    elif self.optional("IDENTIFIER"):
      identifier = self.get_consumed_token().value
      dict_refecence = self.lookup_variable(identifier)
      index = None
      if self.optional("LBRACK"):
        index = int(self.parse_expression(OPERATOR_PRECEDENCE["NONE"]))
        self.expect("RBRACK")
      
      if self.optional("KEYWORD_IS"):
        rhs = self.parse_expression(OPERATOR_PRECEDENCE["NONE"])
        if dict_refecence is None:
          if index is not None:
            self.scope_stack[-1].variables[identifier][index] = rhs
          else:
            self.scope_stack[-1].variables[identifier] = rhs
        else:
          if index is not None:
            dict_refecence[identifier][index] = rhs
          else:
            dict_refecence[identifier] = rhs
        return rhs
      elif dict_refecence is not None:
        if index is not None:
          return dict_refecence[identifier][index]
        return dict_refecence[identifier]
      self.print_call_stack()
      print(f"Undefined variable \"{self.get_consumed_token().value}\" referenced at line {self.get_consumed_token().line}.")
      exit(1)
    elif self.optional("LBRACK"):
      array = []
      while not self.optional("RBRACK"):
        array.append(self.parse_expression(OPERATOR_PRECEDENCE["NONE"]))
        if not self.optional("COMMA"):
          self.expect("RBRACK")
          break
      return array
    elif self.optional("LPAREN"):
      expression_value = self.parse_expression(OPERATOR_PRECEDENCE["NONE"])
      self.expect("RPAREN")
      return expression_value
    elif self.get_next_token().type == "OPERATOR":
      while self.get_next_token().type == "OPERATOR":
        operator = None
        operator_identifier = self.get_next_token().value
        user_operator = False
        if operator_identifier in self.user_operators:
          operator = self.user_operators[operator_identifier]
          user_operator = True
        elif operator_identifier in builtin_operators:
          operator = builtin_operators[operator_identifier]
        else:
          self.print_call_stack()
          print(f"Undefined operator {operator_identifier} referenced in line {self.get_next_token().line}")
          exit(1)
        
        if not user_operator and operator.side != SIDE["RIGHT"]:
          self.print_call_stack()
          print(f"Unexpected two operand operator {operator_identifier} at line {self.get_next_token().line}.")
          exit(1)
        elif user_operator and operator.lhs_identifier is not None:
          self.print_call_stack()
          print(f"Unexpected two operand operator {operator_identifier} at line {self.get_next_token().line}.")
          exit(1)

        self.expect("OPERATOR")
        next_precedence = operator.precedence + operator.associativity
        rhs = self.parse_expression(next_precedence)

        if user_operator:
          parameter_dict = { operator.rhs_identifier: rhs }
          self.scope_stack.append(Scope(operator_identifier, parameter_dict, None, operator.first_token_index))
          self.parse_program()
          lhs = self.scope_stack[-1].return_value
          self.scope_stack.pop()
          return lhs
        elif operator.function_body is None:
          return self.execute_psuedo_operator(operator_identifier, None, rhs)
        else:
          return operator.function(None, rhs)
    else:
      self.print_call_stack()
      print(f"Unexpected token {self.get_consumed_token().type} at line {self.get_consumed_token().line}.")
      exit(1)

  def parse_expression(self, precedence):
    lhs = self.parse_prefix()

    while self.get_next_token().type == "OPERATOR":
      operator = None
      operator_identifier = self.get_next_token().value
      user_operator = False
      if operator_identifier in self.user_operators:
        operator = self.user_operators[operator_identifier]
        user_operator = True
      elif operator_identifier in builtin_operators:
        operator = builtin_operators[operator_identifier]
      else:
        self.print_call_stack()
        print(f"Undefined operator {operator_identifier} referenced in line {self.get_next_token().line}")
        exit(1)

      if operator.precedence < precedence:
        return lhs

      self.expect("OPERATOR")
      next_precedence = operator.precedence + operator.associativity
      rhs = self.parse_expression(next_precedence)

      if user_operator:
        parameter_dict = {
          operator.lhs_identifier: lhs if operator.takes_lhs else None,
          operator.rhs_identifier: rhs if operator.takes_rhs else None,
        }
        self.scope_stack.append(Scope(operator_identifier, parameter_dict, None, operator.first_token_index))
        self.parse_program()
        lhs = self.scope_stack[-1].return_value
        self.scope_stack.pop()
      elif operator.function_body is None:
        lhs = self.execute_psuedo_operator(operator_identifier, lhs, rhs)
      else:
        lhs = operator.function(lhs, rhs)
    return lhs
  
  def parse_operator_definition(self):
    self.expect("IDENTIFIER")
    if self.get_consumed_token().value != "right" and self.get_consumed_token().value != "left":
      print(f"Unexpected token {self.get_consumed_token().type}, expected \"right\" or \"left\" at line {self.get_consumed_token().line}.")
    associativity = SIDE["RIGHT"] if self.get_consumed_token().value == "right" else SIDE["LEFT"]

    precedence = None
    if self.optional("NUMBER"):
      precedence = int(self.get_consumed_token().value)
    elif self.optional("IDENTIFIER") and self.get_consumed_token().value.upper() in OPERATOR_PRECEDENCE:
      precedence = OPERATOR_PRECEDENCE[self.get_consumed_token().value.upper()]
    else:
      print(f"Unexpected token {self.get_consumed_token().type}, expected a precedence value at line {self.get_consumed_token().line}.")

    takes_lhs = False
    lhs_identifier = None
    if self.optional("IDENTIFIER"):
      takes_lhs = True
      lhs_identifier = self.get_consumed_token().value
    
    self.expect("OPERATOR")
    operator_identifier = self.get_consumed_token().value

    takes_rhs = False
    rhs_identifier = None
    if self.optional("IDENTIFIER"):
      takes_rhs = True
      rhs_identifier = self.get_consumed_token().value
    
    if operator_identifier[-1] == "'" and not takes_rhs:
      print(f"Expected right hand side parameter identifier at line {self.get_consumed_token().line}.")

    operator_def = Operator(operator_identifier, self.get_next_token().line,
                            precedence, associativity, takes_lhs, lhs_identifier,
                            takes_rhs, rhs_identifier, self.scope_stack[-1].current_token_index)
    self.user_operators[operator_identifier] = operator_def

    while not self.optional("KEYWORD_END"):
      if self.optional("EOF"):
        print(f"Unterminated operator definition starting at line {operator_def.line_number}.")
        exit()
      self.advance()

  def parse_program(self):
    if len(self.scope_stack) == 1:
      while self.get_next_token().type != "EOF":
        if self.optional("KEYWORD_OPERATOR"):
          self.parse_operator_definition()
        else:
          self.parse_expression(OPERATOR_PRECEDENCE["NONE"])
          if not self.scope_stack[-1].gotod:
            self.expect("SEMICOLON")
          self.scope_stack[-1].gotod = False
    else:
      while not (self.scope_stack[-1].return_now or self.optional("EOF") or self.optional("KEYWORD_END")):
        self.parse_expression(OPERATOR_PRECEDENCE["NONE"])
        if not self.scope_stack[-1].gotod:
          self.expect("SEMICOLON")
        self.scope_stack[-1].gotod = False

  def interpret_file(self, file_name):
    self.tokenize(open(file_name, "r").read())
    self.scope_stack.append(Scope("root", {}, None, 0))
    self.scope_stack[-1].return_now = False
    while self.get_next_token().type != "EOF":
      self.parse_program()

if __name__ == "__main__":
  interpreter = Interpreter()
  interpreter.interpret_file(sys.argv[1])
  exit(interpreter.return_value)