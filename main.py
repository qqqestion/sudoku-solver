from argparse import ArgumentParser

from sudoku import SudokuField
from fields import HardFieldGenerator, EasyFieldGenerator, ExpertFieldGenerator
from utils import check_sudoku


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', type=str, required=False)
    parsed_args = parser.parse_args()
    file = parsed_args.f
    return file


def get_field(file):
    if file:
        field = []
        with open(file, 'r') as fin:
            for line in fin.readlines():
                field.append(list(map(int, line.split())))
    else:
        field = EasyFieldGenerator.generate()
    return field


def run_solver(field):
    sudoku = SudokuField(field)
    while not check_sudoku(sudoku):
        sudoku.changed = False
        for num in sudoku.available_numbers:
            positions = sudoku.get_positions_of_num(num)
            for list_of_containers in [sudoku.squares, sudoku.rows, sudoku.columns]:
                containers_without_number = sudoku.get_containers_without_number(num,
                                                                                 list_of_containers)
                sudoku.predict(containers_without_number, num, positions)
            sudoku.update_all()
        if not sudoku.changed:
            sudoku.pick_random()
        if sudoku.is_complete and not check_sudoku(sudoku):
            sudoku.back_up()
        print(sudoku)

    print('Solution')
    print(sudoku)
    if check_sudoku(sudoku):
        check_msg = "Sudoku is correct"
    else:
        check_msg = "Sorry, something went wrong. Sudoku is incorrect"
    print(check_msg)


def main():
    file = parse_args()
    run_solver(get_field(file))


if __name__ == '__main__':
    main()
