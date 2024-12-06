# NatalIA: PBF-US1 (Phantom Blind-sweeps for Fetal Ultrasound Scanning)

<p style="margin-bottom: 120px;">
<img src="assets/combined_logos_reordered.png" height= "70" alt="logo Galileo" style="position: absolute; background: white; padding: 10px; border-radius: 10px">
</p>

In low-income countries, particularly in remote communities with a shortage of trained sonographers and high maternal mortality rates, developing AI tools to assist non-experts in accurately identifying relevant fetal planes and potential anomalies during ultrasound exams is crucial. This dataset includes 19407 ultrasound frames collected from 90 videos of a 23-week gestational age fetal ultrasound phantom, recorded through free-hand sweeps by non-experts. These data are valuable for advancing research on second-trimester pregnancies. The frames were extracted from videos captured using a point-of-care ultrasound (POCUS) device in obstetric mode, set to a maximum depth of 16 cm. In total, 45 volunteers with no prior ultrasound experience recorded the videos while following four predefined scanning paths: vertical, horizontal, and two diagonal trajectories, with four different fetal poses. This approach creates a dataset that reflects real-world variability in non-expert settings, simulating ultrasound exams conducted by untrained personnel.

## Overview

This Python package provides a collection of standard fetal planes generated using a US-7a SPACE FAN phantom (Kyoto Kagaku) and Clarius C3 HD3 point-of-care ultrasound device. The package is intended for use in medical education, training, and research related to fetal ultrasound imaging.

## Features

- **Standard Fetal Planes**: Includes a comprehensive set of five standard fetal planes:
  - Biparietal.
  - Abdominal.
  - Heart.
  - Femur.
  - Spine.
- **Phantom Device Simulation**: The images are generated using a phantom device, providing realistic simulated fetal anatomy of a 23 weeks fetus. The fetus orientation and presentation was changed in four different poses.
- **Free-Hand Ultrasound**: To gather all the collected images volunteers without prior experience in ultaround performe a free-hand protocol consisting in four diferent sweeps:
  - 1 Vertical.
  - 1 Horizontal.
  - 2 Diagonal.

<p align="center">
 <img src="assets/protocols.png" width="500" alt="images of the four protocols used">
<p>

- **Point-Of-Care Ultrasound**:The videos were collected using a portable ultrasound with a maximum depth of 16 cm and 24 Frames Per Second.
- **Easy Integration**: Simple Python API for loading and accessing fetal plane images, facilitating integration into existing applications and workflows.
- **Open Source**: The package is open source, allowing for customization, extension, and contribution from the community.

## Installation

You can install the package via pip:

```bash
pip install PBFUS1
```

## Usage

