from numpy import matrix
from numpy import linalg
import numpy

class Calculator:
    def __init__(self):
        self.input_string = ''
        self.infix_list = []
        self.postfix_list = []

    operators_set = set(r'+-*/() ')
    operators = {'*': 2, '/': 2, '+': 1, '-': 1, '(': 0, ')': 0}

    def get_input_string(self):
        return self.input_string
    def set_infix_string(self, string):
        allowed_symbols = set(r'0123456789.+-*/() ')
        self.infix_list.clear()
        self.postfix_list.clear()
        for c in string:
            if (c not in allowed_symbols):
                self.input_string = ''
                return
        self.input_string = string
        numeric = set(r'0123456789.')
        current_number = ''
        for c in self.input_string:
            if c in numeric:
                current_number += c
            elif c == ' ':
                continue
            else:
                if current_number != '':
                    self.infix_list.append(float(current_number))
                self.infix_list.append(c)
                current_number = ''
        if current_number != '':
            self.infix_list.append(float(current_number))
    def set_infix_list(self, list):
        self.infix_list.clear()
        self.postfix_list.clear()
        for item in list:
            self.infix_list.append(item)

    def apply_rules(self, item, operator_stack):
        if type(item) == type(matrix([])) or item not in self.operators_set:
            self.postfix_list.append(item)
        else:
            if item == '(':
                operator_stack.append(item)
            elif item == ')':
                current = ''
                while current != '(':
                    current = operator_stack.pop()
                    if current != '(':
                        self.postfix_list.append(current)
            elif len(operator_stack) == 0 or operator_stack[len(operator_stack) - 1] == '(':
                operator_stack.append(item)
            elif operator_stack[len(operator_stack) - 1] == item:
                self.postfix_list.append(operator_stack.pop())
                self.apply_rules(item, operator_stack)
            elif self.operators[item] > self.operators[operator_stack[len(operator_stack) - 1]]:
                operator_stack.append(item)
            else:
                self.postfix_list.append(operator_stack.pop())
                self.apply_rules(item, operator_stack)
    def get_postfix_notation(self):
        operator_stack = []
        for item in self.infix_list:
            self.apply_rules(item, operator_stack)
        while len(operator_stack) > 0:
            self.postfix_list.append(operator_stack.pop())
        return self.postfix_list;

    def is_number(self, item):
        test_m = matrix([])
        if type(item) == type(test_m) or item not in self.operators_set:
            return True
        else:
            return False

    def calculate(self):
        self.get_postfix_notation()
        calculation_stack = []
        for item in self.postfix_list:
            if self.is_number(item):
                calculation_stack.append(item)
            elif len(calculation_stack) > 0:
                if item == '*':
                    right = calculation_stack.pop()
                    left = calculation_stack.pop()
                    if type(left) == type(matrix([])):
                        calculation_stack.append(numpy.multiply(left, right))
                    else:
                        calculation_stack.append(left * right)
                elif item == '/':
                    right = calculation_stack.pop()
                    left = calculation_stack.pop()
                    if type(left) == type(matrix([])):
                        calculation_stack.append(numpy.divide(left, right))
                    else:
                        calculation_stack.append(left / right)
                elif item == '+':
                    right = calculation_stack.pop()
                    left = calculation_stack.pop()
                    calculation_stack.append(left + right)
                elif item == '-':
                    right = calculation_stack.pop()
                    left = calculation_stack.pop()
                    calculation_stack.append(left - right)
        return calculation_stack.pop()