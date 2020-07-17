class Cell:
    def __init__(self, value, position):
        self.value = value
        self.position = position
        if self.value == ' ':
            self.available_numbers = [str(i) for i in range(1, 10)]
        else:
            self.available_numbers = []

    def get_row(self):
        return self.position[0]
    
    def get_column(self):
        return self.position[1]
    
    def get_square(self):
        return self.position[0] // 3 * 3 + self.position[1] // 3

    def is_occupied(self):
        return self.value != ' '
    
    def remove_available(self, num):
        try:
            self.available_numbers.remove(num)
        except ValueError:
            pass
        if len(self.available_numbers) == 1:
            self.set_value(self.available_numbers[0])
            return True
        return False

    def set_value(self, value):
        self.value = value
        if self.is_occupied:
            self.available_numbers = []
    
    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.value == other.value
        else:
            return self.value == other

    def __cmp__(self, other):
        return self.position == other.position and self.available_numbers == self.available_numbers

    def __lt__(self, other):
        if isinstance(other, Cell):
            return self.value < other.value
        else:
            return self.value < other

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

