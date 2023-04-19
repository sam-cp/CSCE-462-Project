#include "Position.h"
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    TranspositionTable table;
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <move>" << std::endl;
        return -1;
    }
    try {
        Position p(argv[1]);
        if (p.has_been_won()) {
            std::cout << -21 << std::endl;
        } else {
            std::cout << p.negamax(table) << std::endl;
        }
    } catch (const std::invalid_argument& err) {
        std::cerr << err.what() << std::endl;
        return -1;
    } catch (const std::runtime_error& err) {
        std::cout << 0 << std::endl;
    }
    return 0;
}