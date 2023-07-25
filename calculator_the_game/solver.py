from typing import List, Dict, Tuple, Callable


class Node:
    def __init__(self, value: int, moves: int, parent: Node=None) -> None:
        self.children: List[Node] = list()
        self.value: int = value
        self.moves: int = moves
        self.parent: Node = parent


    def get_path(self, path: List[Node]=list()) -> List[Node]:
        path.append(self)
        if path[-1].parent is None:
            return path
        else:
            return self.get_path(path)
        

    def __str__(self) -> str:
        return str(self.value)
    

    def create_children(self) -> List[Node]:
        if moves < 1:
            return list()
        
        children: List[Node] = list()

        for func, num in functions:
            new_value: int = func(self.value, num)
            children.append(Node(new_value, self.moves-1, self))

        return children     

    
def add(a: int, b: int) -> int:
    return a + b


def substract(a: int, b: int) -> int:
    return a - b


def multiply(a: int, b: int) -> int:
    return a * b


def divide(a: int, b: int) -> int:
    return a // b


def create_tree(moves: int, goal: int, start: int, functions: List[Tuple[Callable, int]]) -> List[Node]:
    root: Node = Node(start, moves)



def ask_functions() -> List[Tuple[Callable, int]]:
    function_map: Dict[str, Callable] = {'+': add,
                                            '-': substract,
                                            '*': multiply,
                                            '/': divide}
    
    while True:            
        functions: List[Tuple[Callable, int]] = list() 
        inp: List[str] = input('Pleae enter the available functions >> ').split()

        for f in inp:
            try:
                assert f[0] in function_map.keys()
                number: int = int(f[1:])
                functions.append((function_map.get(f[0]), number))
            except ValueError:
                print('Please enter valid numbers', end='')
            except AssertionError:
                print('Please enter valid operators')

        if len(functions) == len(inp):
            break

    return functions 
    

def ask_value(sentence: str, positive: bool) -> int:
    number: str = input(f'{sentence} >> ')
    while True:
        try:
            number: int = int(number)
            if positive:
                assert number >= 0
            return number
        except ValueError:
            number: str = input('Please enter a number >> ')
        except AssertionError:
            number: str = input('Please enter a postive number >> ')
        


    



if __name__ == '__main__':
    moves: int = ask_value('How many moves?', True)
    goal: int = ask_value('What is the goal?', False)
    start: int = ask_value('What is the starting number?', False)
    functions: List[Tuple[Callable, int]] = ask_functions()
    