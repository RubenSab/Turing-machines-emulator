import sys


def parse_source_file(
    file: str
) -> tuple[list[str], dict[tuple[str, str], tuple[str, str, str]]]:
    rules = dict()
    with open(file, 'r') as f:
        input_symbols = f.readline().strip().split(' ')
        while True:
            line = f.readline()
            if not line:
                break
            if line.strip() == '':
                continue
            current_step, next_step = line.split('>')
            current_state, read_symbol = current_step.strip().split(' ')
            next_state, write_symbol, direction = next_step.strip().split(' ')
            rules[(current_state, read_symbol)] = (
                next_state, write_symbol, direction
            )
    return (input_symbols, rules)


class Tape:
    def __init__(self):
        self.tape = ['_']
        self.head = 0

    def clear_with_input(self, symbols: list[str]) -> None:
        self.tape = symbols[::]

    def read(self) -> str:
        return self.tape[self.head]

    def write(self, symbol: str) -> None:
        self.tape[self.head] = symbol

    def move_right(self) -> None:
        self.head += 1
        if self.head >= len(self.tape):
            self.tape.append('_')

    def move_left(self) -> None:
        self.head = max(self.head-1, 0)

    def __str__(self):
        return '| ' + '| '.join([
            f'{f"({self.tape[i]})":<5}'
            if i == self.head else f'{self.tape[i]:<5}'
            for i in range(len(self.tape))
        ]) + '|...'


class TM:
    def __init__(self, rules = dict[tuple[str, str], tuple[str, str, str]]):
        self.tape = Tape()
        self.rules = rules
        self.state = 'START'

    def get_input(self, symbols: list[str]) -> None:
        self.tape.clear_with_input(symbols)

    def step(self) -> None:
        delta_input = (self.state, self.tape.read())
        if delta_input in self.rules:
            next_state, write_symbol, direction = self.rules[delta_input]
        else:
            self.state = 'REJECT'
            return
        self.tape.write(write_symbol)
        if direction == 'L':
            self.tape.move_left()
        if direction == 'R':
            self.tape.move_right()
        self.state = next_state

    def execute(self) -> None:
        print(self, end='\n\n')
        while self.state != 'ACCEPT' and self.state != 'REJECT':
            self.step()
            print(self, end='\n\n')

    def __str__(self):
        return f'{f"{self.state}:":<7} {self.tape}'


if __name__=='__main__':
    input_symbols, rules = parse_source_file(sys.argv[1])
    tm = TM(rules)
    tm.get_input(input_symbols)
    tm.execute()
