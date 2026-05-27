#!/usr/bin/env python3
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

import os # Create the output directory if necessary
import datetime, math # To estimate durations

from tifffile import  imread, imwrite # Read/Write the image of labels

from skimage.transform import resize # Resize the image of labels
from utils import pad_image, crop_image # Process the image of labels
from utils import create_sample # Generate the sample if needed

#  CT simulation
from gvxrPython3 import gvxr
from gvxrPython3.twins.utils import createDigitalTwin
from gvxrPython3.gVXRDataReader import *

# CT reconstruction
from cil.plugins.astra import FBP
from cil.io import TIFFWriter
from cil.processors import TransmissionAbsorptionConverter


# Where to save the data.
output_path = "./output_data"
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Create an OpenGL context
gvxr.createOpenGLContext(-1, 4, 6, 41)
gvxr.enablePoissonNoise()

# Create a digital twin
# We'll make use of the "XT H 225 ST 2x" twin.
twin = createDigitalTwin(name="XT H 225")

# Alter the twin specification to only generate 3 rows of simulated data
for i, resolution in enumerate(twin.specification.detector.resolutions):
    twin.specification.detector.resolutions[i] = [resolution[0], 3]

# SOD will be 150 mm +/- 20%
default_SOD_mm = 150
SOD_mm_set = np.linspace(default_SOD_mm * (1-0.2),
                         default_SOD_mm * (1+0.2),
                         5,
                         endpoint=True)

# Current will be 160 uA +/- 30%
default_current_uA = 160
current_uA_set = np.linspace(default_current_uA * (1-0.3),
                             default_current_uA * (1+0.3),
                             5,
                             endpoint=True)

exposure_s_set = [0.5, 1.0, 1.42, 2.0]

# Voltage will be in the range [180, 225]
kV_set = np.linspace(180, 225, 6, endpoint=True)

# Total number of simulations
number_of_samples = 6
total_number_simulations = number_of_samples * len(kV_set) * len(current_uA_set) * len(exposure_s_set) * len(SOD_mm_set)

# Iterate through all the settings
total_duration = 0
number_of_simulations = 0

# Go through all the voltages
for voltage_kV in kV_set:

    # Set the voltage
    twin.beam.kV = voltage_kV

    # Go through all the currents
    for current_uA in current_uA_set:

        # Set the current
        twin.beam.uA = current_uA

        # Go through all the exposures
        for exposure_s in exposure_s_set:
            # Set the exposure
            twin.detector.exposure = exposure_s

            # Apply the settings
            twin.apply()

            # Add the filtration
            gvxr.clearFiltration()
            gvxr.addFilter("Cu", 1.0, "mm")

            # Go through all the samples
            for sample_id in range(1, 7):

                # Generate the sample if needed
                create_sample(sample_id)

                # Go through all the SODs
                for SOD_mm in SOD_mm_set:

                    # Increment the counter
                    number_of_simulations += 1

                    # Start the timer
                    start_time = datetime.datetime.now()

                    # Print the estimated remaining time
                    print("********************************************************************************")
                    print(f"Processing simulation {number_of_simulations}/{total_number_simulations}")

                    # Estimate how much time is left
                    if number_of_simulations > 1:
                        duration_s_per_run = total_duration / (number_of_simulations - 1)
                        run_left = total_number_simulations - (number_of_simulations - 1)
                        total_duration_s_left = duration_s_per_run * run_left

                        hours_left = math.floor(total_duration_s_left / 3600)
                        minutes_left = max(0, round((total_duration_s_left - hours_left * 3600) / 60))

                        if minutes_left == 60:
                            hours_left += 1
                            minutes_left = 0

                        print(f"Total duration left: {hours_left} hours, {minutes_left} minutes")
                    print("********************************************************************************")

                    # Apply the SOD
                    gvxr.applySOD("sample", SOD_mm, "cm")

                    # Select the number of projections, make it at least 1000.
                    number_of_projections = max(1000, gvxr.getOptimalNumberOfProjectionsCT())

                    # Perform the actual simulations
                    rotation_centre_in_mm = gvxr.getNodeAndChildrenBoundingBoxCentre("sample", "mm")
                    rotation_axis = gvxr.getDetectorUpVector()

                    gvxr.computeCTAcquisition(
                        os.path.join(output_path, "projections"),  # The path where the X-ray projections will be saved
                        "",  # The path where the screenshots will be saved
                        number_of_projections,  # The total number of projections to simulate
                        0,  # The rotation angle corresponding to the first projection
                        False,  # A boolean flag to include or exclude the last angle
                        360,  # The rotation angle corresponding to the last projection
                        50,  # The number of white images used to perform the flat-field correction
                        *rotation_centre_in_mm,  # The location of the rotation centre
                        unit,  # The corresponding unit of length
                        *rotation_axis  # The rotation axis
                    )

                    # Read the simulated data with CIL
                    reader = gVXRDataReader(gvxr.getProjectionOutputPathCT(),
                                            gvxr.getAngleSetCT(),
                                            rotation_axis,
                                            rotation_centre_in_mm)
                    data = reader.read()

                    # Apply the minus log transformation
                    # (use use white_level=1.0 as the flat-field correction is already applied)
                    data_corr = TransmissionAbsorptionConverter(white_level=1.0)(data)

                    # We will only reconstruct one slice
                    image_geometry = data_corr.geometry.get_ImageGeometry()
                    image_geometry.voxel_num_z = 1

                    # Perform the reconstruction with CIL using the Astra backend
                    data_corr.reorder(order='astra')
                    fbp = FBP(image_geometry, data_corr.geometry)
                    fbp.set_input(data_corr)
                    reconstruction = fbp.get_output()

                    # Generate the output file names
                    CT_fname = os.path.join(output_path,
                        "CT_" + str(sample_id) + "_" + str(SOD_mm) + "_" + str(exposure_s) + str(current_uA))

                    label_fname = os.path.join(output_path,
                        "labels_" + str(sample_id) + "_" + str(SOD_mm) + "_" + str(exposure_s) + str(current_uA))

                    # Save the reconstructed CT images
                    writer = TIFFWriter(data=reconstruction,
                                        file_name=CT_fname,
                                        compression="uint16")

                    # Generate the labels
                    # 1. Resize the cropped image of labels without interpolation so that it is using the same pixel size as the CT
                    # reconstruction
                    voxel_size = [image_geometry.voxel_size_x, image_geometry.voxel_size_y]
                    scaling_factors = [voxel_size[0] / original_pixel_size[0], voxel_size[1] / original_pixel_size[1]]

                    labelled_resized = resize(
                        labels_cropped,
                        (round(labels_cropped.shape[0] // scaling_factors[0]), round(labels_cropped.shape[1] //
                                                                                     scaling_factors[1])),
                        anti_aliasing=False
                    )

                    # 2. Pad it with 0s so that it is the same number of pixels as the CT reconstruction
                    labels_padded = pad_image(labelled_resized, reconstruction.array.shape)

                    # 3. Save the image
                    imwrite(label_fname + ".tif", labels_padded)

                    # Compute the processing time of this iteration
                    stop_time = datetime.datetime.now()
                    duration = (stop_time - start_time).total_seconds()
                    total_duration += duration
                    print()

