import collections


class CellContainer:
    def has_number(self, num):
        pass

    def predict(self, num, positions):
        pass

    def update_numbers(self):
        pass


class Square(CellContainer):
    def __init__(self, ystart, xstart, data, number, size=3):
        self.data = []
        self.ystart = ystart
        self.xstart = xstart
        self.size = size
        # self.free_cells = []

        # number of square:
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.number = number
        for i in range(ystart, ystart + size):
            self.data.append([])
            for j in range(xstart, xstart + size):
                # if data[i][j].value == ' ':
                #     self.free_cells.append((i, j))
                self.data[-1].append(data[i][j])
        self.update_numbers()

    def update_numbers(self):
        # remove numbers that already in square
        changed = False
        for i in range(self.size**2):
            update_cell = self.data[i // self.size][i % self.size]
            for j in range(self.size**2):
                iterate_cell = self.data[j // self.size][j % self.size]
                result = update_cell.remove_available(iterate_cell.value)
                if result:
                    changed = True
                    self.update_numbers()
        return changed

    def list_elements(self):
        result = []
        for row in self.data:
            result.extend(row)
        return result

    # def remove_occupied_positions(self, positions):
    #     for pos in positions:
    #         if self.valid_row_position(pos):
    #             self.free_cells = [self.free_cells[i] for i in range(len(self.free_cells))
    #                                if self.free_cells[i][0] != pos[0]]
    #
    #         if self.valid_column_position(pos):
    #             self.free_cells = [self.free_cells[i] for i in range(len(self.free_cells))
    #                                if self.free_cells[i][1] != pos[1]]

    def predict(self, num, positions):
        changed = False
        for pos in positions:
            if self.valid_row_position(pos):
                row_with_that_number = [self.data[pos[0] - self.ystart][i] for i in range(self.size)]
                for cell in row_with_that_number:
                    changed |= cell.remove_available(num)

            if self.valid_column_position(pos):
                column_with_that_number = [self.data[i][pos[1] - self.xstart] for i in range(self.size)]
                for cell in column_with_that_number:
                    changed |= cell.remove_available(num)

        number_counter = collections.defaultdict(lambda: [])
        for row in self.data:
            for elem in row:
                for available in elem.available_numbers:
                    number_counter[available].append(elem.position)

        for available_number, lcells in number_counter.items():
            if len(lcells) == 1:
                y, x = lcells[0]
                self.data[y - self.ystart][x - self.xstart].set_value(available_number)
                changed = True

        if changed:
            self.update_numbers()
        return changed

        cells_with_alaivable_positions = []
        # for i in range(self.size**2):
        #     cell = self.data[i // self.size][i % self.size]
        #     if cell.value == ' ' and len(cell.available_numbers) == 1:
        #         cell.set_value(cell.available_numbers[0])

    def valid_row_position(self, pos):
        return self.ystart <= pos[0] < self.ystart + 3

    def valid_column_position(self, pos):
        return self.xstart <= pos[1] < self.xstart + 3

    def has_number(self, num):
        for row in self.data:
            if num in row:
                return True
        return False

    def __repr__(self):
        # strs = []
        # for row in self.data:
        #     strs.append(' . '.join([r.value for r in row]))
        # return ', '.join(strs)
        return str(self.ystart // 3 * 3 + self.xstart // 3)


class Row(CellContainer):
    def __init__(self, row_number, field):
        self.elems = []
        self.number = row_number

        for i in range(len(field[self.number])):
            self.elems.append(field[self.number][i])

        self.update_numbers()

    def update_numbers(self):
        changed = False
        for i in range(len(self.elems)):
            update_cell = self.elems[i]
            if update_cell.value == ' ':
                for j in range(len(self.elems)):
                    iterate_cell = self.elems[j]
                    result = update_cell.remove_available(iterate_cell.value)
                    if result:
                        changed = True
                        self.update_numbers()
        return changed

    def has_number(self, num):
        return num in self.elems

    def predict(self, num, positions):
        changed = False
        for pos in positions:
            cell = self.elems[pos[1]]
            changed |= cell.remove_available(num)

        number_counter = collections.defaultdict(lambda: [])
        for i in range(len(self.elems)):
            for available in self.elems[i].available_numbers:
                number_counter[available].append(i)

        for available_number, lcells in number_counter.items():
            if len(lcells) == 1:
                icell = lcells[0]
                self.elems[icell].set_value(available_number)
                changed = True

        if changed:
            self.update_numbers()
        return changed

    def __repr__(self):
        return 'R: ' + str(self.number)


class Column(CellContainer):
    def __init__(self, column_number, field):
        self.elems = []
        self.number = column_number

        for i in range(len(field)):
            self.elems.append(field[i][self.number])

        self.update_numbers()

    def update_numbers(self):
        changed = False
        for i in range(len(self.elems)):
            update_cell = self.elems[i]
            for j in range(len(self.elems)):
                iterate_cell = self.elems[j]
                result = update_cell.remove_available(iterate_cell.value)
                if result:
                    changed = True
                    self.update_numbers()
        return changed

    def has_number(self, num):
        return num in self.elems

    def predict(self, num, positions):
        changed = False
        for pos in positions:
            cell = self.elems[pos[0]]
            changed |= cell.remove_available(num)

        number_counter = collections.defaultdict(lambda: [])
        for i in range(len(self.elems)):
            for available in self.elems[i].available_numbers:
                number_counter[available].append(i)

        for available_number, lcells in number_counter.items():
            if len(lcells) == 1:
                icell = lcells[0]
                self.elems[icell].set_value(available_number)
                changed = True

        if changed:
            self.update_numbers()
        return changed

    def __repr__(self):
        return 'C: ' + str(self.number)
