import collections


def list_checker(container):
    for list_from_container in container:
        original_set = set(range(1, 10))
        container_set = set([c.value for c in list_from_container.data])
        if original_set != container_set:
            return False
    return True


def check_sudoku(sudoku):
    result = True
    result &= list_checker(sudoku.rows)
    result &= list_checker(sudoku.columns)
    result &= list_checker(sudoku.squares)
    return result
