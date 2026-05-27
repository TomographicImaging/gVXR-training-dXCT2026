# -*- coding: utf-8 -*-
#
#  Copyright 2026 United Kingdom Research and Innovation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#   Authored by:    Franck Vidal (UKRI-STFC)
#   Data by:    Matthew Jones (UCL)


import numpy as np

def pad_image(img, target_image_shape):
    """
    Zero padding of an image
    :param img: the image to be padded
    :param target_image: the target image size
    :return: the padded image
    """
    extra_x_high = (target_image_shape[1] - img.shape[1]) // 2
    extra_y_high = (target_image_shape[0] - img.shape[0]) // 2

    if not (target_image_shape[1] - img.shape[1]) % 2:
        extra_x_low = extra_x_high
    else:
        extra_x_low = extra_x_high + 1

    if not (target_image_shape[0] - img.shape[0]) % 2:
        extra_y_low = extra_y_high
    else:
        extra_y_low = extra_y_high + 1

    return np.pad(img,
                  ((extra_y_low, extra_y_high), (extra_x_low, extra_x_high)),
                  mode='constant',
                  constant_values=0)

def crop_image(img):
    """
    Crop an image to remove the possible empty border around the data
    :param img: the input image
    :return: the image after border removal
    """
    if np.max(img) != np.min(img):

        # Crop on the left if needed
        min_i = 0
        stop = False
        while not stop:

            if img[:,min_i].sum() == 0:
                min_i += 1
            else:
                stop = True

        # Crop on the right if needed
        max_i = img.shape[1] - 1
        stop = False
        while not stop:

            if img[:,max_i].sum() == 0:
                max_i -= 1
            else:
                stop = True

        # Crop on the top if needed
        min_j = 0
        stop = False
        while not stop:

            if img[min_j,:].sum() == 0:
                min_j += 1
            else:
                stop = True

        # Crop on the bottom if needed
        max_j = img.shape[0] - 1
        stop = False
        while not stop:

            if img[max_j,:].sum() == 0:
                max_j -= 1
            else:
                stop = True

        cropped = img[max(0,min_j-1):max_j+2, max(0,min_i-1):max_i+2]
    else:
        cropped = np.copy(img)

    return  cropped
