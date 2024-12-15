# Demo

## Description

### Basic information

The script allows you to run the full cycle of the DLI
Benchmark system, demonstrating the operability of the entire
system, from system deployment to conversion of tables with
results. At the moment, a version for Linux systems with
the deployment of the DLI Benchmark using Docker containers
has been implemented.

### Algorithm

The application creates two directories on the local machine,
`server` and `client`, which represent the environments
for the FTP server and client, respectively. The output
of the application is CSV, HTML, and XLSX tables with
the results of the experiments measuring the performance
and assessing the quality of the deep `SampleNet` model,
which is a test model for the [AccuracyChecker][accuracy-checker]
tool in [Intel® Distribution of OpenVINO™ Toolkit][openvino-toolkit].

### Application results

The output of the application is a set of CSV, HTML and XLSX
tables with the results of the experiments on measuring performance
and assessing the quality of the test model.

## Usage

```bash
chmod a+x linux.sh
./linux.sh -l <login> -p <password> -d <benchmark_datasets>
```

Command line arguments:

- `-l` corresponds to the login to connect to the current machine.
- `-p` corresponds to the password to connect to the current machine.
- `-d` corresponds to the GitHub repository that contains
  the benchmarking datasets. It is required that the repository
  contains the directory `Datasets/ImageNET/`, in which at least
  one image is stored. It is necessary for system deployment. 

Example:

```bash
chmod a+x linux.sh
./linux.sh -l admin -p admin -d "https://github.com/account/repo.git"
```


<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[accuracy-checker]: https://docs.openvino.ai/latest/omz_tools_accuracy_checker.html
