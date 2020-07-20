from cells import Cell
from components import Square, Row, Column


class SudokuField:
    def __init__(self, gen):
        self.generator = gen
        self.field = self.generator.generate()
        self.available_numbers = set()

        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                self.field[i][j] = Cell(self.field[i][j], (i, j))
                self.available_numbers.add(self.field[i][j].value)

        self.available_numbers.remove(' ')

        self.squares = []
        self.rows = []
        self.columns = []
        for i in range(len(self.field)):
            self.squares.append(Square(i // 3 * 3,
                                       i % 3 * 3,
                                       self.field))
            self.rows.append(Row(i, self.field))
            self.columns.append(Column(i, self.field))

        self.update_all()

    def update_container(self, list_of_containers):
        for cont in list_of_containers:
            result = cont.update_numbers()
            if result:
                return True
        return False

    def update_all(self):
        for list_of_containers in [self.squares, self.rows, self.columns]:
            result = self.update_container(list_of_containers)
            if result:
                self.update_all()

    def get_positions_of_num(self, num):
        positions = []
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.field[i][j].value == num:
                    positions.append((i, j))
        return positions

    def predict(self, list_of_containers, num, positions):
        for s in list_of_containers:
            changed = s.predict(num, positions, self)
            if changed:
                self.update_all()

    def get_containers_without_number(self, num, list_of_containers):
        containers = []
        for c in list_of_containers:
            if not c.has_number(num):
                containers.append(c)
        return containers

    def get_row(self, irow):
        return self.rows[irow]

    def get_column(self, icolumn):
        return self.columns[icolumn]

    def __repr__(self):
        strs = []
        for row in self.field:
            strs.append(' . '.join([r.value for r in row]))
        return '\n'.join(strs)
