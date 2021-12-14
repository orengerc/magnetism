"""
Runs analysis according to specific demands
"""

from DataHandler import *
from Graph import *
from CurveFit import *
from Equations import *
from PIL import Image
from ImageHandler import *
import numpy as np
from scipy.stats import linregress
import os
import matplotlib.pyplot as plt


def calculate_magnetization(image_path):
    image = read_image(image_path, 1)

    # imdisplay(image_path, 2)
    # imdisplay(image_path, 1)
    plot_histogram(image)

    # histogram, bin_edges = np.histogram(image, bins=256, range=(0.0, 1.0))
    # plt.plot(bin_edges[0:-1], histogram)
    # plt.title("Grayscale Histogram")
    # plt.xlabel("grayscale value")
    # plt.ylabel("pixels")
    # plt.xlim(0, 1.0)
    # plt.show()

    threshold = 0.5
    mask = image < threshold
    fig, ax = plt.subplots()
    # plt.imshow(mask, cmap='gray')
    # plt.show()

    black = (np.asarray(image) < threshold).sum()
    white = (np.asarray(image) >= threshold).sum()
    white_percentage = white * 100 / (black + white)
    print(white_percentage)

    return white_percentage


def graph_results(results_dict):
    """
    Plots the magnetization curve (hysteresis loop) from given data dictionary
    :param results_dict: holds voltages and magnetization percentages
    :return: None
    """
    plot_noninjective(results_dict.keys(), results_dict.values())


if __name__ == '__main__':
    layers = ["layer1", "layer2"]
    stages = ["up", "down", "up2"]
    for layer in layers:
        results = dict()
        for stage in stages:
            directory = "data\\{0}\\{1}".format(layer, stage)
            for filename in os.listdir(directory):
                if os.path.splitext(filename)[1] != ".bmp":
                    continue
                voltage = os.path.splitext(filename)[0]
                magnetization = calculate_magnetization(os.path.join(directory, filename))
                if voltage not in results:
                    results[voltage] = [magnetization]
                else:
                    results[voltage].append(magnetization)
        graph_results(results)
