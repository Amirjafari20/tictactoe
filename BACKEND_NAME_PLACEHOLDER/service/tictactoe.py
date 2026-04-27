from typing import List, Optional

def check_win(board: str) -> Optional[str]:
    # Board is a 9-char string, positions 0-8
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [2, 4, 6]              # diags
    ]
    for line in wins:
        a, b, c = line
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def check_draw(board: str) -> bool:
    return ' ' not in board and check_win(board) is None

def is_valid_move(board: str, position: int) -> bool:
    return 0 <= position < 9 and board[position] == ' '

def apply_move(board: str, position: int, player: str) -> str:
    return board[:position] + player + board[position+1:]
