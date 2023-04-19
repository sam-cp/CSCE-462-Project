#ifndef TRANSPOSITION_TABLE_H
#define TRANSPOSITION_TABLE_H

#include <cstdint>
#include <cstddef>

class TranspositionTable {
    public:
        using key_type = uint64_t;
        using value_type = uint8_t;
    private:
        struct Entry {
            key_type key: 56;
            value_type value;
        };
        static constexpr size_t SIZE = 65537;
        Entry table[SIZE];

        size_t index(key_type key) const;
    public:
        TranspositionTable();
        
        value_type get(key_type key) const;
        void put(key_type key, value_type value);
};

#endif