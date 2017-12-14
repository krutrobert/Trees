from tree import Tree
from tree import TreeNode
from operator import itemgetter
from calculator import Calculator

def print_list(list):
    list_string = ''
    for item in list:
        list_string += str(item) + '\t'
    print(list_string)

symbol_set = set(r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
numerics_set = set(r'1234567890. ')
operators_set = set(r'+-*/() ')

user_input = ''
tree = None
calc = Calculator()

print()

while user_input != 'exit':
    user_input = input()

    if len(user_input) > 4 and user_input[0:4] == 'tree':
        current_item = ''
        for char in user_input[4:]:
            if char in symbol_set:
                current_item += char
        tree = Tree(current_item)
    elif len(user_input) > 3 and user_input[0:3] == 'add':
        current_item = ''
        parent = ''
        children = []
        for char in user_input[4:]:
            if char in symbol_set:
                current_item += char
            elif char == ':':
                parent = current_item
                current_item = ''
            elif char == ',':
                children.append(current_item)
                current_item = ''
        if current_item != '':
            children.append(current_item)
            current_item = ''
        if parent != '':
            for child in children:
                tree.add_node(parent, child)
    elif len(user_input) > 4 and user_input[0:5] == 'print':
        if tree == None:
            print('Дерево пусте!\n')
            continue
        print(tree.root)
    elif len(user_input) > 8 and user_input[0:9] == 'postorder':
        if tree == None:
            print('Дерево пусте!\n')
            continue
        print_list(tree.get_postorder_list())
    else:
        invalid_input = False
        for item in user_input:
            if item in operators_set or item in numerics_set:
                continue
            else:
                invalid_input = True
                break

        if invalid_input:
            print('Invalid input!')
            continue

        calc.set_infix_string(user_input)
        postfix = calc.get_postfix_notation()
        memory = []
        i = 0
        while len(postfix) > i:
            current = postfix[i]
            if current in operators_set:
                node = TreeNode(current)
                child2 = memory.pop()
                child1 = memory.pop()
                child1.set_parent(node)
                child2.set_parent(node)
                node.add_child(child1)
                node.add_child(child2)
                memory.append(node)
            else:
                node = TreeNode(current)
                memory.append(node)
            i += 1
        tree = Tree('0')
        tree.root = memory.pop()
        print(tree.root)
        print('result:', calc.calculate())
    print()