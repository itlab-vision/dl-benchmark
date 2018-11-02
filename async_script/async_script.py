#!/usr/bin/env python


import sys
import os
import argparse
import cv2
import numpy as np
import logging as log
import time
from openvino.inference_engine import IENetwork, IEPlugin

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help = "Path to an .xml file with a trained model.", required=True, type=str)
    parser.add_argument("-i", "--image", help = "Path to a folder with images or path to an image files", required=True,
                        type=str, nargs="+")
    parser.add_argument("-l", "--cpu_extension", 
                        help="MKLDNN (CPU)-targeted custom layers.Absolute path to a shared library with the kernels "
                            "impl.", type=str, default=None)
    parser.add_argument("-pp", "--plugin_dir", help="Path to a plugin folder", type=str, default=None)
    parser.add_argument("-d", "--device",
                        help="Specify the target device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device specified (CPU by default)", default="CPU",
                        type=str)
    parser.add_argument("--labels", help="Labels mapping file", default=None, type=str)
    parser.add_argument("-nt", "--number_top", help="Number of top results", default=10, type=int)
    parser.add_argument("-ni", "--number_iter", help="Number of inference iterations", default=1, type=int)
    parser.add_argument("-pc", "--perf_counts", help="Report performance counters", action="store_true", default=False)

    return parser

def main():
