
import numpy as np

EPS_WATER = 80.0               # relative permittivity water
EPS_ZERO = 8.85e-12            # permittivity vacuum
EPS_ZW = EPS_ZERO * EPS_WATER  # often together
E_CHARGE = 1.6e-19             # elementary charge
BOLTZ_T = 1.38e-23 * 298       # Boltzmann constant x temperature
N_AVO = 6.0e23                 # Avogadro's number
ETA_VISC = 0.89e-3             # viscosity water
TWOPI = 2.0 * np.pi
