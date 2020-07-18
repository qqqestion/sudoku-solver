from abc import ABC, abstractmethod
import collections


class CellContainer(ABC):
    def __init__(self, number):
        self.data = []
        self.number = number

    def has_number(self, num):
        return num in self.data

    def remove_number(self, to_save, number):
        for i in range(len(self.data)):
            if i not in to_save:
                self.data[i].remove_available(number)

    def set_available(self, sudoku):
        number_counter = collections.defaultdict(lambda: [])
        changed = False
        for i in range(len(self.data)):
            for available in self.data[i].available_numbers:
                number_counter[available].append(i)

        pairs = []
        for available_number, lcells in number_counter.items():
            if len(lcells) == 1:
                icell = lcells[0]
                self.data[icell].set_value(available_number)
                changed = True
            elif len(lcells) == 2:
                p1, p2 = tuple([self.data[icell] for icell in lcells])
                pairs.append((p1, p2))

                if p1.get_row() == p2.get_row():
                    row = sudoku.get_row(p1.get_row())
                    row.remove_number([p1.get_column(), p2.get_column()],
                                      available_number)
                if p1.get_column() == p2.get_column():
                    column = sudoku.get_column(p1.get_column())
                    column.remove_number([p1.get_row(), p2.get_row()],
                                         available_number)
            elif len(lcells) == 3:
                pass

        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                p1 = pairs[i]
                p2 = pairs[j]
                if p1[0].available_numbers == p2[0].available_numbers and \
                        p1[1].available_numbers == p2[1].available_numbers:
                    s1 = set(p1[0].available_numbers)
                    s2 = set(p1[1].available_numbers)
                    excess_elements = s1.difference(s2)
                    for elem in excess_elements:
                        p1[0].remove_available(elem)
                        p1[1].remove_available(elem)
                    changed = True

        return changed

    def predict(self, num, positions: list, sudoku):
        changed = False
        for pos in positions:
            cell = self.get_element(pos)
            changed |= cell.remove_available(num)
            if changed:
                if cell.value == num:
                    positions.append(cell.position)
                sudoku.update_all()
            # if changed and cell.value == num:
            #     positions.append(cell.position)

        changed |= self.set_available(sudoku)

        return changed

    def update_numbers(self):
        changed = False
        for i in range(len(self.data)):
            update_cell = self.data[i]
            for j in range(len(self.data)):
                iterate_cell = self.data[j]
                result = update_cell.remove_available(iterate_cell.value)
                if result:
                    changed = True
                    self.update_numbers()
        return changed

    @abstractmethod
    def get_element(self, pos):
        pass

    def __next__(self):
        if self.i < 9:
            elem = self.data[self.i]
            self.i += 1
            return elem
        raise StopIteration

    def __iter__(self):
        self.i = 0
        return self


class Square(CellContainer):
    def __init__(self, ystart, xstart, data):
        super().__init__(data[ystart][xstart].get_square())
        self.ystart = ystart
        self.xstart = xstart
        self.size = 3

        for i in range(ystart, ystart + self.size):
            for j in range(xstart, xstart + self.size):
                self.data.append(data[i][j])
        self.update_numbers()

    def predict(self, num, positions, sudoku):
        changed = False
        for pos in positions:
            if self.valid_row_position(pos):
                row_with_that_number = [self.data[(pos[0] - self.ystart) * 3 + i] for i in range(self.size)]
                for cell in row_with_that_number:
                    changed |= cell.remove_available(num)
                    if changed:
                        if cell.value == num:
                            positions.append(cell.position)
                        sudoku.update_all()

            if self.valid_column_position(pos):
                column_with_that_number = [self.data[i * 3 + pos[1] - self.xstart] for i in range(self.size)]
                for cell in column_with_that_number:
                    changed |= cell.remove_available(num)
                    if changed:
                        if cell.value == num:
                            positions.append(cell.position)
                    sudoku.update_all()
                    # if changed and cell.value == num:
                    #     positions.append(cell.position)

        changed |= self.set_available(sudoku)

        return changed

    def valid_row_position(self, pos):
        return self.ystart <= pos[0] < self.ystart + 3

    def valid_column_position(self, pos):
        return self.xstart <= pos[1] < self.xstart + 3

    def get_element(self, pos):
        return self.data[(pos[0] - self.ystart) * 3 + pos[1] - self.xstart]

    def __repr__(self):
        return 'Q: ' + str(self.number)


class Row(CellContainer):
    def __init__(self, row_number, field):
        super(Row, self).__init__(row_number)

        for i in range(len(field[self.number])):
            self.data.append(field[self.number][i])

        self.update_numbers()

    def get_element(self, pos):
        return self.data[pos[1]]

    def __repr__(self):
        return 'R: ' + str(self.number)


class Column(CellContainer):
    def __init__(self, column_number, field):
        super(Column, self).__init__(column_number)

        for i in range(len(field)):
            self.data.append(field[i][self.number])

        self.update_numbers()

    def get_element(self, pos):
        return self.data[pos[0]]

    def __repr__(self):
        return 'C: ' + str(self.number)
