import typing
from . import _tic_tac_toe

class UltimateTicTacToe:
    """
    1. **The game is played on a 3 x 3 grid of smaller tic-tac-toe boards.** This creates a total of 81 squares to play in.  
    2. **Players take turns, starting with `X`.**  
    3. **On your turn, place your mark (`X` or `O`) in any empty square of the small board you're allowed to play in.** The starting player can choose any square on any small board.  
    4. **Your move determines where your opponent will play next.** The square you choose within a small board corresponds to the location of the next small board in the larger grid where your opponent must play. For example:  
    - If you play in the top-left square of a small board, your opponent must play in the top-left small board of the larger grid.  
    5. **If your opponent is sent to a full or won small board, they can play in any other board.**  
    6. **To win a small board, get three of your marks in a row (up, down, across, or diagonally) on that board.** Once a small board is won, it is marked with a large `X` or `O`, and no further moves can be made in that board.  
    7. **The goal is to win the larger board by winning three small boards in a row.** This can be achieved vertically, horizontally, or diagonally.  
    8. **The game ends when one player wins the larger board or when no legal moves remain.** If no player wins the larger board and all possible moves are used up, the game is a draw.  
    """

    grid: list[list[_tic_tac_toe.TicTacToe]]
    turn: typing.Literal["X"] | typing.Literal["O"]
    next_small_board: _tic_tac_toe.TicTacToe | None

    def __init__(self) -> None:
        self.grid = [[_tic_tac_toe.TicTacToe() for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        self.next_small_board = None

    def can_play(self, space1: tuple[int, int], space2: tuple[int, int]) -> bool:
        if self.winner:
            return False
        if self.next_small_board and self.grid[space1[0]][space1[1]] != self.next_small_board:
            return False
        return self.grid[space1[0]][space1[1]].can_play(space2)

    def play(self, space1: tuple[int, int], space2: tuple[int, int]) -> None:
        if not self.can_play(space1, space2):
            raise ValueError("Invalid move")
        self.grid[space1[0]][space1[1]].play(space2)
        for i in self.grid:
            for j in i:
                j.turn = "X" if self.turn == "O" else "O"
        self.turn = "X" if self.turn == "O" else "O"
        self.next_small_board = self.grid[space2[0]][space2[1]] if not self.grid[space2[0]][space2[1]].winner else None

    @property
    def winner(self) -> typing.Literal["X"] | typing.Literal["O"] | None:
        for i in range(3):
            if self.grid[i][0].winner == self.grid[i][1].winner == self.grid[i][2].winner is not None:
                return self.grid[i][0].winner
            if self.grid[0][i].winner == self.grid[1][i].winner == self.grid[2][i].winner is not None:
                return self.grid[0][i].winner
        if self.grid[0][0].winner == self.grid[1][1].winner == self.grid[2][2].winner is not None:
            return self.grid[0][0].winner
        if self.grid[0][2].winner == self.grid[1][1].winner == self.grid[2][0].winner is not None:
            return self.grid[0][2].winner
        return None