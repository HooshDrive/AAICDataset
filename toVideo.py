import glob
import os
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageColor
from matplotlib import pyplot as plt

FRAME_RATE = 2


class_name_to_id_mapping = {
    'car': 0,
    'signal': 1,
    'signs': 2,
    'motorcycle': 3,
    'pedestrian': 4,
    'truck': 5,
    'bus': 6,
    'bicycle': 7
}

class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))
color_map = ['blue', 'coral', 'lime', 'red', 'gold', 'cyan', 'green', 'violet']

def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size

    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
    transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h

    transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
    transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
    transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
    transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]

    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0, y0), (x1, y1)), outline=color_map[int(obj_cls)])

        plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])
    return image


video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), FRAME_RATE,(1920,1280))
annotation_files = glob.glob('dataset/labels/train/*.txt')
for annotation_file in annotation_files:
    with open(annotation_file, "r") as file:
        annotation_list = file.read().split("\n")

        annotation_list = [x.split(" ") for x in annotation_list]
        annotation_list = [[float(y) for y in x] for x in annotation_list]
    # Get the corresponding image file
    image_file = annotation_file.replace("labels", "images").replace("txt", "jpg")
    assert os.path.exists(image_file)

    # Load the image
    image = Image.open(image_file)
    # Plot the Bounding Box
    if len(annotation_list) == 0:
        continue
    image = plot_bounding_box(image, annotation_list)
    video.write(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

video.release()

