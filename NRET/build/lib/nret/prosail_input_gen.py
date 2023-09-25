#@ author : Mahmoud H. Ahmed
#!/usr/bin/env python
import pandas as pd
import numpy as np
'''
This function is to generate random input points for PROSAIL simulation.
This code is designed to restrict the range of variation for certain variables based on the Leaf Area Index 
(LAI) value. The restriction is achieved by assuming a linear relationship between LAI and the variable's range of variation.
The variables that will be restricted are represented by 'Vmin' (minimum value) and 'Vmax' (maximum value).

Initially, 'Vmin(0)' and 'Vmax(0)' store the same old minimum and maximum values for the variable.
'LAImax' represents the maximum LAI value considered, and as LAI increases, the range of variation for 'Vmin' 
and 'Vmax' changes linearly until it reaches 'Vmin(LAImax)' and 'Vmax(LAImax)'.

The values 'Vmin(LAImax)' and 'Vmax(LAImax)' define the co-distributions. These values were derived empirically, 
assuming that larger LAIs correspond to a more restricted range of the other variables.

The code will automatically adjust the values of 'Vmin' and 'Vmax' based on the provided relationship with LAI, thereby 
creating restricted ranges for the variables as LAI increases.


the parameters, min values, max values, and mode values shoul be identified first in 
dictionary file {}. e.g. { 'parameter1': {'min': 1, 'max': 5, 'mode': 2}, 'parameter2': {'min': 0.1, 'max': 5, 'mode': 1},...}.
The distribution laws should be identified in a separate dictionary with the parameters names
and the desired distribution laws e.g. { 'parameter1': 'log-normal', 'parameter2': 'gaussian', 'parameter3': 'uniform',...}.
The number of generated samples is just a variable with one value.


  Parameters
    -----------
    parameter_ranges: dictonary
        the parameters, min values, max values, mode, Vmin(0), Vmax(0), Vmin(LAImax), Vmin(LAImax) and standard deviation values
        should be identified first in dictionary file {}. e.g.
        {
    'n': {'min': 1.2, 'max': 2.2, 'mode': 1.5, 'Vmin(0)': 1.2, 'Vmax(0)': 2.2, 'Vmin(LAImax)': 1.3, 'Vmax(LAImax)': 1.8, 'std': 0.3 },
    'cab': {'min': 20, 'max': 90, 'mode': 45, 'Vmin(0)': 20, 'Vmax(0)': 90, 'Vmin(LAImax)': 45, 'Vmax(LAImax)': 90,  'std': 30},  ...
         }

    distribution_laws: dictonary
        A dictionary that contains the distribution laws for all the parameters.
        e.g.
        distribution_laws = {
                             'n': 'gaussian',
                            'cab': 'gaussian',...
                            }

    num_samples: float
        Number of samples to generate.

    LAI_max: float
        the maximum LAI value.
    
    Returns
    --------
    Dataframe with input points

        References
    ----------
    .. [Weiss 2016] Fapar, Fcover (2016) S 2 ToolBox Level 2 products : LAI , FAPAR , FCOVER Version 1.

    

'''



def link_distribution_to_lai(value, Vmin_0, Vmax_0, Vmin_LAI_max, Vmax_LAI_max, LAI, LAI_max):

    Vmin_LAI = Vmin_0 + LAI * (Vmin_LAI_max - Vmin_0) / LAI_max
    Vmax_LAI = Vmax_0 + LAI * (Vmax_LAI_max - Vmax_0) / LAI_max
    value_star = Vmin_LAI + ((Vmax_LAI - Vmin_LAI) * (value - Vmin_0) / (Vmax_0 - Vmin_0))
   
    return value_star

def generate_input_samples(parameter_ranges, distribution_laws, num_samples, LAI_max):
    inputs = {}
    
    for param, param_range in parameter_ranges.items():
        min_val = param_range['min']
        max_val = param_range['max']
        mode_val = param_range['mode']
        Vmin_0 = param_range.get('Vmin(0)', None)
        Vmax_0 = param_range.get('Vmax(0)', None)
        Vmin_LAI_max = param_range.get('Vmin(LAImax)', None)
        Vmax_LAI_max = param_range.get('Vmax(LAImax)', None)
        std_dev = param_range['std']

        if Vmin_0 is None:
            Vmin_0 = min_val
        if Vmax_0 is None:
            Vmax_0 = max_val
        if Vmin_LAI_max is None:
            Vmin_LAI_max = min_val
        if Vmax_LAI_max is None:
            Vmax_LAI_max = max_val
        
        distribution = distribution_laws[param]
        
        if param in ['n', 'cab', 'car', 'cbrown', 'cw', 'cm', 'lidfa', 'hspot']:

            if distribution == 'log-normal':
                samples = np.random.lognormal(mean=np.log(mode_val), sigma=1, size=num_samples)
            elif distribution == 'gaussian':
                samples = np.random.normal(loc=mode_val, scale=std_dev, size=num_samples)
                samples = np.clip(samples, min_val, max_val) # Clip values to the range [min_val, max_val]
            elif distribution == 'uniform':
                samples = np.random.uniform(low=min_val, high=max_val, size=num_samples)
            else:
                raise ValueError("Invalid distribution for parameter: {}".format(param))
        else:
            if distribution == 'log-normal':
                samples = np.random.lognormal(mean=np.log(mode_val), sigma=1, size=num_samples)
            elif distribution == 'gaussian':
                samples = np.random.normal(loc=mode_val, scale=std_dev, size=num_samples)
                samples = np.clip(samples, min_val, max_val)  # Clip values to the range [min_val, max_val]
            elif distribution == 'uniform':
                samples = np.random.uniform(low=min_val, high=max_val, size=num_samples)
            else:
                raise ValueError("Invalid distribution for parameter: {}".format(param))
        
        inputs[param] = samples

# Link distributions to LAI for n, cab, car, cbrown, cw, cm, lidfa, hspot
    for param in ['n', 'cab', 'car', 'cbrown', 'cw', 'cm', 'lidfa', 'hspot', 'ant', 'prot', 'cbc', 'rsoil', 'psoil']:
        inputs[param] = link_distribution_to_lai(inputs[param],
                                                 parameter_ranges[param]['Vmin(0)'],
                                                 parameter_ranges[param]['Vmax(0)'],
                                                 parameter_ranges[param]['Vmin(LAImax)'],
                                                 parameter_ranges[param]['Vmax(LAImax)'],
                                                 inputs['lai'],
                                                 LAI_max)
        
        
        # Clip the linked values to the specified range
        inputs[param] = np.clip(inputs[param], parameter_ranges[param]['min'], parameter_ranges[param]['max'])
    
    # Round the values to three decimal places for specified parameters
    for param in ['n', 'cab', 'car', 'cbrown', 'lai', 'lidfa', 'ant']:
        inputs[param] = np.round(inputs[param], 3)
    for param in ['cw', 'cm', 'hspot', 'prot', 'cbc', 'rsoil', 'psoil']:
        inputs[param] = np.round(inputs[param], 5)

    df = pd.DataFrame(inputs)
    
    return df