```python
from PBFUS1.metadata import count_elements_per_class, get_images_by_class_value, plot_random_images, load_studies_metadata
from PBFUS1.data_loader import download_dataset, load_images_info

# Download dataset
download_dataset()
## Downloading dataset: 260091it [00:05, 44607.73it/s]
## Dataset downloaded and extracted to ./data

#Load images info
images_df = load_images_info()
images_df.head()
## file_name	studie	class	value	image
## 0	cineframe_100_2024-05-03T12-19-10.jpeg	Obstetrics Exam - 03-May-2024_1216_PM	Biparietal standard plane	0	./data/Obstetrics Exam - 03-May-2024_1216_PM/c...
##1	cineframe_147_2024-05-02T08-37-43.jpeg	Obstetrics Exam - 02-May-2024_817_AM	Biparietal standard plane	0	./data/Obstetrics Exam - 02-May-2024_817_AM/ci...
##2	cineframe_146_2024-05-02T08-37-43.jpeg	Obstetrics Exam - 02-May-2024_817_AM	Biparietal standard plane	0	./data/Obstetrics Exam - 02-May-2024_817_AM/ci...
##3	cineframe_106_2024-05-03T15-03-07.jpeg	Obstetrics Exam - 03-May-2024_300_PM	Biparietal standard plane	0	./data/Obstetrics Exam - 03-May-2024_300_PM/ci...
##4	cineframe_150_2024-05-02T08-57-41.jpeg	Obstetrics Exam - 02-May-2024_854_AM	Biparietal standard plane	0	./data/Obstetrics Exam - 02-May-2024_854_AM/ci...

# load studies metadata
studies_df = load_studies_metadata()
studies_df.head()
## 	Study Name	protocol	position	Age	Gender	Level of Education	Ultrasound Experience	Years of Experience	Race/Ethnicity	Visual Impairment	specify	dominant hand
## 0	Obstetrics Exam - 02-May-2024_1144_AM	Vertical	OA	20	Female	High School	1	0	Hispanic	Yes	Astigmatism and Myopia	Right-handed
## 1	Obstetrics Exam - 02-May-2024_1159_AM	Horizontal	OA	20	Female	High School	1	0	Hispanic	Yes	Astigmatism and Myopia	Right-handed
## 2	Obstetrics Exam - 02-May-2024_1204_PM	Diagonal /	OA	22	Female	High School	1	0	Hispanic	No	NaN	Right-handed
## 3	Obstetrics Exam - 02-May-2024_1209_PM	Diagonal	OA	22	Female	High School	1	0	Hispanic	No	NaN	Right-handed
## 4	Obstetrics Exam - 02-May-2024_1212_PM	Vertical	OA	23	Female	High School	1	0	Hispanic	No	NaN	Right-handed


class_count = count_elements_per_class()
## Class 'Biparietal standard plane' (Value: 0): 42 elements
## Class 'Abdominal standard plane' (Value: 1): 63 elements
## Class 'Heart standard plane' (Value: 2): 61 elements
## Class 'Spine standard plane' (Value: 3): 134 elements
## Class 'Femur standard plane' (Value: 4): 46 elements
## Class 'No plane' (Value: 5): 19061 elements

class_value = 2
images_by_class_value = get_images_by_class_value(class_value)
print(f"First 10 images in class with value '{class_value}':\n{images_by_class_value.iloc[0:10]}")
## First 10 images in class with value '2':
## 77     cineframe_100_2024-05-02T08-36-34.jpeg
## 78     cineframe_100_2024-05-02T08-37-43.jpeg
## 81     cineframe_100_2024-05-02T08-38-50.jpeg
## 83     cineframe_102_2024-05-02T08-36-34.jpeg
## 84     cineframe_102_2024-05-02T08-37-43.jpeg
## 88     cineframe_105_2024-05-02T08-38-08.jpeg
## 818     cineframe_70_2024-05-02T08-58-54.jpeg
## 864    cineframe_111_2024-05-02T08-57-41.jpeg
## 865    cineframe_112_2024-05-02T08-57-41.jpeg
## 877    cineframe_123_2024-05-02T08-57-22.jpeg
## Name: name_file, dtype: object

# Show 5 random images with the name and value.
plot_random_images(5,fig_size=(15,2))
```

<p align="center">
 <img src="assets/5ImagesPerClass.png" width="500" alt="5 random images per class">
<p>

## Citation

If you use this dataset, please cite it as follows:

González, D., Barrientos, J. P., Perez, M., Fajardo, J., Reyna, F., & Lara, A. (2024). NatalIA: PBF-US1 (Phantom Blind-sweeps for Fetal Ultrasound Scanning) (1.0.0) [Data set]. Zenodo. [https://doi.org/10.5281/zenodo.14193949](https://doi.org/10.5281/zenodo.14193949)

For BibTeX format:

```bibtex
@dataset{Gonzalez2024,
  author       = {González, D. and Barrientos, J. P. and Perez, M. and Fajardo, J. and Reyna, F. and Lara, A.},
  title        = {NatalIA: PBF-US1 (Phantom Blind-sweeps for Fetal Ultrasound Scanning)},
  year         = {2024},
  version      = {1.0.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.14193949},
  note         = {[Data set]},
  url          = {https://doi.org/10.5281/zenodo.14193949}
}

```

## Acknowledgments

This project was funded by CLIAS (Centro de Inteligencia Artificial y Salud para América Latina y el Caribe), an initiative of CIIPS (Centro de Implementación e Innovación de Políticas de Salud) at IECS (Instituto de Efectividad Clínica y Sanitaria), with support from IDRC (International Development Research Centre).

## License

Use the planes for educational purposes, training simulations, or research.

![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)

## Contact

For more information about the dataset or the package, feel free to contact:

- **Douglas González** at [**duglasa@galileo.edu**](**mailto:duglasa@galileo.edu**)
- **Juan Pablo Barrientos** at [**juan.barrientos@galileo.edu**](**mailto:juan.barrientos@galileo.edu**)
