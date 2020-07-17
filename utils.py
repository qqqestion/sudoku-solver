import collections

from sudoku import SudokuField


def list_checker(container):
    for list_from_container in container:
        counter = collections.Counter(list_from_container.elems)
        num, count = counter.most_common(1)[0]
        if num == ' ' or count != 1:
            # print(num, count)
            raise RuntimeError


def squares_checker(squares):
    for sq in squares:
        counter = collections.Counter(sq.list_elements())
        num, count = counter.most_common(1)[0]
        if num == ' ' or count != 1:
            raise RuntimeError


def check_sudoku(sudoku: SudokuField):
    try:
        list_checker(sudoku.rows)
        list_checker(sudoku.columns)
        squares_checker(sudoku.squares)
    except RuntimeError:
        return False
    return True


def compare(sudoku: SudokuField):
    for i in range(len(sudoku.field)):
        for j in range(len(sudoku.field[i])):
            if sudoku.field[i][j] != ' ' \
                    and sudoku.field[i][j] != sudoku.correct_field[i][j]:
                return False
    return True
