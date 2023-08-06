import yaml
from dielectric.classes.constants import *


# https://stackoverflow.com/questions/16444719/python-numpy-complex-numbers-is-there-a-function-for-polar-to-rectangular-co


def P2R(radii, angles):
    """convert modulus and phase to complex number.
        uses R*exp(j*phi)

    Args:
        radii: modulus of complex number(s)
        angles: phase of complex number(s)

    Returns:
        complex number(s) with input modulus and phase
    """
    return radii * np.exp(1j * angles)


def R2P(z):
    """converts complex number to polar coordinates modulus and phase

    Args:
        z: complex number(s)

    Returns:
       (tuple): (modulus, phase) of input complex number(s)
    """
    return abs(z), np.angle(z)


def P2R2(A, phi):
    """convert modulus and phase to complex number.
        uses A*(cos(phi) + j*sin(phi))

    Args:
        A:    modulus of complex number(s)
        phi:  phase of complex number(s)

    Returns:
        complex number(s) with input modulus and phase

    """
    return A * (np.cos(phi) + np.sin(phi) * 1j)


def cond_part(omega, kappa2, D0, lambda_n2, eps_part, radius, rzeta):
    """

    Args:
        omega:
        kappa2:
        D0:
        lambda_n2:
        eps_part:
        radius:
        rzeta:

    Returns:

    """
    # initialization
    kappa = np.sqrt(kappa2)
    kr = kappa * radius

    # dipole coefficient
    ic_inf, in_inf = dipole_coef(rzeta, kr)

    # conductivity
    K1 = EPS_ZW * D0 * kappa2
    K1_tilde = K1 + 1j * EPS_ZW * omega

    # conductivity interior particle
    K2_tilde = 1j * EPS_ZERO * eps_part * omega

    lambda_n = np.sqrt(lambda_n2)
    delta1 = 2.5 / (1.0 + 2.0 * np.exp(-kr))
    r1 = radius + delta1 / kappa
    delta0 = 1.0 + 3.0 / kr * np.exp(-rzeta / 2.0)
    r0 = radius + delta0 / kappa
    J1 = 1.0 + lambda_n * r0
    J2 = 2.0 + 2.0 * lambda_n * radius + lambda_n2 * np.square(radius)

    mobrien = 2.0 / 3.0 * (EPS_ZW * np.square(BOLTZ_T)) / (D0 * ETA_VISC * np.square(E_CHARGE))
    Us = EPS_ZW * rzeta / ETA_VISC
    KU = -(K1 * mobrien * rzeta * ic_inf) * (
                J1 / (2.0 * J2 * (r0 / radius) ** 3 * np.exp(lambda_n * (r0 - radius))) - 1.0)
    Kper = (2.0 * J1 * K1 * in_inf) / (J2 * np.exp(lambda_n * (r0 - radius)) * (r0 / radius) ** 3)
    Kpar = -K1 * in_inf - (2.0 * J1 * K1 * (np.square(ic_inf) - np.square(in_inf))) / (
                J2 * np.exp(lambda_n * (r0 - radius)) * (r0 / radius) ** 3)

    beta = (K2_tilde - K1_tilde + 2.0 * (Kpar + KU) + Kper) / (
                K2_tilde + 2.0 * K1_tilde + 2.0 * (Kpar * (r0 / radius) ** 3 + KU * (r1 / radius) ** 3) - 2.0 * Kper)

    return K1, K1_tilde, beta


def complex_cond(omega, kappa2, Dp, Dm, zp, zm, el_dist):
    """FULL THEORY, limited to omega << kappa^2 * D0
                    or to be used in the particular case
                    that D1 = D2 (then valid for all frequencies)

    Args:
        omega:       angular velocity array of impedance measurement (rad/s)
        kappa2:      inverse of Debije length squared ((m^-2)
        Dp:          ionic diffusion constant for positive ions (m^2/s)
        Dm:          ionic diffusion constant for negative ions (m^2/s)
        zp:          valence positive ion
        zm:          valence negative ion
        el_dist:     cell electrode distance for flat parallel electrodes

    Returns:
        K (array):         conductivity(omega)
        EPSreal (array):   relative permittivity(omega)
        D_zero:
        Dn:
        Dc:
        lambda_n2 (array): eigenvalue(omega)
        lambda_c2 (array): eigenvalue(omega)
    """
    # initialization
    # kappa = np.sqrt(kappa2)  # inverse of the Debije length

    Dc = np.reciprocal((zp / Dp - zm / Dm) / (zp - zm))
    Dn = np.reciprocal((zp / Dm - zm / Dp) / (zp - zm))
    Dt = np.reciprocal((zp * zm / (zp - zm)) * np.square(1.0 / Dp - 1.0 / Dm) / (zp / Dm - zm / Dp))
    D_zero = np.reciprocal((zp - zm) / (zp * Dp - zm * Dm))

    lambda_c2 = kappa2 + 1j * omega / Dc  # Chassagne 2016 Eq. (24)
    lambda_n2 = 1j * omega / Dn

    D0et = np.reciprocal(Dn / 4.0 * np.square(1.0 / Dp - 1.0 / Dm))
    KDCet = EPS_ZW * kappa2 * D0et * omega / omega

    # see (6.34 in thesis):
    EPS = 1.0 - kappa2 / lambda_c2 * (1.0 - 2.0 / np.sqrt(lambda_c2 * np.square(el_dist)))
    EPS += 1j * omega / (kappa2 * Dt) * (1.0 - 2.0 / np.sqrt(lambda_n2 * np.square(el_dist)))
    EPS = EPS_WATER / EPS

    EPSreal = np.real(EPS)
    K = -np.imag(EPS) * omega * EPS_ZERO

    return K, EPSreal, D_zero, Dn, Dc, lambda_n2, lambda_c2


