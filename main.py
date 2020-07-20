from sudoku import SudokuField
from fields import HardFieldGenerator, EasyFieldGenerator, ExpertFieldGenerator
from utils import check_sudoku, compare


def main():
    sudoku = SudokuField(ExpertFieldGenerator())
    print('We are currently working on the solution...')
    while not check_sudoku(sudoku):
        for num in sudoku.available_numbers:
            positions = sudoku.get_positions_of_num(num)
            for list_of_containers in [sudoku.squares, sudoku.rows, sudoku.columns]:
                containers_without_number = sudoku.get_containers_without_number(num,
                                                                                 list_of_containers)
                sudoku.predict(containers_without_number, num, positions)

        print('Solution')
        print(sudoku)
    if check_sudoku(sudoku):
        check_msg = "Sudoku is correct"
    else:
        check_msg = "Sorry, something went wrong. Sudoku is incorrect"
    print(check_msg)

    if compare(sudoku):
        compare_msg = "Comparing with correct version is successful"
    else:
        compare_msg = "During comparing with correct version we got some trouble"
    print(compare_msg)


if __name__ == '__main__':
    main()
