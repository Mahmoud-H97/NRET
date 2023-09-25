<p><img src="https://github.com/Mahmoud-H97/NRET/assets/65749493/df15592d-793a-4bc5-adef-373abfbf85f9" style="width:150px; hight:150px;" align="left" />
</p>

<br/>
<br/>




# NRET
A Python package to retrieve canopy aboveground Nitrogen content using a hybrid modelling approach.
#### Mahmoud H. Ahmed ``mahmoudhatim55@gmail.com``

[![PyPI version](https://badge.fury.io/py/nret.svg)](https://badge.fury.io/py/nret)

## pip install the package

You can pip install the package to your environment ( Anaconda or Google colab) and it should also work fine (Tested in a local Windows machine & in Google Colaboratory).
it **should** work on Python 3.6. and newer versions (Tested on 3.9.)

`pip install nret`

## Discription
This repository is your comprehensive toolkit for conducting geospatial analysis to retrieve canopy aboveground Nitrogen content and estimating biomass, with a primary focus on Wheat. It offers a systematic, step-by-step approach, complemented by Jupyter notebooks designed for Google Colab, to guide you through the entire process.

Major phases:
* **Sensitivity Analysis**: Starting with a simple sensitivity analysis aims to see the impact of certain input parameters in the simulated reflectance of PROSAIL-PRO.
* **Generating a Learning Database**: This repository describes how to use the NRET package for generating biochemical and biophysical input variables, simulating canopy reflectance, and estimating fractional absorbed photosynthetically active radiation (fAPAR) through the PROSAIL-PRO model. At the end of this step, you will have a dataframe containing biochemical and biophysical input variables, along with their respective canopy reflectance and fAPAR simulations. This database forms the foundation for subsequent analysis.

* **Gaussian Process Regression (GPR) Modeling**: Learn how to set up and train a Gaussian Process Regression (GPR) model on the generated database, validate its performance, and save the trained model. 

* **Sentinel-2 Imagery Prediction**: Apply your trained Gaussian Process Regression (GPR) model to real Sentinel-2 imagery, enabling precise predictions for the specific parameter of interest. Subsequently, create maps to visualize both the predicted variable and the uncertainty associated with these predictions, represented as standard deviation maps.

By following the guidance and examples provided in this repository, you'll gain the knowledge and tools needed to perform an in-season canopy aboveground Nitrogen content retrieval and biomass estimation efficiently and effectively. 

## Sensitivity Analysis
The parameter sensitivity analysis in this [Notebook](https://colab.research.google.com/drive/1akdlPXksWSi2tBTLvOYCewFQVqJTGaA7?usp=sharing) was executed to ascertain the extent of
influence employed by individual parameters on the simulated canopy reflectance of
PROSAIL-PRO. These parameters involved all of the sun and sensor angles (SZA, VZA, and
psi), LAI, and Cp (you can adjust it to any parameter you want). To carry out this analysis, the approach involved maintaining all input
parameters at constant values, with the exception to the parameter under examination. Subsequently, PROSAIL was used to simulate canopy reflectance while
systematically adjusting the parameter’s value from its minimum value to its maximum value.
* Note: The python binding of PROSAIL used within the nret package was taken from [J Gomez-Dans](https://github.com/jgomezdans/prosail/tree/master)

## Generating a Learning Database
The biophysical and biochemical variables (BV) play a crucial role as input parameters for
PROSAIL-PRO during forward simulation. The sensible selection of their ranges is essential
to ensure that the simulated reflectance accurately captures meaningful features of the BV. 
This [Notebook](https://colab.research.google.com/drive/1Uami5cwG7Afx2JmAYE30jEx8g2m_XYlS?usp=sharing) shows an example on how to use the nret function "generate_input_samples", this function takes two dictonaries as an input "parameter_ranges" and "distribution_laws", along with the number of input points to generate and the max LAI value. This function is designed to restrict the range of variation for certain variables based on the Leaf Area Index 
(LAI) value according to the concept introduced by Weiss and Baret
(2016) . The restriction is achieved by assuming a linear relationship between LAI and the variable's range of variation.
The variables that will be restricted are represented by 'Vmin' (minimum value) and 'Vmax' (maximum value).
Initially, 'Vmin(0)' and 'Vmax(0)' store the same old minimum and maximum values for the variable.
'LAImax' represents the maximum LAI value considered, and as LAI increases, the range of variation for 'Vmin' 
and 'Vmax' changes linearly until it reaches 'Vmin(LAImax)' and 'Vmax(LAImax)'.

The values 'Vmin(LAImax)' and 'Vmax(LAImax)' define the co-distributions. These values were derived empirically, 
assuming that larger LAIs correspond to a more restricted range of the other variables.

The code will automatically adjust the values of 'Vmin' and 'Vmax' based on the provided relationship with LAI, thereby 
creating restricted ranges for the variables as LAI increases.

After generating the input database, the next step is looping throughout all the points and simulating the canopy reflectance and fAPAR using "nret.run_prosail" and "nret.calculate_fapar".

The computation of aboveground N content from the LUT
entry points (specifically by using LAI and Cp for each input point) , was done as suggested by Berger et al (2020).


## Train a GPR Model
This [Notebook](https://colab.research.google.com/drive/1rZzsSSGsG2-N00HqvSg2E1rU8AcSonkM?usp=sharing) provides a detailed guide on how to partition the database into training and validation sets, establish a Gaussian Process model, train and validate it. Additionally, it outlines the process of saving the trained parameters and training data, enabling the reconstruction of the trained model at a later time. (Please note that while Gaussian Process Regression is recommended, you have the flexibility to explore other regression models if they better suit your needs.)

## Predict on Sentinel-2 Bands
In this [Notebook](https://colab.research.google.com/drive/1QYzftGsZXp2OOUL4ZIvSVQh3FTHKg44q?usp=sharing), the process of reconstructing the trained Gaussian Process Regression (GPR) model is outlined, along with instructions on making predictions using Sentinel-2 images for a specific cropping season. Furthermore, the notebook demonstrates how to generate maps that display the predicted values and associated uncertainties for each pixel.
## Interesting Statistical Analysis
Finally, this [Notebook](https://colab.research.google.com/drive/1XDyt_rGjk23-kA2y0yKRC96SGafC70EL?usp=sharing) provides an in-depth exploration of statistical analyses, covering both the original Sentinel-2 (S2) images and the predicted values. Explore this notebook for valuable insights into the statistical aspects of your geospatial analysis.

References
----------
* .. [Berger 2020] Retrieval of aboveground crop nitrogen content with a hybrid machine learning method.
* .. [Weiss 2016] Fapar, Fcover (2016) S 2 ToolBox Level 2 products : LAI , FAPAR , FCOVER Version 1.
