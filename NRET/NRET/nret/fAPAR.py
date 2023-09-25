#@ author : Mahmoud H. Ahmed
#!/usr/bin/env python
import numpy as np
from nret import spectral_lib
from .FourSAIL import foursail
from .prospect_d import run_prospect
from .sail_model import run_prosail


def calculate_fapar(
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
    ant=0.0,
    prot=0.0,
    cbc=0.0,
    alpha=40.0,
    prospect_version="PRO",
    typelidf=2,
    lidfb=0.0,
    rsoil0=None,
    rsoil=None,
    psoil=None,
    soil_spectrum1=None,
    soil_spectrum2=None,
    fapar_wl=slice(0, 300),
):
    """
       fAPAR is the fraction of incoming solar radiation that is absorbed by the green 
       vegitation in the spectral range from 400 to 700 nm.

       Assuming constant soil reflectance, fAPAR includes the direct absorption of radiation
       by the canopy a1(λ), and the part that is reflected by the background and absorbed by
       the vegitation a2(λ).

       Therefore, the total energy fraction absorbed by the green canopy is:

       a(λ) = a1(λ) + a2(λ)                where λ is the wavelength 



    This is a function to calculate fAPAR . You can select the 
    spectral range of fAPAR using the slice notation. By default 
    fAPAR is calculated between 400 and 700 nm.


    Parameters
    -----------
    n: float
        The number of leaf layers. Unitless [-].
    cab: float
        The chlorophyll a+b concentration. [g cm^{-2}].
    car: float
        Carotenoid concentration.  [g cm^{-2}].
    cbrown: float
        The brown/senescent pigment. Unitless [-], often between 0 and 1
        but the literature on it is wide ranging!
    cw: float
        Equivalent leaf water. [cm]
    cm: float
        Dry matter [g cm^{-2}]
    lai: float
        leaf area index
    lidfa: float
        a parameter for leaf angle distribution. If ``typliedf``=2, average
        leaf inclination angle.
    tts: float
        Solar zenith angle
    tto: float
        Sensor zenith angle
    psi: float
        Relative sensor-solar azimuth angle ( saa - vaa )
    ant: float, optional
        Anthocyanins content. Used in Prospect-D and Prospect-PRO [g cm^{-2}]
    prot: float, optional
        Protein content. Used in Prospect-PRO. [g cm^{-2}]
    cbc: float, optional
        Carbon based constituents. Used in Prospect-PRO. [g cm^{-2}]
    alpha: float
        The alpha angle (in degrees) used in the surface scattering
        calculations. By default it_s set to 40 degrees.
    prospect_version: str
        Which PROSPECT version to use. We have "5", "D" and "PRO"
    typelidf: int, optional
        The type of leaf angle distribution function to use. By default, is set
        to 2.
    lidfb: float, optional
        b parameter for leaf angle distribution. If ``typelidf``=2, ignored
    rsoil0: float, optional
        The soil reflectance spectrum
    rsoil: float, optional
        Soil scalar 1 (brightness)
    psoil: float, optional
        Soil scalar 2 (moisture)
    soil_spectrum1: 2101-element array
        First component of the soil spectrum
    soil_spectrum2: 2101-element array
        Second component of the soil spectrum
    fapar_wl: slice
        Wavelengths to use for fAPAR calculation. Selects slice positions for
        the interval 400-2500 (inclusive). By default, use `slice(0,300)`,
        equivalent to 400 to 700 nm.

    Returns
    --------
    fAPAR

    References
    ----------
    .. [Fan et. al 2014] Fan W, Liu Y, Xu X, Chen G, Zhang B (2014) A New FAPAR Analytical
      Model Based on the Law of Energy Conservation: A Case Study in China. Selected Topics
      in Applied Earth Observations and Remote Sensing, IEEE Journal of 7: 3945-3955 DOI 10.1109/JSTARS.2014.2325673.


    """
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
        alpha=alpha,
        prospect_version=prospect_version,
        typelidf=typelidf,
        lidfb=lidfb,
        factor="ALLALL",
        rsoil0=rsoil0,
        rsoil=rsoil,
        psoil=psoil,
        soil_spectrum1=soil_spectrum1,
        soil_spectrum2=soil_spectrum2,
    )

    """
    es and ed:
    These variables represent the solar irradiance spectra for direct and diffuse illumination, respectively.
    """
    es = spectral_lib.light.es
    ed = spectral_lib.light.ed

    """
    The SAIL parameter skyl controls the ratio of diffuse to total solar radiation incident on
    the target. It is calculated in dependence of the sun zenith angle according to the approach
    of François et al. (2002) which considers an average state of atmospheric conditions 
    aligned to mid-latitudes:
    
    """
    
    skyl = ( 0.847 - 1.61 * np.sin(np.deg2rad(90 - tts))
        + 1.04 * np.sin(np.deg2rad(90 - tts)) * np.sin(np.deg2rad(90 - tts))
    )

    """
    edir represents the direct component of solar irradiance reaching the canopy,
    and edif represents the diffuse component. 
    """
    edir = (1 - skyl) * es
    edif = skyl * ed
    
    # Interaction with the soil
    dn = 1.0 - rsoil * rdd
    try:
        dn[dn < 1e-36] = 1e-36
    except TypeError:
        dn = max(1e-36, dn)

    # fAPAR calculations
    
    alfa_s = 1.0 - tss - tsd - rsd  # direct flux
    alfa_d = 1.0 - tdd - rdd  # diffuse
    alfa_sx = alfa_s + (rsoil * (tss + tsd) / dn) * alfa_d
    alfa_dx = alfa_d + ((tdd * rsoil) / dn) * alfa_d
    top = alfa_sx * edir + alfa_dx * edif
    fAPAR = np.sum((top[fapar_wl])) / np.sum((edir + edif)[fapar_wl])


    return fAPAR

