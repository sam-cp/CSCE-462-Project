#include "TranspositionTable.h"

size_t TranspositionTable::index(key_type key) const {
    return key % SIZE;
}

TranspositionTable::TranspositionTable()
    :table{0} {}

TranspositionTable::value_type TranspositionTable::get(key_type key) const {
    size_t _index = index(key);
    if (table[_index].key != key) {
        return 0;
    } else {
        return table[_index].value;
    }
}

void TranspositionTable::put(key_type key, value_type value) {
    size_t _index = index(key);
    table[_index].key = key;
    table[_index].value = value;
}