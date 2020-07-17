from cells import Cell
from components import Square, Row, Column


class SudokuField:
    def __init__(self, gen):
        self.generator = gen
        self.correct_field = self.generator.generate_correct()
        self.field = self.generator.generate()
        self.is_complete = False
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
                                           self.field,
                                           self.field[i][j].get_square()))
        self.rows = []
        for i in range(len(self.field)):
            self.rows.append(Row(i, self.field))

        self.columns = []
        for i in range(len(self.field)):
            self.columns.append(Column(i, self.field))

        self.update_numbers()

    def update_numbers(self):
        for sq in self.squares:
            result = sq.update_numbers()
            if result:
                self.update_numbers()
        for row in self.rows:
            result = row.update_numbers()
            if result:
                self.update_numbers()
        for column in self.columns:
            result = column.update_numbers()
            if result:
                self.update_numbers()

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

    def set_num(self, num, pos):
        self.field[pos[0]][pos[1]] = Cell(num, (pos[0], pos[1]))
        counter = 0
        for row in self.field:
            for elem in row:
                if elem == num:
                    counter += 1
        if counter == 9:
            self.available_numbers.remove(num)
            self.is_complete = not self.available_numbers

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

    def __str__(self):
        strs = []
        for row in self.field:
            strs.append(' . '.join([r.value for r in row]))
        return '\n'.join(strs)
