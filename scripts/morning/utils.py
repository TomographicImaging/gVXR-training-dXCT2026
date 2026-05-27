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

import os.path
import numpy as np
from gvxrPython3 import gvxr
from tifffile import imread

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

def create_sample(sample_id: int,
                  mesh_path: str):
    """
    Create a sample if needed

    :param sample_id: the ID of the sample. Must be in the range [1, 6]
    :param mesh_path: the path to the meshes
    :return:
    """

    # Make sure the sample ID is in the range [1, 6]
    assert(sample_id >= 1 and sample_id <= 6)

    # Remove the sample if any
    gvxr.removePolygonMeshesFromSceneGraph()

    # Create an empty sample
    gvxr.emptyMesh("sample")

    # Load the image
    labels = imread("../../data/morning/seg" + str(sample_id) + ".tif")
    unit = "mm"

    # Create the path if needed
    if not os.path.exists(mesh_path):
        os.makedirs(mesh_path)

    # Crop the image
    labels_cropped = crop_image(labels)

    # Make sure it is a 3D image
    if len(labels_cropped.shape) == 2:
        labels = np.repeat(labels_cropped[np.newaxis, :, :], 5, axis=0)

    # Set the pixel size
    if sample_id == 1 or sample_id == 2 or sample_id == 3:
        original_pixel_size = [0.01307412, 0.01307412]
    else:
        original_pixel_size = [0.01415419, 0.01415419]

    material_composition = {

        1: {
            'name': "Al",
            'material type': 'element',
            'material': 'Al',
            'density': 2.70
        },

        2: {
            'name': "Cu-lower-density",
            'material type': 'element',
            'material': 'Cu',
            'density': 1.87
        },

        3: {
            'name': "NMC811",
            'material type': 'mixture',
            'material': 'NMC811',
            'materials': ["Li", "Ni", "Mn", "Co"],
            'weights': [0.8 * 0.1057, 0.8 * 0.8943, 0.1, 0.1],
            'density': 2.61
        },

        4: {
            'name': "Cu-higher-density",
            'material type': 'element',
            'material': 'Cu',
            'density': 8.96
        },

        5: {
            'name': "Fe70Cr19Ni10Mn1",
            'material type': 'mixture',
            'material': 'Fe70Cr19Ni10Mn1',
            'density': 8.00
        }
    }

    for label in np.unique(labels):
        if label in material_composition.keys():
            selected_material = material_composition[label]
            mesh_label = material_composition[label]['name']

            # Select the structure
            binary_image = (labels == label).astype(np.uint8)

            stl_fname = os.path.join(mesh_path, str(sample_id) + "-" + mesh_label + ".stl")

            # Load the existing STL file
            if os.path.exists(stl_fname):
                gvxr.loadMeshFile(mesh_label, stl_fname, unit, False, "sample")
            # Apply the Marching cubes
            else:
                print(f"Create {stl_fname}")

                # Let' make it a cube
                image_size = np.average([
                    labels.shape[2] * original_pixel_size[0],
                    labels.shape[1] * original_pixel_size[0]
                ])

                voxel_size = [
                    original_pixel_size[0],
                    original_pixel_size[1],
                    image_size / labels.shape[0]
                ]

                # Create the mesh
                gvxr.makeIsoSurface(mesh_label,
                                    binary_image,
                                    1,
                                    0, 0, 0,
                                    *voxel_size,
                                    unit,
                                    "sample"
                )

                # Save the mesh as an STL file
                gvxr.saveSTLfile(mesh_label, stl_fname)

            # Set the material
            if selected_material['material type'].upper() == 'ELEMENT':
                print("\tUse element", material_composition[label]["material"])
                gvxr.setElement(mesh_label, material_composition[label]["material"])

                if "density" in selected_material:
                    gvxr.setDensity(mesh_label, selected_material["density"], "g/cm3")

            elif selected_material['material type'].upper() == 'COMPOUND':
                gvxr.setCompound(mesh_label, material_composition[label]["material"])
                gvxr.setDensity(mesh_label, selected_material["density"], "g/cm3")

            elif selected_material['material type'].upper() == 'MIXTURE':
                if "materials" in selected_material and "weights" in selected_material:
                    gvxr.setMixture(mesh_label, selected_material["materials"], selected_material["weights"])
                else:
                    gvxr.setMixture(mesh_label, material_composition[label]["material"])

                gvxr.setDensity(mesh_label, selected_material["density"], "g/cm3")

            else:
                raise IOError("Invalid material type")

            # Add the material
            gvxr.addPolygonMeshAsInnerSurface(mesh_label)

    return labels_cropped, original_pixel_size, unit