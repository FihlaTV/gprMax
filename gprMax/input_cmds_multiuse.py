# Copyright (C) 2015-2019: The University of Edinburgh
#                 Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.
# Copyright (C) 2015-2018: The University of Edinburgh
#                 Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.

from .cmds_multiple import Waveform
from .cmds_multiple import VoltageSource
from .cmds_multiple import HertzianDipole
from .cmds_multiple import MagneticDipole
from .cmds_multiple import TransmissionLine
from .cmds_multiple import Material
from .cmds_multiple import Snapshot
from .cmds_multiple import AddDebyeDispersion
from .cmds_multiple import AddLorentzDispersion
from .cmds_multiple import AddDrudeDispersion
from .cmds_multiple import SoilPeplinski
from .cmds_multiple import GeometryView
from .cmds_multiple import GeometryObjectsWrite
from .cmds_multiple import PMLCFS
from .cmds_multiple import Rx
from .exceptions import CmdInputError


def process_multicmds(multicmds):
    """
    Checks the validity of command parameters and creates instances of
        classes of parameters.

    Args:
        multicmds (dict): Commands that can have multiple instances in the model.

    Returns:
        scene_objects (list): Holds objects in scene.
    """

    scene_objects = []

    # Waveform definitions
    cmdname = '#waveform'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) != 4:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires exactly four parameters')

            waveform = Waveform(wave_type=tmp[0], amp=float(tmp[1]), freq=float(tmp[2]), id=tmp[3])
            scene_objects.append(waveform)

    # Voltage source
    cmdname = '#voltage_source'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) == 6:
                voltage_source = VoltageSource(polarisation=tmp[0].lower(), p1=(float(tmp[1]), float(tmp[2]), float(tmp[3])), resistance=float(tmp[4]), waveform_id=tmp[5])
            elif len(tmp) == 8:
                voltage_source = VoltageSource(polarisation=tmp[0].lower(), p1=(float(tmp[1]), float(tmp[2]), float(tmp[3])), resistance=float(tmp[4]), waveform_id=tmp[5], start=float(tmp[6]), end=float(tmp[7]))
            else:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires at least six parameters')

            scene_objects.append(voltage_source)

    # Hertzian dipole
    cmdname = '#hertzian_dipole'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) < 5:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires at least five parameters')
            if len(tmp) == 5:
                hertzian_dipole = HertzianDipole(polarisation=tmp[0], p1=(float(tmp[1]), float(tmp[2]), float(tmp[3])), waveform_id=tmp[4])
            elif len(tmp) == 7:
                hertzian_dipole = HertzianDipole(polarisation=tmp[0], p1=(float(tmp[1]), float(tmp[2]), float(tmp[3])), waveform_id=tmp[4], start=float(tmp[5]), end=float(tmp[6]))
            else:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' too many parameters')

            scene_objects.append(hertzian_dipole)

    # Magnetic dipole
    cmdname = '#magnetic_dipole'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) < 5:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires at least five parameters')
            if len(tmp) == 5:
                magnetic_dipole = MagneticDipole(polarisation=tmp[0], p1=(float(tmp[1]), float(tmp[2]), float(tmp[3])), waveform_id=tmp[4])
            elif len(tmp) == 7:
                magnetic_dipole = MagneticDipole(polarisation=tmp[0], p1=(float(tmp[1]), float(tmp[2]), float(tmp[3])), waveform_id=tmp[4], start=float(tmp[5]), end=float(tmp[6]))
            else:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' too many parameters')

            scene_objects.append(magnetic_dipole)

    # Transmission line
    cmdname = '#transmission_line'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) < 6:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires at least six parameters')

            if len(tmp) == 6:
                tl = TransmissionLine(polarisation=tmp[0], p1=(float(tmp[1]), float(tmp[2]), float(tmp[3])), resistance=float(tmp[4]), waveform_id=tmp[5])
            elif len(tmp) == 8:
                tl = TransmissionLine(polarisation=tmp[0], p1=(float(tmp[1]), float(tmp[2]), float(tmp[3])), resistance=float(tmp[4]), waveform_id=tmp[5], start=tmp[6], end=tmp[7])
            else:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' too many parameters')

            scene_objects.append(tl)

    # Receiver
    cmdname = '#rx'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) != 3 and len(tmp) < 5:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' has an incorrect number of parameters')
            if len(tmp) == 3:
                rx = Rx(p1=(float(tmp[0]), float(tmp[1]), float(tmp[2])))
            else:
                rx = Rx(p1=(float(tmp[0]), float(tmp[1]), float(tmp[2])), id=tmp[3], outputs=tmp[4:])
            scene_objects.append(rx)

    # Receiver array
    cmdname = '#rx_array'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) != 9:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires exactly nine parameters')

            p1 = (float(tmp[0]), float(tmp[1]), float(tmp[2]))
            p2 = (float(tmp[3]), float(tmp[4]), float(tmp[5]))
            dl = (float(tmp[6]), float(tmp[7]), float(tmp[8]))

            rx_array = RxArray(p1=p1, p2=p2, dl=dl)
            scene_objects.append(rx_array)

    # Snapshot
    cmdname = '#snapshot'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) != 11:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires exactly eleven parameters')

            p1 = (float(tmp[0]), float(tmp[1]), float(tmp[2]))
            p2 = (float(tmp[3]), float(tmp[4]), float(tmp[5]))
            dl = (float(tmp[6]), float(tmp[7]), float(tmp[8]))
            filename = tmp[10]

            try:
                iterations = int(tmp[9])
                snapshot = Snapshot(p1=p1, p2=p2, dl=dl, iterations=iterations, filename=filename)

            except ValueError:
                time = float(tmp[9])
                snapshot = Snapshot(p1=p1, p2=p2, dl=dl, time=time, filename=filename)

            scene_objects.append(snapshot)

    # Materials
    cmdname = '#material'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) != 5:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires exactly five parameters')

            material = Material(er=float(tmp[0]), se=float(tmp[1]), mr=float(tmp[2]), sm=float(tmp[3]), id=tmp[4])
            scene_objects.append(material)

    cmdname = '#add_dispersion_debye'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()

            if len(tmp) < 4:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires at least four parameters')

            poles = int(tmp[0])
            er_delta = []
            tau = []
            material_ids = tmp[(2 * poles) + 1:len(tmp)]

            for pole in range(1, 2 * poles, 2):
                er_delta.append(float(tmp[pole]))
                tau.append(float(tmp[pole + 1]))

            debye_dispersion = AddDebyeDispersion(pole=poles, er_delta=er_delta, tau=tau, material_ids=material_ids)
            scene_objects.append(debye_dispersion)

    cmdname = '#add_dispersion_lorentz'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()

            if len(tmp) < 5:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires at least five parameters')

            poles = int(tmp[0])
            material_ids = tmp[(3 * poles) + 1:len(tmp)]
            er_delta = []
            tau = []
            alpha = []

            for pole in range(1, 3 * poles, 3):
                er_delta.append(float(tmp[pole]))
                tau.append(float(tmp[pole + 1]))
                alpha.append(float(tmp[pole + 2]))

            lorentz_dispersion = AddLorentzDispersion(poles=poles, material_ids=material_ids, er_delta=er_delta, tau=tau, alpha=alpha)
            scene_objects.append(lorentz_dispersion)

    cmdname = '#add_dispersion_drude'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()

            if len(tmp) < 5:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires at least five parameters')

            poles = int(tmp[0])
            material_ids = tmp[(3 * poles) + 1:len(tmp)]
            tau = []
            alpha = []

            for pole in range(1, 2 * poles, 2):
                tau.append(float(tmp[pole]))
                alpha.append(float(tmp[pole + 1]))

            drude_dispersion = AddDrudeDispersion(poles=poles, material_ids=material_ids, tau=tau, alpha=alpha)
            scene_objects.append(drude_dispersion)

    cmdname = '#soil_peplinski'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()

            if len(tmp) != 7:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires at exactly seven parameters')
            soil = SoilPeplinski(sand_fraction=float(tmp[0]),
                                 clay_fraction=float(tmp[1]),
                                 bulk_density=float(tmp[2]),
                                 sand_density=float(tmp[3]),
                                 water_fraction_lower=float(tmp[4]),
                                 water_fraction_upper=float(tmp[5]),
                                 id=tmp[6])
            scene_objects.append(soil)

    # Geometry views (creates VTK-based geometry files)
    cmdname = '#geometry_view'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) != 11:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires exactly eleven parameters')

            p1 = float(tmp[0]), float(tmp[1]), float(tmp[2])
            p2 = float(tmp[3]), float(tmp[4]), float(tmp[5])
            dl = float(tmp[6]), float(tmp[7]), float(tmp[8])

            geometry_view = GeometryView(p1=p1, p2=p2, dl=dl, filename=tmp[9], output_type=tmp[10])

            scene_objects.append(geometry_view)

    # Geometry object(s) output
    cmdname = '#geometry_objects_write'
    if multicmds[cmdname] is not None:
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) != 7:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires exactly seven parameters')

                p1 = float(tmp[0]), float(tmp[1]), float(tmp[2])
                p2 = float(tmp[3]), float(tmp[4]), float(tmp[5])
                gow = GeometryObjectsWrite(p1=p1, p2=p2, filename=tmp[6])
                scene_objects.append(gow)


    # Complex frequency shifted (CFS) PML parameter
    cmdname = '#pml_cfs'
    if multicmds[cmdname] is not None:
        if len(multicmds[cmdname]) > 2:
            raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' can only be used up to two times, for up to a 2nd order PML')
        for cmdinstance in multicmds[cmdname]:
            tmp = cmdinstance.split()
            if len(tmp) != 12:
                raise CmdInputError("'" + cmdname + ': ' + ' '.join(tmp) + "'" + ' requires exactly twelve parameters')

            pml_cfs = PMLCFS(alphascalingprofile=tmp[0],
                             alphascalingdirection=tmp[1],
                             alphamin=tmp[2],
                             alphamax=tmp[3],
                             kappascalingprofile=tmp[4],
                             kappascalingdirection=tmp[5],
                             kappamin=tmp[6],
                             kappamax=tmp[7],
                             sigmascalingprofile=tmp[8],
                             sigmascalingdirection=tmp[9],
                             sigmamin=tmp[10],
                             sigmamax=tmp[11])

            scene_objects.append(pml_cfs)

    return scene_objects


def process_subgrid_hsg(cmdinstance):

    pass
