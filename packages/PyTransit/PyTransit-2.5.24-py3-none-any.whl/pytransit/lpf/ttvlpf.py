#  PyTransit: fast and easy exoplanet transit modelling in Python.
#  Copyright (C) 2010-2019  Hannu Parviainen
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import seaborn as sb
from matplotlib.pyplot import subplots, setp
from numpy import pi, sign, cos, sqrt, sin, array, arccos, inf, round, int, s_, percentile, concatenate, median, mean, \
    arange, poly1d, polyfit, atleast_2d, repeat

from numba import njit, prange
from .lpf import BaseLPF, map_ldc
from ..models.transitmodel import TransitModel
from ..param.parameter import ParameterSet, PParameter, GParameter
from ..param.parameter import UniformPrior as UP, NormalPrior as NP, GammaPrior as GM
from ..orbits.orbits_py import as_from_rhop, i_from_ba

with_seaborn = True

@njit("f8[:](f8[:], f8, f8, f8, f8[:], i8[:])", cache=False, parallel=False)
def z_circular_ttv(t, p, a, i, tc, tcid):
    cosph = cos(2*pi * (t - tc[tcid]) / p)
    z = sign(cosph) * a * sqrt(1.0 - cosph * cosph * sin(i) ** 2)
    return z


def plot_estimates(x, p, ax, bwidth=0.8):
    ax.bar(x, p[4, :] - p[3, :], bwidth, p[3, :], alpha=0.25, fc='b')
    ax.bar(x, p[2, :] - p[1, :], bwidth, p[1, :], alpha=0.25, fc='b')
    [ax.plot((xx - 0.47 * bwidth, xx + 0.47 * bwidth), (pp[[0, 0]]), 'k') for xx, pp in zip(x, p.T)]

class TTVLPF(BaseLPF):
    """Log posterior function for TTV estimation.

    A log posterior function for TTV estimation. Each light curve represents a single transit, and
    is given a separate free transit centre parameter. The average orbital period and (one) transit
    zero epoch are assumed as known.

    Notes: The number of parameters can grow large with Kepler short-period planets.

    """

    def _init_p_orbit(self):
        """Orbit parameter initialisation.
        """
        porbit = [
            GParameter('p', 'period', 'd', NP(1.0, 1e-5), (0, inf)),
            GParameter('rho', 'stellar_density', 'g/cm^3', UP(0.1, 25.0), (0, inf)),
            GParameter('b', 'impact_parameter', 'R_s', UP(0.0, 1.0), (0, 1))]
        self.ps.add_global_block('orbit', porbit)

        ptc = [GParameter(f'tc_{i}', f'transit_center_{i}', '-', NP(0.0, 0.1), (-inf, inf)) for i in range(self.nlc)]
        self.ps.add_global_block('tc', ptc)
        self._pid_tc = repeat(self.ps.blocks[-1].start, self.nlc)
        self._start_tc = self.ps.blocks[-1].start
        self._sl_tc = self.ps.blocks[-1].slice

    def transit_model(self, pv, copy=True):
        pv = atleast_2d(pv)
        ldc = map_ldc(pv[:, self._sl_ld])
        zero_epoch = pv[:, self._sl_tc] - self._tref
        period = pv[:, 0]
        smaxis = as_from_rhop(pv[:, 1], period)
        inclination = i_from_ba(pv[:, 2], smaxis)
        radius_ratio = sqrt(pv[:, self._sl_k2])
        return self.tm.evaluate(radius_ratio, ldc, zero_epoch, period, smaxis, inclination)

    def _post_initialisation(self):
        super()._post_initialisation()
        self.tm.epids = arange(self.nlc)

