# DeepLInf: Deep Learning Inference Benchmark based on Intel® Distribution of OpenVINO™ toolkit

Deep learning benchmark based on [Intel® Distribution of OpenVINO™ toolkit][openvino-toolkit].

## Repo Structure

- `data` directory contains images for benchmarking.
  - `CelebA` is a subset of test images from
    [CelebA dataset][celeba].
  - `ImageNET` is a subset of test images from
    [ImageNET dataset][imagenet].
  - `MS_COCO` is a subset of test images from
    [MS COCO dataset][ms-coco].
  - `PASCAL_VOC` is a subset of test images from
    [PASCAL VOC 2007, 2012 datasets][pascal-voc].
  - `WIDER_FACE` is a subset of test images from
    [WIDER FACE dataset][wider-face].

- `docs` directory contains project documentation.
  - [`concept.md`](docs/concept.md) is a concept description
    (goals, tasks and requirements).
  - [`technologies.md`](docs/technologies.md) is a list
    of technologies.
  - [`architecture.md`](docs/architecture.md) is a benchmarking
    system architecture.

- `src` directory contains benchmark sources.
  - `auxiliary` contains auxiliary scripts for benchmarking
    (to get node information).
  - `benchmark` is a set of scripts to estimate inference
    performance of different models at the single local computer.
  - `configs` contains template configuration files.
  - `converter` is a set of scripts to convert models to the
    intermediate representation using Model Optimizer from
	Intel® Distribution of OpenVINO™ toolkit.
  - `inference` contains inference implementation based on
    Intel® Distribution of OpenVINO™ toolkit.
  - `remote_control` contains scripts to execute benchmark
    remotely.

- `results` directory contains validation and performance results.
  - [`validation_results.md`](docs/validation_results.md) is a table
    that confirms correctness of inference implementation based on
    Intel® Distribution of OpenVINO™ toolkit.
  - `*.csv` is a table of benchmarking results in csv-format.
  - `*.html` is a copy of the previous table in html-format.

<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[celeba]: http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html
[imagenet]: http://www.image-net.org
[ms-coco]: http://cocodataset.org
[pascal-voc]: http://host.robots.ox.ac.uk/pascal/VOC
[wider-face]: http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace
