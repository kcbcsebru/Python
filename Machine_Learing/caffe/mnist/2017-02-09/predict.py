import sys
import argparse
import cv2
import caffe

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--png')
    args = parse.parse_args()
    model = './classificat_net.prototxt'
    weights = './lenet_iter_10000.caffemodel'
    net = caffe.Net(model, weights, caffe.TEST)
    img = cv2.imread(args.png, cv2.IMREAD_GRAYSCALE)
    net.blobs['data'].data[...] = img
    out = net.forward()
    prob = out['prob'][0]
    for index, item in enumerate(prob):
        if item == 1:
            print index