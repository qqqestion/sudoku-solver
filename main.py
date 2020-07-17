from sudoku import SudokuField
from fields import HardFieldGenerator, EasyFieldGenerator
from utils import check_sudoku, compare


def main():
    sudoku = SudokuField(HardFieldGenerator())
    print('Sudoku', sudoku, sep='\n')
    # print('Field', sudoku.field, sep='\n')
    # print('Squares', sudoku.squares, sep='\n')
    # print('Rows', sudoku.rows, sep='\n')
    # print('Column', sudoku.columns, sep='\n')
    # return
    while not check_sudoku(sudoku):
        for num in sudoku.available_numbers:
            positions = sudoku.get_positions_of_num(num)

            squares = sudoku.get_squares_without_number(num)
            for s in squares:
                changed = s.predict(num, positions)
                if changed:
                    sudoku.update_numbers()

            rows = sudoku.get_rows_without_number(num)
            for r in rows:
                changed = r.predict(num, positions)
                if changed:
                    sudoku.update_numbers()

            columns = sudoku.get_columns_without_number(num)
            for c in columns:
                changed = c.predict(num, positions)
                if changed:
                    sudoku.update_numbers()
            a = 10
            print(a)

        print(sudoku)
        print('-' * 20)
        print(compare(sudoku))
    print('Final')
    print(sudoku)

    print(check_sudoku(sudoku))


if __name__ == '__main__':
    main()
