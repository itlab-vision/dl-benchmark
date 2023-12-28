# To run smoke test

1. Perform common installation
   [steps](../../README.md#software-installation).

1. Run tests using the following command:

   ```
   cd test/smoke_test
   python -m pytest -k=<test_name>, where test_name: test_benchmark_smoke or test_ac_smoke
   ```

   For caffe tests the following mark should be used: -m=caffe

   Pytest performs download and convert steps for test models,
   runs `inference_benchmark.py` on simple config.
