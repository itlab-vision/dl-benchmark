from __future__ import print_function
import sys
import os
from argparse import ArgumentParser
import cv2
import numpy as np
import logging as log
from openvino.inference_engine import IENetwork, IEPlugin


def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", help = "Path to an .xml \
        file with a trained model.", required = True, type = str)
    parser.add_argument("-w", "--weights", help = "Path to an .bin file \
        with a trained weights.", required = True, type = str)
    parser.add_argument("-i", "--input", help = "Path to a folder with \
        images or path to an image files", required = True, type = str, nargs = "+")
    parser.add_argument("-l", "--cpu_extension", help = "MKLDNN \
        (CPU)-targeted custom layers.Absolute path to a shared library \
        with the kernels implementation", type = str, default = None)
    parser.add_argument("-pp", "--plugin_dir", help = "Path to a plugin \
        folder", type = str, default = None)
    parser.add_argument("-d", "--device", help = "Specify the target \
        device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. \
        Sample will look for a suitable plugin for device specified \
        (CPU by default)", default = "CPU", type = str)
    parser.add_argument("--labels", help = "Labels mapping file",
        default = None, type = str)
    parser.add_argument("-nt", "--number_top", help = "Number of top results",
        default = 10, type = int)
    parser.add_argument("-ni", "--number_iter", help = "Number of inference \
        iterations", default = 1, type = int)
    parser.add_argument("-pc", "--perf_counts", help = "Report performance \
        counters", action = "store_true", default = False)

    return parser

def Convert_Image(net, args, log):
	input_blob = next(iter(net.inputs))
    n, c, h, w = net.inputs[input_blob]
    images = np.ndarray(shape=(n, c, h, w))
    for i in range(n):
        image = cv2.imread(args.input[i])
        if image.shape[:-1] != (h, w):
            log.warning("Image {} is resized from {} to {}".format(args.input[i], image.shape[:-1], (h, w)))
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        images[i] = image
    
    return images

def Model_loading(log):
    args=build_argparser().parse_args()
    model_xml=args.model
    model_bin =args.weights
    plugin = IEPlugin(device=args.device, plugin_dirs=args.plugin_dir)
    if args.cpu_extension and 'CPU' in args.device:
    	plugin.add_cpu_extension(args.cpu_extension)
	#log.info("Loading network files:\n\t{}\n\t{}".format(model_xml, model_bin))
    net = IENetwork.from_ir(model=model_xml, weights=model_bin)
    if "CPU" in plugin.device:
        supported_layers = plugin.get_supported_layers(net)
        not_supported_layers = [l for l in net.layers.keys() if l not in  supported_layers]
        if len(not_supported_layers) != 0:
        	"""
        	log.error("Following layers are not supported by the plugin for \
            	specified device {}:\n {}". format(plugin.device, ',\
            	'.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in\
            	sample's command line parameters using -l "
            	"or --cpu_extension command line argument")
            """
            sys.exit(1)   
             
	#log.info("Preparing input blobs")
    net.batch_size = len(args.input)
	#log.info("Loading model to the plugin")
    exec_net = plugin.load(network=net)
    input_blob = next(iter(net.inputs))
   
    return {'net': net, 'exec_net': exec_net, 'args': args}

def Inference_sync(net,images,exec_net,args,log):
	log.info("Starting inference ({} iterations)".format(args.number_iter))
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.inputs))
    for i in range(args.number_iter):
    	res = exec_net.infer(inputs={input_blob: images})
    res=res[out_blob]
    
    return res

def Inference_out(res, args, log):
    log.info("Top {} results: ".format(args.number_top))
    if args.labels:
        with open(args.labels, 'r') as f:
            labels_map = [x.split(sep=' ', maxsplit=1)[-1].strip() for x in f]
    else:
        labels_map = None
    for i, probs in enumerate(res):
        probs = np.squeeze(probs)
        top_ind = np.argsort(probs)[-args.number_top:][::-1]
        print("Image {}\n".format(args.input[i]))
        for id in top_ind:
            det_label = labels_map[id] if labels_map else "#{}".format(id)
            print("{:.7f} label {}".format(probs[id], det_label))
        print("\n")

def main():
    log.basicConfig(format = "[ %(levelname)s ] %(message)s",
    level = log.INFO, stream = sys.stdout)
    model=Model_loading(log)
    images=Convert_Image(model['input_blob'], model['net'], model['args'], log)
    res=Inference_sync(model['net'], images, model['exec_net'], model['args'], log)
    Inference_out(res, model['args'], log)

if __name__ == '__main__':
    sys.exit(main() or 0)
