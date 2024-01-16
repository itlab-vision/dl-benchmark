# To run smoke test

1. Perform common installation
   [steps](../../README.md#software-installation).

1. Run benchmark smoke tests using the following command:

   ```bash
   cd test/smoke_test/benchmark_smoke
   python -m pytest -k=test_benchmark_smoke
   ```

   For caffe tests the following mark should be used: -m=caffe

   For cpp tests the following arguments could be used: --cpp_benchmarks_dir and --openvino_cpp_benchmark_dir

   Pytest performs download and convert steps for test models,
   runs `inference_benchmark.py` on simple config.

1. Run accuracy tests using the following command:

   ```bash
   cd test/smoke_test/ac_smoke
   python -m pytest -k=test_ac_smoke
   ```

   Pytest performs download and convert steps for test models,
   runs `accuracy_checker.py` on simple config.
