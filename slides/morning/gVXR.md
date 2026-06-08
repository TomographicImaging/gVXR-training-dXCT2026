---
title: Introduction to X-ray attenuation and its implementation in gVXR
author: Prof Franck P. Vidal
subtitle: Workshop, dXCT 2026
date: 2026-06-16
keywords: gVXR, gVirtualXray, dXCT, X-ray simulation
institute: 
fontsize: 11pt
lang: en-gb
---

# Real vs simulated?

![](img/real-vs-simulated1.png){ width=70% }

# Real vs simulated?

![](img/real-vs-simulated2.png){ width=70% }

# Aims of this session

- Become familiar with the Beer-Lambert law to compute the attenuation of X-rays by matter;
- Describe how the Beer-Lambert law is implemented in gVirtualXray;  
- Learn how to generate realistic, XCT projection data using the [**gVXR** package](https://gvirtualxray.sourceforge.io/), 
  - with a focus on building simulation setups that mirror practical XCT scenarios and 
  - producing synthetic datasets suitable for downstream analysis and model training.

# Contents

1. 
2. 
3. 
4. 

<!--
:::::::::::::: {.columns}
::: {.column width="40%"}
contents...
:::
::: {.column width="60%"}
contents...
:::
::::::::::::::
-->

# What is gVirtualXray (gVXR)?

::::: columns
::: column

- API (application programming interface)
- relying on the **Beer--Lambert law**
- to simulate X-ray images in realtime on a GPU (graphics processor
  unit)
- using triangular meshes.
:::

::: column

![image](img/wireframe_model2.png)
:::
:::::

> It is an alternative to Monte Carlo methods when scattering[^1] can be ignored or speed is required.

[^1]: It may be added in the future

# Implementation

- R&D started in the early 2000s, VXI[^2] by Nicolas Freud (INSA-Lyon),
  and
- Its port on GPU when they became programmable (Bangor University,
  2007);
- Not a ray tracer, but a rasterizer!
- Implemented in ![C++](img/cpp-logo.png){ height=30px } using ![OpenGL](img/OpenGL-logo.png){ height=30px }
- Wrapper for ![Python](img/python-logo-generic.svg){ height=30px }, 
  ![image](img/Rlogo.svg){ height=30px },
  ![image](img/ruby-crop){ height=30px },
  ![image](img/Tcl-powered.svg){ height=30px },
  ![image](img/Logo_C_sharp.svg){ height=30px }, 
  ![Java](img/java-ar21.svg){ height=30px }, and ![GNU Octave](img/gnu-octave-logo-lnx.png){ height=30px }.

[^2]: [@FREUD2006175].

# Cross-platform

::::: columns
::: column
- Operating systems: ![MS Windows, MacOs, and GNU/Linux.](img/201-2015528_windows-mac-linux-logo.jpg){ height=30px }
- CPUs:
  - x86_64 (i.e. Intel & AMD)
  - ARM
- GPUs:
  - NVIDIA
  - AMD
  - Intel
  - Mesa software rendering
:::

::: column
- Computers:
  - Raspberry Pi 5
  - NVIDIA Jetson
  - Laptop
  - Desktop PC
  - Supercomputers
- Cloud infrastructures:
  - Google Colab
  - Code Ocean (used for reproducible research)
- Containerisation with ![Docker.](img/Docker_logo.svg){ height=30px }
:::
:::::
::::::

# Beer-Lambert law (monochromatic)

$$pixel(x,y) = N_{in} \times E  \times \exp\left({-\sum_i \mu_i(E,\rho,Z) \; L_p(i, x, y})\right)$$

- $N_{in}$ is the number of photons of Energy $E$ emitted by the source
- $\mu_i(E)$ is the linear attenuation coefficient at Energy $E$ of the
  i-th material;
- $L_p(i, x, y)$ is the path length of the ray from the X-ray source to
  pixel $(x,y)$ crossing the $i$-th material.

# Final model

$$
pixel(x,y) = gain \times {\sum_u\sum_v \mathrm{PSF}(u,v)} \times \sum_k\sum_j {\mathbf{R}(E_j)} \times \\{\mathrm{Poisson}}\left(N_{in}(E_j) \; \exp\left({-\sum_i \mu_i(E_j,\rho,Z) \; L_p(i, k, x{-u}, y{-v})}\right)\right)
$$

- $gain$ is the detector gain
- $PSF$ is the impulse response of the detector, a low-pass convolution
  filter;
- Focal spot ($\sum_k$)
- Polychromatism ($\sum_j$)
- $\mathbf{R}(E_j)$ is the energy response of the detector, a lookup
  table to mimic scintillators.

# What can we scan?

- Surface mesh from files (all common formats are supported, inc. STL)

*STL file from 3D laser scanning*

![Welsh dragon](img/models/welsh-dragon.png){ width=30% }

# What can we scan?

- Surface mesh from files (all common formats are supported, inc. STL)
- Multi-part models using multiple different materials

*Lungman anthropomorphic chest phantom (Kyoto Kagaku, Tokyo, Japan)*

![Paediatric phantom from the ERROR project.](img/models/pediatric_model.png){ width=30% }

# What can we scan?

- Surface mesh from files (all common formats are supported, inc. STL)
- Multi-part models using multiple different materials
- Volume meshes (INP files from Abaqus, EXPERIMENTAL)

*Tooth model*

![Volumetric mesh made of tetrahedrons.](img/models/tetrahedon.png){ width=30% }

# What can we scan?

- Surface mesh from files (all common formats are supported, inc. STL)
- Multi-part models using multiple different materials
- Volume meshes (INP files from Abaqus, EXPERIMENTAL)
- Implicit modelling (organic-looking $n$-dimensional isosurfaces)

| Far from each other                                  | Getting closer                                        | Close from each other                                 | Positive + negative density fields                   |
|------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|------------------------------------------------------|
| ![](img/models/implicit_modelling1.png){ width=80% } | ![](img/models/implicit_modelling2.png){ width=80% } | ![](img/models/implicit_modelling3.png){ width=80% } | ![](img/models/implicit_modelling4.png){ width=80% } |

# What can we scan?

- Surface mesh from files (all common formats are supported, inc. STL)
- Multi-part models using multiple different materials
- Volume meshes (INP files from Abaqus, EXPERIMENTAL)
- Implicit modelling (organic-looking $n$-dimensional isosurfaces)
- Customisable built-in phantoms

| Welsh dragon | Step wedge | Foam                                  | Geometric shapes                         | Lungman                                            |
|--------------|------------|---------------------------------------|------------------------------------------|----------------------------------------------------|
| ![](img/models/welsh-dragon.png){ height=200px } | ![](img/models/step-wedge.png){ height=200px } | ![](img/models/foam.png){ height=200px } | ![](img/models/cyl_sph.png){ height=200px } | ![](img/models/lungman_wireframe.png){ height=200px } |

# Other built-in functionalities

:::::: columns
::: column
0.45

- Impulse response of detectors

- [Parallel beams]{.alert}, [point sources]{.alert}, [focal
  spots]{.alert}

- [Mono/Poly chromatic spectra]{.alert}

  - including kV and beam filtration

- [Photon noise]{.alert} (calibrated on Geant4/Gate)

- [Scintillation]{.alert}

- [Flexible material composition]{.alert}

- Interactive 3D visualization\

Text in [red]{.alert} marks components validated against Monte Carlo
simulations
:::

:::: column
0.55

::: examples
:::
::::
::::::
:::::::

:::: frame
Setting up the simulation

- Write the code to describe the previous parameters in pure
  [](https://github.com/TomographicImaging/gVXR-SPIE2024/blob/main/code/dragon-without-JSON.ipynb),
  ![image](cpp-logo){height="1.25\\baselineskip"},
  ![image](Rlogo){height="1.25\\baselineskip"},
  ![image](ruby-crop){height="1.25\\baselineskip"},
  ![image](Tcl-powered){height="1.25\\baselineskip"} ,
  ![image](Logo_C_sharp){height="1.25\\baselineskip"} , , and

- Or use a human friendly [
  file](https://github.com/TomographicImaging/gVXR-SPIE2024/blob/main/results/dragon.json)

- To simplify the [
  code](https://github.com/TomographicImaging/gVXR-SPIE2024/blob/main/code/dragon-with-JSON.ipynb).

::: block
Remark [Easy installation for using
with](https://pypi.org/project/gvxr/)

``` {numbers="none"}
pip install gvxr
```
:::
::::

::::: frame
fileVisualisation window

:::: center
::: minipage
``` {.JSON language="JSON" startFrom="1"}
{
    "Window size": [640, 480],
```
:::
::::
:::::

::::: frame
fileX-ray source

:::: center
::: minipage
``` {.JSON language="JSON" startFrom="3"}
"Source": {
        "Position": [0.0, -1500.0, 0.0, "mm"],
        "Shape": "POINT",
        "Beam": {
            "Peak kilo voltage": 160.0,
            "Tube angle": 12.0,
            "mAs": 0.5,
            "filter": [
                ["Cu", 1.0, "mm"]
            ]
        }
    },
```
:::
::::
:::::

::::: frame
fileX-ray detector

:::: center
::: minipage
``` {.JSON language="JSON" startFrom="15"}
"Detector": {
        "Position": [0.0, 400.0, 0.0, "mm"],
        "UpVector": [0, 0, -1],
        "RightVector": [-1.0, 0.0, 0.0],
        "NumberOfPixels": [512, 512],
        "Size": [256.0, 256.0, "mm"],
        "LSF": [0.0002, 0.0060, 0.0606, 0.2417, 
            0.3829, 0.2417, 0.0606, 0.0060, 0.0002],
        "Scintillator": {
            "Material": "CsI",
            "Thickness": 500.0,
            "Unit": "um"
        }
    },    
```
:::
::::
:::::

::::: frame
fileSample

:::: center
::: minipage
``` {.JSON language="JSON" startFrom="29"}
"Samples": [
        {
            "Label": "Dragon",
            "Path": "welsh-dragon-small.stl",
            "Unit": "mm",
            "Material": ["Mixture", "Al6Ti90V4"],
            "Density": 4.43,
            "Type": "inner"
        }
    ],
```
:::
::::
:::::

::::: frame
fileCT scan acquisition

:::: center
::: minipage
``` {.JSON language="JSON" startFrom="39"}
"Scan": {
        "OutFolder": "projections",
        "GifPath": "screenshots",
        "NumberOfProjections": 200,
        "StartAngle": 0,
        "FinalAngle": 360,
        "IncludeLastAngle": true,
        "Flat-Field Correction": true,
        "NumberOfWhiteImages": 60,
        "CentreOfRotation": [0, 0, 0, "mm"],
        "RotationAxis": [0, 0, -1]
    }
}
```
:::
::::
:::::

::::: frame
    CT simulation

:::: center
::: minipage
``` {.python language="Python" startFrom="1"}
from gvxrPython3 import json2gvxr # Simulate X-ray images

json2gvxr.initGVXR("filename.json", renderer="OPENGL")
json2gvxr.initDetector()
json2gvxr.initSourceGeometry()
json2gvxr.initSpectrum()
json2gvxr.initSamples(verbose=0)
json2gvxr.initScan()
json2gvxr.doCTScan()
```
:::
::::
:::::

::::: frame
    CT reconstruction

:::: center
::: minipage
``` {.python language="Python" startFrom="1"}
from gvxrPython3.JSON2gVXRDataReader import *
from cil.processors import TransmissionAbsorptionConverter
from cil.framework import AcquisitionData
from cil.recon import FDK
from cil.io import TIFFWriter

reader = JSON2gVXRDataReader(file_name="filename.json")
data_absorption = TransmissionAbsorptionConverter(
    white_level=data_original.max())(data_original)
acquisition_data = AcquisitionData(data_absorption,
    geometry=data_absorption.geometry)
acquisition_data.reorder(order="tigre")
ig = acquisition_data.geometry.get_ImageGeometry()
fdk =  FDK(acquisition_data, ig)
recon = fdk.run()
TIFFWriter(data=recon, file_name="slices", "out")).write()
```
:::
::::
:::::

::::::: frame
#     Modern Web-based GUI

:::::: columns
::: column
0.6 ![image](webct){height="80%" width="\\textwidth"}
:::

:::: column
0.4

::: block
Remarks See video on YouTube\
![image](WebCTYouTube){width="2.cm"}\
Download the new pre-release\
![image](WebCTdownload){width="2.cm"}\
Or visit <https://webct.io/>
:::
::::
::::::
:::::::





# 1. Simulate accurate X-ray images
![img_1.png](img_1.png)
# 1. What is a point operator?
![img_2.png](img_2.png)
- Simplest image filtering technique in regard to complexity and computing time.
- They require no data from other pixels to process an input pixel into an output pixel.
- Simply calculate a single-parameter function with the input pixel as the parameter.

# 1. What is a point operator?

- Modify each pixel independently from one another
- The simplest case: multiplication and addition:

$$g(x,y) = gain \times f(x,y) + bias$$

with $g$ the output image, $f$ the input image, and $(x,y)$ the pixel coordinate ($x$-th column, and $y$-th-row).

- Which one ($gain$ or $bias$) will change the image brightness, and
- which will change image contrast?

# Note to students:

- Most algorithms are developed for greyscale images;
- Simpler format;
- Faster processing; but
- You can often extend the algorithms to colour images (e.g. repeat the operations for each colour channel).

# 2. Improving the brightness and contrast

# 2. Improving the brightness and contrast

- Known as "Contrast enhancement"

![Image with a very poor contrast](img/Chapter 5 - Introduction to image processing41.png)

# Intensity histogram

- Is a representation of the distribution of pixel values in an image
- Plots the number of pixels for each value
  - X-axis: pixel intensity
  - Y-axis: pixel count for each pixel intensity

![Corresponding histogram](img/Chapter 5 - Introduction to image processing42.png)


# Exercise

- Draw the intensity histogram of the following image:

$$\left( \begin{array}{ccc}
0 & 5 & 0 \\
0 & 5 & 0 \\
1 & 3 & 0 \end{array} \right)$$

# Exercise

- Draw the intensity histogram of the following image:

$$\left( \begin{array}{ccc}
0 & 5 & 0 \\
0 & 5 & 0 \\
1 & 3 & 0 \end{array} \right)$$

- For each pixel value of the dynamic range, find how many times it has been used.

| Pixel intensity | Count |
|-----------------|-------|
| 0               |       |
| 1               |       |
| 2               |       |
| 3               |       |
| 4               |       |
| 5               |       |

# Exercise

- For each pixel value of the dynamic range, find how many times it has been used.

| Pixel intensity | Count |
|-----------------|-------|
| 0               | 5     |
| 1               | 1     |
| 2               | 0     |
| 3               | 1     |
| 4               | 0     |
| 5               | 2     |

- Plot the data using a bar chart.

![Corresponding histogram](img/histogram.png)

- Remember to **ALWAYS** add a label to the graph axes.

# Exercise

- Sometimes, the frequency in % is provided instead of the count.

| Pixel intensity | Count | Frequency |
|-----------------|-------|-----------|
| 0               | 5     | $100 \times 5 / 9$% |
| 1               | 1     | $100 \times 1 / 9$% |
| 2               | 0     | $100 \times 0 / 9$% |
| 3               | 1     | $100 \times 1 / 9$% |
| 4               | 0     | $100 \times 0 / 9$% |
| 5               | 2     | $100 \times 2 / 9$% |

# Exercise

- Sometimes, the frequency in % is provided instead of the count.

| Pixel intensity | Count | Frequency |
|-----------------|-------|-----------|
| 0               | 5     | 56% |
| 1               | 1     | 11% |
| 2               | 0     | 0% |
| 3               | 1     | 11% |
| 4               | 0     | 0% |
| 5               | 2     | 22% |

![Corresponding histogram](img/histogram-percent.png)

# Back to the example: Contrast enhancement

![Image with a poor contrast](img/Chapter 5 - Introduction to image processing43.png)

# See the image histogram:

* Plots the number of pixels for each value

![Image with a poor contrast](img/Chapter 5 - Introduction to image processing44.png)

* Most of the intensity values used are in the middle of the dynamic range, the image is grey with poor contrast.
  * No black pixels,
  * No white pixels,
  * Just grey pixels.
* **To improve the contrast, we want to use the whole range of possible values (0 to 255),** enable
  * Black pixels,
  * White pixels, and
  * Grey pixels.

# How? Make the min = 0:

- Subtract the smallest pixel value of the image to all the pixels:
- $Image'(i,j) = Image(i,j) - \min(Image)$
- The image will look dark.

# How? Make the min = 0:

- Subtract the smallest pixel value of the image to all the pixels:
- $Image'(i,j) = Image(i,j) - \min(Image)$
- The image will look dark.

| Notation | Image | Corresponding histogram |
|----------|-------|-------------------------|
| $Image(i,j)$ | <img src="img/Chapter 5 - Introduction to image processing45.png" width=500px alt="original image" /> | <img src="img/Chapter 5 - Introduction to image processing46.png" width=310px alt="its histogram" /> |
| $Image'(i,j)$ | <img src="img/Chapter 5 - Introduction to image processing48.png" width=500px alt="transformed image" /> | <img src="img/Chapter 5 - Introduction to image processing47.png" width=310px alt="its histogram" /> |

# How? Normalise the image between 0 and 1:

- Divide all the pixels with the range of pixel values $(\max(Image) - \min(Image))$
- $Image''(i,j) = \frac{Image(i,j) - \mathrm{min}(Image)}{\max(Image) - \min(Image)}$

# How? Rescale the image so that the max is 255:

- Multiply all the pixels with 255
- $Image'''(i,j) = 255 \times \frac{Image(i,j) - \mathrm{min}(Image)}{\max(Image) - \min(Image)}$

# How? Rescale the image so that the max is 255:

- Multiply all the pixels with 255
- $Image'''(i,j) = 255 \times \frac{Image(i,j) - \mathrm{min}(Image)}{\max(Image) - \min(Image)}$

| Notation | Image | Corresponding histogram |
|----------|-------|-------------------------|
| $Image'(i,j)$ | <img src="img/Chapter 5 - Introduction to image processing48.png" width=500px alt="transformed image" /> | <img src="img/Chapter 5 - Introduction to image processing47.png" width=310px alt="its histogram" /> |
| $Image''(i,j)$ | <img src="img/Chapter 5 - Introduction to image processing57.png" width=500px alt="transformed image" /> | <img src="img/Chapter 5 - Introduction to image processing56.png" width=310px alt="its histogram" /> |

# More general case

- Smallest pixel value does not have to be 0
- Largest pixel value does not have to be 255
- See [http://scikit-image.org/docs/dev/user_guide/data_types.html](http://scikit-image.org/docs/dev/user_guide/data_types.html)
- See [Lab 2](https://github.com/effepivi/ICE-3111-Computer_Vision/tree/main/Labs/Lab-02):

<img src="https://github.com/effepivi/ICE-3111-Computer_Vision/raw/main/Labs/Lab-02/img/visualisation-eq.png" width=700px alt="General equation" />

- with $f$ original image and $g$ the visualisation image.
- In I the previous example,
  - $\min(g) = 0$,
  - $\max(g) = 255$,
  - $T_{low} = \min(f)$, and
  - $T_{high} = \max(f)$

# 3. Compute the negative image

# 3. Compute the negative image

![Positive](img/Chapter 5 - Introduction to image processing63.png)
![Negative](img/Chapter 5 - Introduction to image processing64.png)

    Consider an image in UINT8

- 0 should become 255
- 1 should become 254
- 2 should become 253
- …
- 255 should become 0

Given an intensity, _i_ , what is the new intensity?

# 3. Compute the negative image

- Consider an image in UINT8
- Given an intensity, _i_ , what is the new intensity?
- $Negative(x,y) = 255 - Positive(x,y)$, and
- $Positive(x,y) = 255 - Negative(x,y)$

# More general case

- Smallest pixel value does not have to be 0
- Largest pixel value does not have to be 255
- See [http://scikit-image.org/docs/dev/user_guide/data_types.html](http://scikit-image.org/docs/dev/user_guide/data_types.html)
- $Negative(i,j) = \min(Positive) + \max(Positive) - Positive(i,j)$
- Other equations are possible
- Must ensure that the $Netagive$ of the $Negative$ is the $Positive$.

```c
bool i = false;
!i == true;
```

# 4. Image blending

- Cross-dissolve between two images

$$g(x,y) - (1 - \alpha) f_0(x,y) + \alpha f_1(x,y)$$

where $\alpha$ is between 0 and 1

# Where is it used?

Example: [Transitions between two scenes in cinema](https://en.wikipedia.org/wiki/Film_transition)

- Fade in/out
- Dissolve

[![Example](img/300px--A2o_dissolve.ogv.jpg)](https://upload.wikimedia.org/wikipedia/commons/6/6c/A2o_dissolve.ogv)
(From wikimedia: [https://en.wikipedia.org/wiki/File:A2o_dissolve.ogv](https://en.wikipedia.org/wiki/File:A2o_dissolve.ogv))
# Exercise

- Derive this formula in a `for` loop

$$g(x,y) = (1 - \alpha) f_0(x,y) + \alpha f_1(x,y)$$

that blends the image $f_0$ and $f_1$ over $t$ iterations:

```c
for (int i = 0; i < t; ++i)
{
  float alpha = ???;

  g = (1.0 - alpha) * f_0 + alpha f_1;
}
```

# 5. Image matting and compositing

![ALT](img/Chapter 6 - Point operators and linear filtering87.png)

Matting – the process of extracting an object from the original image

Compositing – the process of inserting the object into a different image

It is convenient to represent the extracted object as an RGBA image


# Transparency, alpha channel

![ALT](img/Chapter 6 - Point operators and linear filtering88.png)

* RGBA – red. green. blue. alpha
  * alpha = 0 – transparent pixel
  * alpha = 1 – opaque pixel
* Compositing
  * Final pixel value:
  * Multiple layers:

Linear interpolation



# End of Chapter on Point operators