def complex_cond2(omega, kappa2,
                  diff_plus, diff_minus,
                  z_plus, z_minus,
                  nu_plus, nu_minus,
                  elec_dist):
    """# THEORY ANY FREQUENCY, not to be used when D1 = D2

    Args:
        omega:           angular velocity array of impedance measurement (rad/s)
        kappa2:          inverse of Debije length squared ((m^-2)
        diff_plus:       ionic diffusion constant for positive ions (m^2/s)
        diff_minus:      ionic diffusion constant for negative ions (m^2/s)
        z_plus:          valence positive ion
        z_minus:         valence negative ion
        nu_plus:         stoechiometric coef. ion 1 ("+" ion)
        nu_minus:        stoechiometric coef. ion 2 ("-" ion)
        elec_dist:       cell electrode distance for flat parallel electrodes

    Returns:
        K (array):         conductivity(omega)
        EPSreal (array):   relative permittivity(omega)
        lambda_n2 (array): eigenvalue(omega)
        lambda_c2 (array): eigenvalue(omega)
    """
    # initialization
    # kappa = np.sqrt(kappa2)  # inverse of the Debije length

    help1 = nu_plus * np.square(z_plus) - nu_minus * np.square(z_minus)
    help1 /= nu_plus * np.square(z_plus) + nu_minus * np.square(z_minus)

    re_delta = 1.0 - np.square(omega) * np.square(1.0 / diff_plus - 1.0 / diff_minus) / np.square(kappa2)
    im_delta = 2.0 * omega / kappa2 * help1 * (1.0 / diff_plus - 1.0 / diff_minus)
    delta = np.sqrt(re_delta + 1j * im_delta)

    lambda_n2 = kappa2 / 2.0 + 1j * omega / 2 * (1.0 / diff_plus + 1.0 / diff_minus) - 0.5 * kappa2 * delta
    lambda_c2 = kappa2 / 2.0 + 1j * omega / 2 * (1.0 / diff_plus + 1.0 / diff_minus) + 0.5 * kappa2 * delta
    lambda_c = np.sqrt(lambda_c2)
    lambda_n = np.sqrt(lambda_n2)

    Dc = np.reciprocal((z_plus / diff_plus - z_minus / diff_minus) / (z_plus - z_minus))
    A1 = -(1 + 1j * omega / (kappa2 * Dc) - lambda_n2 / kappa2)
    A2 = (1 + 1j * omega / (kappa2 * Dc) - lambda_c2 / kappa2)

    B = A1 / lambda_c2 * (1.0 - 2.0 / (elec_dist * lambda_c)) + A2 / lambda_n2 * (1.0 - 2.0 / (elec_dist * lambda_n))

    EPS = EPS_WATER / (1.0 + np.square(kappa2) * B / (lambda_c2 - lambda_n2))
    EPSreal = np.real(EPS)
    K = -np.imag(EPS) * omega * EPS_ZERO
    # in time, remove return values lambda
    return K, EPSreal, lambda_n2, lambda_c2


