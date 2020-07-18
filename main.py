from sudoku import SudokuField
from fields import HardFieldGenerator, EasyFieldGenerator, ExpertFieldGenerator
from utils import check_sudoku, compare


def main():
    sudoku = SudokuField(ExpertFieldGenerator())
    print('We are currently working on the solution...')
    while not check_sudoku(sudoku):
        for num in sudoku.available_numbers:
            positions = sudoku.get_positions_of_num(num)

            squares = sudoku.get_squares_without_number(num)
            for s in squares:
                changed = s.predict(num, positions, sudoku)
                if changed:
                    sudoku.update_all()

            rows = sudoku.get_rows_without_number(num)
            for r in rows:
                changed = r.predict(num, positions, sudoku)
                if changed:
                    sudoku.update_all()

            columns = sudoku.get_columns_without_number(num)
            for c in columns:
                changed = c.predict(num, positions, sudoku)
                if changed:
                    sudoku.update_all()

        # print(sudoku)
        # print('-' * 20)
        # print(compare(sudoku))
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
