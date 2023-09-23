<p><img src="https://github.com/Mahmoud-H97/NRET/assets/65749493/df15592d-793a-4bc5-adef-373abfbf85f9" style="width:150px; hight:150px;" align="left" />
</p>

<br/>
<br/>




# NRET
A Python package to retrieve canopy aboveground Nitrogen content using a hybrid modelling approach.
#### Mahmoud H. Ahmed ``mahmoudhatim55@gmail.com``

## Install in Anaconda env

The package can be easily installed using the command

`conda install -c mah010 nret`

it **should** work on Python 3.6. and newer versions (Tested on 3.9.)

## pip install the package

You can also pip install the package to your environment and it should also work fine (Tested in Google Colaboratory)

`pip install nret`

## Discription
This repository is your comprehensive toolkit for conducting geospatial analysis to retrieve canopy aboveground Nitrogen content and estimating biomass, with a primary focus on Wheat. It offers a systematic, step-by-step approach, complemented by Jupyter notebooks designed for Google Colab, to guide you through the entire process.

Major phases:

* **Generating a Learning Database**: This repository describes how to use the NRET package for generating biochemical and biophysical input variables, simulating canopy reflectance, and estimating fractional absorbed photosynthetically active radiation (fAPAR) through the PROSAIL-PRO model. At the end of this step, you will have a dataframe containing biochemical and biophysical input variables, along with their respective canopy reflectance and fAPAR simulations. This database forms the foundation for subsequent analysis.

* **Gaussian Process Regression (GPR) Modeling**: Learn how to set up and train a Gaussian Process Regression (GPR) model on the generated database, validate its performance, and save the trained model. 

* **Sentinel-2 Imagery Prediction**: Apply your trained Gaussian Process Regression (GPR) model to real Sentinel-2 imagery, enabling precise predictions for the specific parameter of interest. Subsequently, create maps to visualize both the predicted variable and the uncertainty associated with these predictions, represented as standard deviation maps.

By following the guidance and examples provided in this repository, you'll gain the knowledge and tools needed to perform an in-season canopy aboveground Nitrogen content retrieval and biomass estimation efficiently and effectively. 

