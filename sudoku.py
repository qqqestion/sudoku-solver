from random import randint

from cells import Cell
from components import Square, Row, Column
from utils import check_sudoku


class SudokuField:
    def __init__(self, field):
        self.field = field
        self.original_field = []
        self.available_numbers = set()
        self.random_cell = None
        self.changed = False

        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                self.field[i][j] = Cell(self.field[i][j], (i, j))
                self.available_numbers.add(self.field[i][j].value)

        self.available_numbers.remove(0)

        self.squares = []
        self.rows = []
        self.columns = []

        self.initiate_containers()

    def initiate_containers(self):
        for i in range(len(self.field)):
            self.squares.append(Square(i // 3 * 3,
                                       i % 3 * 3,
                                       self.field))
            self.rows.append(Row(i, self.field))
            self.columns.append(Column(i, self.field))
        self.update_all()

    def delete_containers(self):
        self.rows = []
        self.columns = []
        self.squares = []

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
        for c in list_of_containers:
            changed = c.predict(num, positions, self)
            if changed:
                self.changed = True
                self.update_all()

    def get_containers_without_number(self, num, list_of_containers):
        containers = []
        for c in list_of_containers:
            if not c.has_number(num):
                containers.append(c)
            else:
                c.remove_number([i for i in range(len(c.data)) if c.data[i].value == num], num)
        return containers

    def get_row(self, irow):
        return self.rows[irow]

    def get_column(self, icolumn):
        return self.columns[icolumn]

    def _get_random(self):
        free_cells = []
        for row in self.field:
            for cell in row:
                if cell.value == ' ' and len(cell.available_numbers) == 2:
                    free_cells.append(cell)
        return free_cells[randint(0, len(free_cells) - 1)] if len(free_cells) > 0 else None

    def pick_random(self):
        # print('hello')
        if len(self.original_field):
            self.field = self.original_field
        self.original_field = []
        for row in self.field:
            self.original_field.append([])
            for cell in row:
                copy_cell = cell.copy()
                self.original_field[-1].append(copy_cell)
        random_cell = self._get_random()
        if random_cell:
            self.random_cell = random_cell.copy()
            random_cell.set_value(random_cell.available_numbers[randint(0, len(random_cell.available_numbers) - 1)])
            self.random_cell.value = random_cell.value
            self.delete_containers()
            self.initiate_containers()
            self.update_all()
        # self.field[0][0].set_value('9')
        a = 10

    # def pick_random(self):
    #     free_cells = self.get_free_cells
    #     self.original_field = self.copy_field()
    #

    def back_up(self):
        if self.random_cell is not None:
            cell = self.original_field[self.random_cell.position[0]][self.random_cell.position[1]]
            self.field = self.original_field
            value = [number for number in cell.available_numbers if number != self.random_cell.value]
            cell.set_value(*value)
            self.delete_containers()
            self.initiate_containers()

    @property
    def is_complete(self):
        for row in self.field:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def __repr__(self):
        strs = []
        for row in self.field:
            strs.append(' . '.join([str(r.value) for r in row]))
        return '\n'.join(strs)
