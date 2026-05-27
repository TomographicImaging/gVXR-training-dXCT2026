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

# import numpy as np # Who does not use Numpy?
#
# from tifffile import  imread, imwrite
# import matplotlib.pyplot as plt # Plotting
# import matplotlib.cm as cm
# plt.style.use('tableau-colorblind10')
#
# from tqdm.notebook import tqdm
#
# #  CT simulation
from gvxrPython3 import gvxr
from gvxrPython3.twins.utils import createDigitalTwin
# from gvxrPython3.gVXRDataReader import *
#
# # CT reconstruction
# from cil.plugins.astra import FBP
# from cil.io import TIFFWriter
#
# from cil.processors import TransmissionAbsorptionConverter
# from cil.utilities.display import show_geometry

# Where to save the data.
output_path = "./output_data"
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Create an OpenGL context
# gvxr.createOpenGLContext(-1, 4, 6, 41)
#
# # Create a digital twin
# # We'll make use of the "XT H 225 ST 2x" twin.
# twin = createDigitalTwin(name="XT H 225")

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
for voltage_kV in kV_set:
    for current_uA in current_uA_set:
        for exposure_s in exposure_s_set:
            for SOD_mm in SOD_mm_set:
                for sample_id in range(1, 7):
                    number_of_simulations += 1

                    start_time = datetime.datetime.now()

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

                    # Generate the output file names
                    CT_fname = os.path.join(output_path,
                        "CT_" + str(sample_id) + "_" + str(SOD_mm) + "_" + str(exposure_s) + str(current_uA) + ".tif")

                    label_fname = os.path.join(output_path,
                        "CT_" + str(sample_id) + "_" + str(SOD_mm) + "_" + str(exposure_s) + str(current_uA) + ".tif")


                    # Compute the processing time of this iteration
                    stop_time = datetime.datetime.now()
                    duration = (stop_time - start_time).total_seconds()
                    total_duration += duration
                    print()