def complex_cond3(omega, kappa2,
                  diff_plus, diff_minus,
                  z_plus, z_minus,
                  nu_plus, nu_minus,
                  elec_dist):
    """# THEORY ANY FREQUENCY, not to be used when D1 = D2

    Args:
        omega:           angular velocity array of impedance measurement (rad/s)
        kappa2:          inverse of Debije length squared ((m^-2)
        diff_plus:       ionic diffusion constant for positive ions (m^2/s)
        diff_minus:      ionic diffusion constant for negative ions (m^2/s)
        z_plus:          valence positive ion
        z_minus:         valence negative ion
        nu_plus:         stoechiometric coef. ion 1 ("+" ion)
        nu_minus:        stoechiometric coef. ion 2 ("-" ion)
        elec_dist:       cell electrode distance for flat parallel electrodes

    Returns:
        K (array):         conductivity(omega)
        EPSreal (array):   relative permittivity(omega)
        lambda_n2 (array): eigenvalue(omega)
        lambda_c2 (array): eigenvalue(omega)
    """
    # initialization
    # kappa = np.sqrt(kappa2)  # inverse of the Debije length

    help1 = nu_plus * np.square(z_plus) - nu_minus * np.square(z_minus)
    help1 /= nu_plus * np.square(z_plus) + nu_minus * np.square(z_minus)

    re_delta = 1.0 - np.square(omega) * np.square(1.0 / diff_plus - 1.0 / diff_minus) / np.square(kappa2)
    im_delta = 2.0 * omega / kappa2 * help1 * (1.0 / diff_plus - 1.0 / diff_minus)
    delta = np.sqrt(re_delta + 1j * im_delta)

    lambda_n2 = kappa2 / 2.0 + 1j * omega / 2 * (1.0 / diff_plus + 1.0 / diff_minus) - 0.5 * kappa2 * delta
    lambda_c2 = kappa2 / 2.0 + 1j * omega / 2 * (1.0 / diff_plus + 1.0 / diff_minus) + 0.5 * kappa2 * delta
    lambda_c = np.sqrt(lambda_c2)
    lambda_n = np.sqrt(lambda_n2)

    Dn = np.reciprocal((z_plus / diff_minus - z_minus / diff_plus) / (z_plus - z_minus))
    Dc = np.reciprocal((z_plus / diff_plus - z_minus / diff_minus) / (z_plus - z_minus))

    C1 = kappa2 / lambda_c2 * 1j * omega / (lambda_n2 * Dn)
    # in line below lambda_c2 is different than in original THEORY3.m ! ?
    CA1 = (kappa2 - lambda_n2) / (lambda_c2 - lambda_n2) + 1j * omega / ((lambda_c2 - lambda_n2) * Dc)
    CA1 /= 1.0 + np.exp(-lambda_c * elec_dist)
    CA1 *= 2.0 / (lambda_c * elec_dist) * kappa2 / lambda_c2

    CA2 = (kappa2 - lambda_c2) / (lambda_c2 - lambda_n2) + 1j * omega / ((lambda_c2 - lambda_n2) * Dc)
    CA2 /= 1.0 + np.exp(-lambda_n * elec_dist)
    CA2 *= 2.0 / (lambda_n * elec_dist) * kappa2 / lambda_n2

    EPS = EPS_WATER / (1.0 - C1 + CA1 + CA2)
    EPSreal = np.real(EPS)
    K = -np.imag(EPS) * omega * EPS_ZERO

    return K, EPSreal


def dipole_coef(rzeta: float, ka: float, method='Chassagne'):
    """ dipole coefficient for a colloidal sphere (approx.)

    Args:
        rzeta: zeta potential in kT/e units
        ka:    kappa * radius

    Returns: ic, in at infinity

    """
    if method == 'Chassagne':
        if rzeta > 1.0:
            # HIGH ZETA POTENTIAL Chassagne 2008, Eq.(55)
            qadim = 2.0 * np.sinh(rzeta / 2.0)
            qadim += 4.0 / ka * np.tanh(rzeta / 4.0)
            qadim -= rzeta / ka
            # surf = (qadim-rzeta/ka) * epsilon_zero * epsilon_water * Boltz_T * np.sqrt(kappa2) / elem_charge
            ic_inf = qadim / ka
            in_inf = -np.abs(ic_inf)  # polydisperse.m
            # in_inf = -ic_inf + (1.0 + 2.0*ka) / 2.0 * np.square(ka) # article_2015.m
        else:
            # LOW ZETA POTENTIAL
            ic_inf = rzeta / ka
            in_inf = 0
    elif method == 'Ohshima':
        qOhshi = (2. * (np.cosh(rzeta) - 1.0 + 8.0 / ka * (
                np.cosh(rzeta / 2.0) - 1.0 + 2.0 / ka * np.log(np.cosh(rzeta / 4.0))))) ^ 0.5 - rzeta / ka
        IcinfOhshi = qOhshi / ka

    elif method == 'Turnhout':
        IcJan = (np.sqrt(2.0 * (ka) ** 2 * (np.cosh(rzeta) - 1.0) + (1.0 + 2.0 * ka) * rzeta ** 2) - rzeta) / (ka) ** 2
        yJan = (1.0 + 2.0 * ka - np.exp(-rzeta) * (ka * (rzeta + 2.0) + rzeta + 1.0)) / (2.0 * ka ** 2)
        yJan2 = (2.0 * ka + 1.0) * (1.0 - np.exp(-2.0 * ka * rzeta / (np.sqrt(np.exp(1) * (2.0 * ka + 1))))) / (
                    2.0 * ka ** 2)

        IninfJan3 = -IcJan + yJan
        IninfJan4 = -IcJan + yJan2
        IninfJan = 0.2 * IninfJan3 + 0.8 * IninfJan4

    return ic_inf, in_inf


def load_config(config_name: str):
    """

    Args:
        config_name:

    Returns:
    """
    with open(config_name) as config_file:
        hp = yaml.safe_load(config_file)  # hp = house_parameters
        return hp
