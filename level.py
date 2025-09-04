class Level:
    COLORS = {
        0: 'none',
        1: 'grey',
        2: 'baba',
        3: 'rock',
        4: 'is',
        5: 'baba_word',
        6: 'you_word',
        7: 'flag_word',
        8: 'win_word',
        9: 'flag',
        10: 'rock_word',
        11: 'push_word',
    }

    def __init__(self, rows, columns, grid):
        self.rows = rows
        self.columns = columns
        self.grid = grid

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as file:
            rows = 0
            columns = 0
            grid = []
            for line in file:
                nums = line.split()
                row = []
                for num in nums:
                    try:
                        row.append(cls.COLORS[int(num)])
                    except KeyError as e:
                        raise KeyError(f"Unknown color: {e}") from e
                if not columns:
                    columns = len(row)
                elif len(row) != columns:
                    raise ValueError("Inconsistent number of columns")
                rows += 1
                grid.append(row)
        return cls(rows, columns, grid)
