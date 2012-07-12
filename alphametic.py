import re
import itertools


def solve(puzzle):
    ''' Solving puzzles like "A + B == C" or "2 * 3 == 6" '''

    words = re.findall('[A-Z]+', puzzle)
    if not words:
        words = re.findall('\d+', puzzle)

    unique_chars = set(''.join(words))
    assert len(unique_chars) <= 10, 'Cannot handle more than 10 letters!'

    chars = tuple(ord(c) for c in unique_chars)
    digits = tuple(ord(d) for d in '0123456789')

    invalid = re.compile('(\D|^)0\d*')
    for guess in itertools.permutations(digits, len(unique_chars)):
        equation = puzzle.translate(dict(zip(chars, guess)))
        print(equation, end='\r')
        if not invalid.search(equation):
            if eval(equation, {}, {}):
                print(equation)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('\n  Usage: $ python3 alphametic.py "equation"\n')
        exit()

    puzzle = sys.argv[1].upper()
    print('\n' + puzzle)
    print('-' * len(puzzle))
    solve(puzzle)
    print('-' * len(puzzle) + '\n')
