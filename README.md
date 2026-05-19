# XR Simulation and U-Net Segmentation for Real XCT Workflows

Code repository for the [workshop day](https://dxct.co.uk/workshop-day/) at the [dimensional X-ray Computed Tomography (dXCT)](https://dxct.co.uk/), 
16th of June 2026. 
Registrations are open and will be closed on the 29th of May. 
[Attend the training and conference](https://dxct.co.uk/conference-registration/).

## Description
This hands-on workshop provides an end-to-end workflow for X-ray Computed Tomography (XCT), combining physics-based simulation with machine-learning segmentation.

### Session 1 (Prof Franck P. Vidal)
Participants will learn how to generate realistic, XCT projection data using the [**gVXR** package](https://gvirtualxray.sourceforge.io/). 
The focus will be on building simulation setups that mirror practical XCT scenarios and producing synthetic datasets suitable for downstream analysis and model training.

### Session 2 (Dr Matthew Peter Jones)
Participants will train **machine-learning segmentation models**, focusing on the **U-Net** architecture.  
The session will demonstrate a practical training workflow and show how **synthetic data from Session 1** can be incorporated to improve robustness, reduce labelling burden, and support generalisation to real CT volumes.

*Both sessions are grounded in **battery CT examples**, with exercises designed to be practical, transferable, and 
directly relevant to other imaging workflows.*

 
## Who this workshop is for

- CT users interested in **simulation** for method development, protocol testing, or data augmentation;
- Researchers working with **XCT data** who want a clear route from dataset creation to segmentation;
- Practitioners new to **ML segmentation** with python who want a guided, practical introduction (not just theory).

### Learning objectives
By the end of the workshop, you will be able to:

- Set up and run **gVXR** simulations to generate synthetic XCT datasets;
- Understand how simulation choices (geometry, materials, noise, artefacts) affect the data you generate;
- Build a practical **U-Net segmentation** training workflow for CT-derived data;
- Use **synthetic data augmentation** strategically to improve segmentation performance and reliability.

### Pre-requisites
- Some familiarity with **CT imaging and image analysis** is recommended;
- Some familiarity with **Python** is useful but not required;
- No ML background required (we’ll focus on practical workflow and good habits).

### Practical requirements
- Exercises will use **pre-prepared cloud notebooks/scripts**, with guided steps throughout;
- **All participants must bring a laptop** (Windows/macOS/Linux) suitable for running Python notebooks.

## Installation

You do not need to install anything for the training during the workshop day. 
If you want to recreate it at home, we recommend that you use the Conda environment file that is provided for your 
convenience. 

### Using Conda

```bash
conda env create -f environment.yml
conda activate gvxr-dXCT2026
```

### Morning session

- [Test installation](notebooks/morning/test_installation.ipynb): 
  Run the quick test script provided with gVirtualXray's Python package to make sure the installation is working well on your system.
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TomographicImaging/gVXR-training-dXCT2026/blob/main/notebooks/morning/test_installation.ipynb)
- [First X-ray simulation](notebooks/morning/first_xray_simulation.ipynb): 
  Explore the step-by-step notebook to create our first X-ray radiograph. 
  A mono-material object is imaged with a monochromatic source and an ideal detector. 
  We show how to visualise the X-ray radiograph and take a screenshot of the 3D visualisation of the simulation environment.
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TomographicImaging/gVXR-training-dXCT2026/blob/main/notebooks/morning/first_xray_simulation.ipynb)
- [Numpy integration](notebooks/morning/numpy_integration.ipynb): Experiment with the Numpy integration to speed up 
  the simulation. 
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TomographicImaging/gVXR-training-dXCT2026/blob/main/notebooks/morning/numpy_integration.ipynb)
- [3D visualisation](notebooks/morning/visualisation.ipynb): 
  Get familiar with the three different 3D visualisation methods provided with gVXR, 
  1. K3D to interactively visualise the 3D scene in a Jupyter widget, 
  2. a customisable static 3D visualisation, and 
  3. an interactive 3D visualisation window. <br/>
  In this notebook you will also create a multi-material sample. 
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TomographicImaging/gVXR-training-dXCT2026/blob/main/notebooks/morning/visualisation.ipynb)
- [Polychromtic X-ray tube spectra](notebooks/morning/polychromatism.ipynb):
  In this notebook we explore how to specify polychromtic X-ray tube spectra, without and with filtration. 
  We also shows how to plot the spectrum. 
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TomographicImaging/gVXR-training-dXCT2026/blob/main/notebooks/morning/polychromatism.ipynb)
- [Scintillation](notebooks/morning/scintillation.ipynb): 
  In this notebook we explore how to create a detector with a scintillator.
  We also shows how to plot the corresponding energy response. 
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TomographicImaging/gVXR-training-dXCT2026/blob/main/notebooks/morning/scintillation.ipynb)

## How to find help

### General inquiry

- Email us (Franck P. Vidal, STFC | Matthew Peter Jones, UCL);
- Join the discord: [https://discord.gg/qebNF8mz](https://discord.gg/qebNF8mz);
- Raise an issue on GitHub: [https://github.com/TomographicImaging/gVXR-training-dXCT2026/issues](https://github.com/TomographicImaging/gVXR-Tutorials/issues).

### gVXR-specific inquiry

Same as above plus the following:
- Open a ticket on SourceForge: [https://sourceforge.net/p/gvirtualxray/tickets](https://sourceforge.net/p/gvirtualxray/tickets);
- Subscribe to the mailing list: [https://sourceforge.net/projects/gvirtualxray/lists/gvirtualxray-discuss](https://sourceforge.net/projects/gvirtualxray/lists/gvirtualxray-discuss);
- Check the technical documentation, e.g. calling `help(gvxr)` for help on the Python package or something like `help(gvxr.createNewContext)` for a specific function.
