#pragma once

#include <nlohmann/json.hpp>

#include <map>
#include <string>
#include <utility>
#include <vector>

struct Record {
    std::string name;
    std::string val;
};

class Report {
public:
    Report(const std::string& report_path) : path(report_path) {}

    enum class Category : unsigned int {
        FRAMEWORK_INFO = 0,
        CMD_OPTIONS,
        CONFIGURATION_SETUP,
        EXECUTION_RESULTS,
    };

    const std::map<Category, std::string> record_categories_str = {
        {Category::FRAMEWORK_INFO, "framework_info"},
        {Category::CMD_OPTIONS, "cmd_options"},
        {Category::CONFIGURATION_SETUP, "configurations_setup"},
        {Category::EXECUTION_RESULTS, "execution_results"}};

    void save();

    void add_record(Category type, const std::vector<Record>& records);

private:
    std::map<Category, std::vector<Record>> records_per_category;
    std::string path;
};
