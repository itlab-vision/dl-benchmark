#pragma once

#include <executorch/extension/module/module.h>
#include <executorch/extension/tensor/tensor.h>
#include <executorch/extension/memory_allocator/malloc_memory_allocator.h>
#include <executorch/extension/threadpool/cpuinfo_utils.h>
#include <executorch/extension/threadpool/threadpool.h>
#include <executorch/extension/data_loader/file_data_loader.h>


using executorch::aten::Tensor;
using executorch::aten::TensorImpl;
using executorch::extension::FileDataLoader;
using executorch::extension::MallocMemoryAllocator;
using executorch::runtime::Error;
using executorch::runtime::EValue;
using executorch::runtime::MemoryAllocator;
using executorch::runtime::HierarchicalAllocator;
using executorch::runtime::MemoryManager;
using executorch::runtime::Method;
using executorch::runtime::MethodMeta;
using executorch::runtime::Program;
using executorch::runtime::Result;
using executorch::runtime::Span;


static uint8_t method_allocator_pool[4 * 1024U * 1024U];


class InferenceAPI {
public:
    InferenceAPI() {}

    virtual void read_model(const std::string& model_file) = 0;

    virtual void set_input(const std::vector<std::vector<executorch::runtime::EValue>>& tens, const int input_idx) = 0;

    virtual void inference() = 0;

    virtual ~InferenceAPI() {}

    virtual const Tensor dump_output(const std::vector<std::vector<executorch::runtime::EValue>>& tens) = 0;

};


class LowLevelInferenceAPI : public InferenceAPI {
public:

    LowLevelInferenceAPI() {}
    virtual ~LowLevelInferenceAPI() {}

    void read_model(const std::string& model_file) override {
        loader = std::make_unique<Result<FileDataLoader>>(FileDataLoader::from(model_file.c_str()));
        program = std::make_unique<Result<Program>>(Program::load(&loader->get()));
        const char* method_name = "forward";
        method_meta = std::make_unique<Result<MethodMeta>>(program->get().method_meta(method_name));
        size_t num_memory_planned_buffers1 = method_meta->get().num_memory_planned_buffers();

        for (size_t id = 0; id < num_memory_planned_buffers1; ++id) {
            size_t buffer_size =
                static_cast<size_t>(method_meta->get().memory_planned_buffer_size(id).get());
            planned_buffers.push_back(std::make_unique<uint8_t[]>(buffer_size));
            planned_arenas.push_back({planned_buffers.back().get(), buffer_size});
        }
        planned_memory = std::make_unique<HierarchicalAllocator>(HierarchicalAllocator({planned_arenas.data(), planned_arenas.size()}));
        method_allocator = std::make_unique<MemoryAllocator>(MemoryAllocator{MemoryAllocator(sizeof(method_allocator_pool), method_allocator_pool)});
        memory_manager = std::make_unique<MemoryManager>(MemoryManager(method_allocator.get(), planned_memory.get()));
        method = std::make_unique<Result<Method>>(program->get().load_method("forward", memory_manager.get()));
    }

    void set_input(const std::vector<std::vector<executorch::runtime::EValue>>& tens, const int input_idx) override {
        Error set_input_error = method.get()->get().set_input(tens[0][input_idx], 0);
        if (set_input_error != Error::Ok) {
            throw std::runtime_error("Error when setting input tensor.");
        }
    }

    void inference() override {
        Error execute_error = method.get()->get().execute();
        if (execute_error != Error::Ok) {
            throw std::runtime_error("Inference error.");
        }
    }

    const Tensor dump_output(const std::vector<std::vector<executorch::runtime::EValue>>& tens) override {
        Error set_input_error = method.get()->get().set_input(tens[0][0], 0);
        if (set_input_error != Error::Ok) {
            throw std::runtime_error("Error when setting input tensor.");
        }
        method.get()->get().execute();
        const auto result = method.get()->get().get_output(0);
        return result.toTensor();
    }

private:
    std::unique_ptr<Result<FileDataLoader>> loader;
    std::unique_ptr<Result<Program>> program;
    std::unique_ptr<Result<MethodMeta>> method_meta;
    std::unique_ptr<Result<Method>> method;
    std::unique_ptr<MemoryAllocator> method_allocator;
    std::unique_ptr<HierarchicalAllocator> planned_memory;
    std::unique_ptr<MemoryManager> memory_manager;
    std::vector<std::unique_ptr<uint8_t[]>> planned_buffers;
    std::vector<Span<uint8_t>> planned_arenas;
};


class HighLevelInferenceAPI : public InferenceAPI {
public:

    HighLevelInferenceAPI() {}
    virtual ~HighLevelInferenceAPI() {}

    void read_model(const std::string& model_file) override {
        module = std::make_unique<executorch::extension::Module>(model_file);
    }

    void set_input(const std::vector<std::vector<executorch::runtime::EValue>>& tens, const int input_idx) override {
        module->set_input("forward", tens[0][input_idx], 0);
    }

    void inference() override {
        module->forward();
    }

    const Tensor dump_output(const std::vector<std::vector<executorch::runtime::EValue>>& tens) override {
        module->set_input("forward", tens[0][0], 0);
        const auto result = module->forward();
        return result->at(0).toTensor();
    }

private:
    std::unique_ptr<executorch::extension::Module> module;
};