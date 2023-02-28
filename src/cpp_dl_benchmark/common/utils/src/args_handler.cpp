// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#include "args_handler.hpp"

#include "logger.hpp"

#include <algorithm>
#include <exception>
#include <filesystem>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> args::split(const std::string &s, char delim) {
    std::vector<std::string> result;
    std::stringstream ss(s);
    std::string item;
    while (getline(ss, item, delim)) {
        result.push_back(item);
    }
    return result;
}

std::vector<std::string> get_files_from_dir(const std::string &path) {
    // use set to get files in order
    std::set<std::string> res;
    for (const auto &entry : std::filesystem::directory_iterator(path)) {
        res.insert(entry.path());
    }

    return std::vector<std::string>{res.begin(), res.end()};
}

std::vector<std::string> check_read_files(const std::string &path) {
    if (std::filesystem::is_regular_file(path)) {
        return {path};
    }
    else if (std::filesystem::is_directory(path)) {
        return get_files_from_dir(path);
    }
    throw std::invalid_argument("Input path " + path + " neither an existing file nor a directory");
}

std::pair<std::string, std::vector<std::string>> parse_input_files_per_input(const std::string &file_paths_string) {
    auto search_string = file_paths_string;
    std::string input_name = "";
    std::vector<std::string> file_paths;

    // parse strings like <input1>:file1,file2,file3 and get name from them
    size_t semicolon_pos = search_string.find_first_of(":");
    size_t quote_pos = search_string.find_first_of("\"");
    if (semicolon_pos != std::string::npos && quote_pos != std::string::npos && semicolon_pos > quote_pos) {
        // if : is found after opening " symbol - this means that " belongs to pathname
        semicolon_pos = std::string::npos;
    }
    if (search_string.length() > 2 && semicolon_pos == 1 && search_string[2] == '\\') {
        // Special case like C:\ denotes drive name, not an input name
        semicolon_pos = std::string::npos;
    }

    if (semicolon_pos != std::string::npos) {
        input_name = search_string.substr(0, semicolon_pos);
        search_string = search_string.substr(semicolon_pos + 1);
    }

    // parse file1,file2,file3 and get vector of paths
    size_t coma_pos = 0;
    do {
        coma_pos = search_string.find_first_of(',');
        file_paths.push_back(search_string.substr(0, coma_pos));
        if (coma_pos == std::string::npos) {
            search_string = "";
            break;
        }
        search_string = search_string.substr(coma_pos + 1);
    } while (coma_pos != std::string::npos);

    if (!search_string.empty()) {
        throw std::logic_error("Can't parse file paths for input " + input_name +
                               " in input parameter string: " + file_paths_string);
    }

    return {input_name, file_paths};
}

std::map<std::string, std::vector<std::string>> args::parse_input_files_arguments(const std::vector<std::string> &args,
                                                                                  size_t max_files) {
    std::map<std::string, std::vector<std::string>> mapped_files = {};
    auto args_it = begin(args);
    const auto is_image_arg = [](const std::string &s) {
        return s == "-i";
    };
    const auto is_arg = [](const std::string &s) {
        return s.front() == '-';
    };
    while (args_it != args.end()) {
        const auto files_start = std::find_if(args_it, end(args), is_image_arg);
        if (files_start == end(args)) {
            break;
        }
        const auto files_begin = std::next(files_start);
        const auto files_end = std::find_if(files_begin, end(args), is_arg);
        for (auto f = files_begin; f != files_end; ++f) {
            const auto &[input_name, files] = parse_input_files_per_input(*f);
            if (mapped_files.count(input_name) == 0) {
                mapped_files[input_name] = {};
            }

            for (const auto &file : files) {
                if (file == "image_info" || file == "random") {
                    mapped_files[input_name].push_back(file);
                }
                else {
                    auto checked_files = check_read_files(file);
                    std::copy(std::make_move_iterator(checked_files.begin()),
                              std::make_move_iterator(checked_files.end()),
                              std::back_inserter(mapped_files[input_name]));
                }
            }
        }
        args_it = files_end;
    }

    if (mapped_files.size() == 0) {
        logger::info << "No files were added. Random data will be used." << logger::endl;
    }
    for (auto &[input_name, files] : mapped_files) {
        if (input_name != "") {
            logger::info << "For input \"" << input_name << "\" " << files.size()
                         << " files were added:" << logger::endl;
        }
        if (files.size() > max_files) {
            logger::warn << "Too many files to process. The number of files is limited to " << max_files << ""
                         << logger::endl;
            files.resize(max_files);
        }
        for (const auto &f : files) {
            logger::info << "\t" << f << logger::endl;
        }
    }

    return mapped_files;
}

// Parse parameter string like "input0[value0],input1[value1]" or "[value]" into map
std::map<std::string, std::string> args::parse_shape_layout_string(const std::string &parameter_string) {
    std::map<std::string, std::string> return_value;
    std::string search_string = parameter_string;
    auto start_pos = search_string.find_first_of('[');
    auto input_name = search_string.substr(0, start_pos);
    while (start_pos != std::string::npos) {
        auto end_pos = search_string.find_first_of(']');
        if (end_pos == std::string::npos) {
            break;
        }
        if (start_pos) {
            input_name = search_string.substr(0, start_pos);
        }

        auto input_value = search_string.substr(start_pos + 1, end_pos - start_pos - 1);
        if (!input_name.empty()) {
            return_value[input_name] = input_value;
        }
        else {
            return_value[""] = input_value;
        }

        search_string = search_string.substr(end_pos + 1);
        if (search_string.empty() || (search_string.front() != ',' && search_string.front() != '[')) {
            break;
        }
        if (search_string.front() == ',') {
            search_string = search_string.substr(1);
        }
        start_pos = search_string.find_first_of('[');
    }

    if (!search_string.empty()) {
        throw std::invalid_argument("Can't parse input parameter string: " + parameter_string);
    }

    return return_value;
}

// Parse parameter string like "input0[255,255,255],input1[255,255,255]" or "[255,255,255]" into map
std::map<std::string, std::vector<float>> args::parse_mean_scale_string(const std::string &parameter_string) {
    std::map<std::string, std::vector<float>> return_value;
    std::string search_string = parameter_string;

    auto start_pos = search_string.find_first_of('[');
    auto input_name = search_string.substr(0, start_pos);
    while (start_pos != std::string::npos) {
        auto end_pos = search_string.find_first_of(']');
        if (end_pos == std::string::npos) {
            break;
        }
        if (start_pos) {
            input_name = search_string.substr(0, start_pos);
        }

        auto input_value = string_to_vec<float>(search_string.substr(start_pos + 1, end_pos - start_pos - 1), ',');

        if (!input_name.empty()) {
            return_value[input_name] = input_value;
        }
        else {
            return_value[""] = input_value;
        }

        search_string = search_string.substr(end_pos + 1);
        if (search_string.empty() || (search_string.front() != ',' && search_string.front() != '[')) {
            break;
        }
        if (search_string.front() == ',') {
            search_string = search_string.substr(1);
        }
        start_pos = search_string.find_first_of('[');
    }

    if (!search_string.empty()) {
        throw std::invalid_argument("Can't parse input parameter string: " + parameter_string);
    }

    return return_value;
}
