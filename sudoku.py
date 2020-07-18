from cells import Cell
from components import Square, Row, Column


class SudokuField:
    def __init__(self, gen):
        self.generator = gen
        self.correct_field = self.generator.generate_correct()
        self.field = self.generator.generate()
        self.available_numbers = set()

        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                self.field[i][j] = Cell(self.field[i][j], (i, j))
                self.available_numbers.add(self.field[i][j].value)

        self.available_numbers.remove(' ')

        self.squares = []
        for i in range(0, len(self.field), 3):
            for j in range(0, len(self.field[i]), 3):
                self.squares.append(Square(i,
                                           j,
                                           self.field))
        self.rows = []
        for i in range(len(self.field)):
            self.rows.append(Row(i, self.field))

        self.columns = []
        for i in range(len(self.field)):
            self.columns.append(Column(i, self.field))

        self.update_all()

    def update_container(self, list_of_containers):
        for cont in list_of_containers:
            result = cont.update_numbers()
            if result:
                return True
        return False

    def update_all(self):
        square_result = self.update_container(self.squares)
        if square_result:
            self.update_all()
        row_result = self.update_container(self.rows)
        if row_result:
            self.update_all()
        column_result = self.update_container(self.columns)
        if column_result:
            self.update_all()

    def get_positions_of_num(self, num):
        positions = []
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.field[i][j].value == num:
                    positions.append((i, j))
        return positions

    def get_squares_without_number(self, num):
        squares = []
        for sq in self.squares:
            if not sq.has_number(num):
                squares.append(sq)
        return squares

    def get_rows_without_number(self, number):
        rows = []
        for r in self.rows:
            if not r.has_number(number):
                rows.append(r)
        return rows

    def get_columns_without_number(self, number):
        columns = []
        for c in self.columns:
            if not c.has_number(number):
                columns.append(c)
        return columns

    def get_row(self, irow):
        return self.rows[irow]

    def get_column(self, icolumn):
        return self.columns[icolumn]

    def __repr__(self):
        strs = []
        for row in self.field:
            strs.append(' . '.join([r.value for r in row]))
        return '\n'.join(strs)
