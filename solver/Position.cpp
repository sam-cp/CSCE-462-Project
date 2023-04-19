#include "Position.h"
#include <stdexcept>

Position::position_t Position::top_mask(int column) {
    return bottom_mask(column) << 5;
}

Position::position_t Position::bottom_mask(int column) {
    return BOTTOM & column_mask(column);
}

Position::position_t Position::column_mask(int column) {
    position_t _column_mask = 0x7F;
    return _column_mask << (7 * column);
}

bool Position::is_alignment(position_t _board) {
    // Check for vertical alignment
    position_t adjacent_vertical = _board & (_board >> 1);
    if (adjacent_vertical & (adjacent_vertical >> 2)) {
        return true;
    }

    // Check for horizontal alignment
    position_t adjacent_horizontal = _board & (_board >> 7);
    if (adjacent_horizontal & (adjacent_horizontal >> 14)) {
        return true;
    }

    // Check for diagonal alignment (/)
    position_t adjacent_diagonal1 = _board & (_board >> 8);
    if (adjacent_diagonal1 & (adjacent_diagonal1 >> 16)) {
        return true;
    }

    // Check for diagonal alignment (\)
    position_t adjacent_diagonal2 = _board & (_board >> 6);
    if (adjacent_diagonal2 & (adjacent_diagonal2 >> 12)) {
        return true;
    }

    return false;
}

Position::Position(const Position& other)
    :board(other.board), mask(other.mask), num_moves(other.num_moves) {}

bool Position::can_play(int column) const {
    return (mask & top_mask(column)) == 0;
}

bool Position::is_winning_move(int column) const {
    position_t new_board = board | ((mask + BOTTOM) & column_mask(column));
    return is_alignment(new_board);
}

Position::position_t Position::key() const {
    return board + mask + BOTTOM;
}

int Position::negamax(int alpha, int beta, TranspositionTable& table, time_t start) const {
    /*if (time(nullptr) > start + TIMEOUT) {
        throw std::runtime_error("Timeout");
    }*/
    if (num_moves == 42) {
        return 0;
    }

    for (int i = 0; i < 7; i++) {
        int col = exploration_order[i];
        if (can_play(col) && is_winning_move(col)) {
            return (43 - num_moves) / 2;
        }
    }

    int max = (41 - num_moves) / 2;
    if (int stored = table.get(board + mask)) {
        max = stored - 21;
    }
    if (beta > max) {
        beta = max;
        if (alpha >= beta) {
            return beta;
        }
    }

    for (int i = 0; i < 7; i++) {
        int col = exploration_order[i];
        if (can_play(col)) {
            Position new_position = *this;
            new_position.play(col);
            int score = -new_position.negamax(-beta, -alpha, table, start);

            if (score >= beta) {
                return beta;
            }
            if (score > alpha) {
                alpha = score;
            }
        }
    }
    table.put(board + mask, alpha + 21);
    return alpha;
}

void Position::play(int column) {
    board ^= mask;
    mask |= mask + bottom_mask(column);
    ++num_moves;
}


// Public methods

Position::Position(const char* moves)
    :board(0), mask(0), num_moves(0) {
    for (const char* i = moves; *i; ++i) {
        if (*i < '1' || *i > '7') {
            throw std::invalid_argument("Column index must be between 1 and 7.");
        }
        if (can_play(*i - '1')) {
            bool won = is_winning_move(*i - '1');
            play(*i - '1');
            if (won) return;
        } else {
            throw std::invalid_argument("Too many plays in a column.");
        }
    }
    if (num_moves > 42) {
        throw std::invalid_argument("Too many moves.");
    }
}

int Position::negamax(TranspositionTable& table) {
    return negamax(-21, 21, table, time(nullptr));
}


// Other methods

std::ostream& operator << (std::ostream& os, const Position& position) {
    // Assume X is first, O is second
    bool x_is_1 = position.num_moves % 2 == 0;
    for (int row = 6; row-- > 0; ) {
        Position::position_t row_mask = Position::BOTTOM << row;
        for (int column = 0; column < 7; ++column) {
            Position::position_t cell_mask = Position::column_mask(column) & row_mask;
            if (position.mask & cell_mask) {
                if (position.board & cell_mask) {
                    os << (x_is_1 ? 'x' : 'o');
                } else {
                    os << (x_is_1 ? 'o' : 'x');
                }
            } else {
                os << ' ';
            }
        }
        if (row > 0) {
            os << std::endl;
        }
    }
    return os;
}

bool Position::has_been_won() {
    return is_alignment(board) || is_alignment(board ^ mask);
}