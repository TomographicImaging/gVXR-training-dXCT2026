import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tifffile import imread, imwrite

from skimage.transform import rotate, resize
from skimage.util import random_noise
from skimage.exposure import rescale_intensity

def normalise_for_display(image, lower=1, upper=99):
    """Normalise an image using percentile clipping for display."""
    image = image.astype(np.float32)
    vmin, vmax = np.percentile(image, [lower, upper])

    if vmax <= vmin:
        return np.zeros_like(image, dtype=np.float32)

    image = np.clip(image, vmin, vmax)
    image = (image - vmin) / (vmax - vmin)

    return image


def plot_overlay(image, mask, title=None, alpha=0.35):
    """Plot a CT image with a red segmentation mask overlay."""
    image_disp = normalise_for_display(image)
    mask_binary = mask > 0

    # Create red RGBA overlay
    overlay = np.zeros((*mask.shape, 4), dtype=np.float32)
    overlay[..., 0] = 1.0          # red channel
    overlay[..., 3] = mask_binary * alpha  # alpha channel

    plt.figure(figsize=(6, 6))
    plt.imshow(image_disp, cmap="gray")
    plt.imshow(overlay)
    plt.axis("off")

    if title is not None:
        plt.title(title)

    plt.show()


def make_red_overlay(mask, alpha=0.35):
    """Create a red RGBA overlay from a binary mask."""
    mask_binary = mask > 0

    overlay = np.zeros((*mask.shape, 4), dtype=np.float32)
    overlay[..., 0] = 1.0
    overlay[..., 3] = mask_binary * alpha

    return overlay


def plot_pair_overlay(row, title=None):
    """Plot a CT image with its binary mask overlay."""
    image = imread(row["ct_path"]).astype(np.float32)
    mask = imread(row["label_path"]).astype(np.uint8)

    plt.figure(figsize=(6, 6))
    plt.imshow(normalise_for_display(image), cmap="gray")
    plt.imshow(make_red_overlay(mask))
    plt.axis("off")

    if title is not None:
        plt.title(title)

    plt.show()
