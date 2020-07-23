class Cell:
    def __init__(self, value, position):
        self.value = value
        self.position = position
        if self.value == 0:
            self.available_numbers = [i for i in range(1, 10)]
        else:
            self.available_numbers = []

    def get_row(self):
        return self.position[0]
    
    def get_column(self):
        return self.position[1]
    
    def get_square(self):
        return self.position[0] // 3 * 3 + self.position[1] // 3

    @property
    def is_occupied(self):
        return self.value != 0

    def remove_available(self, num):
        changed = False
        try:
            self.available_numbers.remove(num)
            changed = True
        except ValueError:
            pass
        if len(self.available_numbers) == 1:
            self.set_value(self.available_numbers[0])
            changed = True
        return changed

    def set_value(self, value):
        self.value = value
        if self.is_occupied:
            self.available_numbers = []

    def full_compare(self, other):
        return self.value == other.value and self.available_numbers == other.available_numbers

    def copy(self):
        new_cell = Cell(self.value, self.position)
        new_cell.available_numbers = self.available_numbers.copy()
        return new_cell

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.value == other.value
        else:
            return self.value == other

    def __lt__(self, other):
        return self.position < other.position

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.position)


