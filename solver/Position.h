#ifndef POSITION_H
#define POSITION_H

#include <cstdint>
#include <limits>
#include <iostream>
#include <ctime>
#include "TranspositionTable.h"

class Position {
    private:
        using position_t = uint64_t;
        static constexpr uint64_t BOTTOM = 0x40810204081;
        static constexpr time_t TIMEOUT = 1;
        static constexpr int exploration_order[7] = {3, 2, 4, 1, 5, 0, 6};
        static position_t top_mask(int column);
        static position_t bottom_mask(int column);
        static position_t column_mask(int column);
        static bool is_alignment(position_t _board);

        position_t board;
        position_t mask;
        int num_moves;

        Position(const Position& other);

        bool can_play(int column) const;
        bool is_winning_move(int column) const;
        position_t key() const;
        int negamax(int alpha, int beta, TranspositionTable& table, time_t start) const;
        void play(int column);

        friend std::ostream& operator << (std::ostream& os, const Position& position);

    public:
        Position(const char* moves);
        int negamax(TranspositionTable& table);
        bool has_been_won();
};

std::ostream& operator << (std::ostream& os, const Position& position);

#endif