#!/usr/bin/env python
import nret
import numpy as np
import pandas as pd
from .FourSAIL import foursail
from .prospect_d import run_prospect
from .sail_model import run_prosail
from .fAPAR import calculate_fapar



def simulate_df (tts, tto, psi, input_dataframe,):
    """
    This function is to run prosail using a series of input points in the form of pandas dataframe.
    
    Parameters
    -----------
    tts: float
        Solar zenith angle
    tto: float
        Sensor zenith angle
    psi: float
        Relative sensor-solar azimuth angle ( saa - vaa )
    input_dataframe: df
        A dataframe that contains prosail's crop input parameters (n, cab, car, cbrown, cw, cm, lai,
          lidfa, hspot, ant, prot, cbc, rsoil, psoil), by default the version that will 
          be used is PROSAIL-PRO.

    Returns
    --------
    The same data frame with canopy reflectance, S2-A bands (2, 3, 4, 5, 6, 7, 8, 8A, 11, 12) and fAPAR.

    """



    # Assuming your DataFrame is named 'input_dataframe'
    # Create an empty list to store the reflectance arrays
    reflectance_data = []
    fapar_data = []
    rho = []

    # Load up the spectral response functions for S2 (Source: https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/document-library/-/asset_publisher/Wk0TKajiISaR/content/sentinel-2a-spectral-responses)
    # ISSUE: 3.1, Date: 21 Jun 2022
    srf = np.loadtxt("S2A-SRF.csv", skiprows=1, delimiter=",")[100:, :]
    srf[:, 1:] = srf[:, 1:]/np.sum(srf[:, 1:], axis=0)
    srf_land = srf[:, [2, 3, 4, 5, 6, 7, 8, 9, 12, 13]].T

    # Loop over the DataFrame rows
    for index, row in input_dataframe.iterrows():
        n = row['n']
        cab = row['cab']
        car = row['car']
        cbrown = row['cbrown']
        cw = row['cw']
        cm = row['cm']
        lai = row['lai']
        lidfa = row['lidfa']
        hspot = row['hspot']
        ant = row['ant']
        prot = row['prot']
        cbc = row['cbc']
        rsoil_value = row['rsoil']
        psoil_value = row['psoil']

        # Run PROSAIL for each set of parameters
        (
        tss,
        too,
        tsstoo,
        rdd,
        tdd,
        rsd,
        tsd,
        rdo,
        tdo,
        rso,
        rsos,
        rsod,
        rddt,
        rsdt,
        rdot,
        rsodt,
        rsost,
        rsot,
        gammasdf,
        gammasdb,
        gammaso,
    ) = run_prosail(
        n,
        cab,
        car,
        cbrown,
        cw,
        cm,
        lai,
        lidfa,
        hspot,
        tts,
        tto,
        psi,
        ant=ant,
        prot=prot,
        cbc=cbc,
        alpha=40,
        prospect_version='PRO',
        typelidf=2,
        lidfb=None,
        factor="ALLALL",
        rsoil0=None,
        rsoil=np.full(2101, rsoil_value),
        psoil=np.full(2101, psoil_value),
        soil_spectrum1=None,
        soil_spectrum2=None,
        )
        rho.append(tss)

        #calculate fAPAR for each set of parameters
        fapar_data.append(nret.calculate_fapar(n, cab, car, cbrown, cw, cm, lai, lidfa, hspot, psi, ant, prot, cbc, tts, tto, rsoil = np.full(2101, rsoil_value), psoil = np.full(2101, psoil_value)))

        # Calculate the reflectance by applying the spectral response functions
        reflectance_data.append(np.round(np.sum(tss * srf_land, axis=-1), 5))


    # Add the lists as new columns in the DataFrame
    input_dataframe['canopy_reflectance'] = rho
    input_dataframe['reflectance'] = reflectance_data
    input_dataframe['fAPAR'] = fapar_data
    
    return input_dataframe, rho, reflectance_data, fapar_data