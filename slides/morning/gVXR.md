---
title: gVXR
author: Prof Franck P. Vidal
subtitle: ICE-3111 Computer Vision
date: 2026-06-16
keywords: gVXR, gVirtualXray, dXCT, X-ray simulation
institute: 
fontsize: 11pt
lang: en-gb
---

# Contents

1. What is a point operator?
2. Improving the brightness and contrast
3. Negative image
4. Image blending

# This slide has columns

::: columns

:::: column
left
::::

:::: column
right
::::

:::

# 1. What is a point operator?

# 1. What is a point operator?

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
