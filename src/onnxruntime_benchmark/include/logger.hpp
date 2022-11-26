#pragma once

#include <iostream>
#include <memory>
#include <string>

namespace logger {

class EndLine {};
static constexpr EndLine endl;

class LogStream {
    std::string prefix;
    std::ostream *lstream;
    bool end_line;

public:
    LogStream(const std::string &prefix, std::ostream &lstream) : prefix(prefix), lstream(&lstream), end_line(true) {}

    template <class T>
    LogStream &operator<<(const T &arg) {
        if (end_line) {
            (*lstream) << "[ " << prefix << " ] ";
            end_line = false;
        }
        (*lstream) << arg;
        return *this;
    }

    LogStream &operator<<(const EndLine &) {
        end_line = true;
        (*lstream) << std::endl;
        return *this;
    }
};

static LogStream info("INFO", std::cout);
static LogStream debug("DEBUG", std::cout);
static LogStream warn("WARNING", std::cout);
static LogStream err("ERROR", std::cerr);

} // namespace logger
