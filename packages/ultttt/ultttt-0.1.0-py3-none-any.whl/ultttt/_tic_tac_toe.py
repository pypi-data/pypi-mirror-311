import typing

class TicTacToe:
    """
    1.  The game is played on a grid that's 3 squares by 3 squares.
    2.  You are `X`, your friend (or the computer in this case) is `O`. Players take turns putting their marks in empty squares.
    3.  The first player to get 3 of their marks in a row (up, down, across, or diagonally) is the winner.
    4.  When all 9 squares are full, the game is over. If no player has 3 marks in a row, the game ends in a tie.
    """

    grid: list[list[typing.Literal["X"] | typing.Literal["O"] | None]]
    turn: typing.Literal["X"] | typing.Literal["O"]

    def __init__(self) -> None:
        self.grid = [[None for _ in range(3)] for _ in range(3)]
        self.turn = "X"

    def can_play(self, space: tuple[int, int]) -> bool:
        return not self.winner and not self.grid[space[0]][space[1]]

    def play(self, space: tuple[int, int]) -> None:
        if not self.can_play(space):
            raise ValueError("Invalid move")
        self.grid[space[0]][space[1]] = self.turn
        self.turn = "X" if self.turn == "O" else "O"

    @property
    def winner(self) -> typing.Literal["X"] | typing.Literal["O"] | None:
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] is not None:
                return self.grid[i][0]
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] is not None:
                return self.grid[0][i]
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] is not None:
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] is not None:
            return self.grid[0][2]
        return None