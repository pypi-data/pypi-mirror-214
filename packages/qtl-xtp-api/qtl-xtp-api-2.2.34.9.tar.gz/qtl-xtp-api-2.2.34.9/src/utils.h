#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <codecvt>
#include <locale>
#include <limits>
#include <vector>
#include <algorithm>
#include <functional>
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>


namespace nb = nanobind;


inline bool contains(const nb::dict &d, const std::string &k) {
    for (auto i: d) {
        if (nb::cast<std::string>(i.first) == k) {
            return true;
        }
    }
    return false;
}

template <class NumberType>
inline void set_num_field(NumberType &field, const nb::dict &input, const char *field_name) {
    if (contains(input, field_name)) {
        field = nb::cast<NumberType>(input[field_name]);
    }
}

inline void set_str_field(char *field, const nb::dict &input, const char *field_name, size_t size) {
    if (contains(input, field_name)) {
        strncpy(field, nb::cast<std::string>(input[field_name]).c_str(), size);
    }
}

#endif //UTILS_H
