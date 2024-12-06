"""various viewer functions for ASE"""
import numpy
import pandas
import pint
from matplotlib import pyplot
from ase import io, visualize
from ase.eos import EquationOfState
from ase.spectrum.band_structure import BandStructure
from ase.dft.kpoints import BandPath
from ase.mep.neb import NEBTools
from ase.vibrations import VibrationsData
from ase.calculators.singlepoint import SinglePointCalculator
from virtmat.language.utilities.errors import RuntimeValueError, RuntimeTypeError
from virtmat.language.utilities.amml import AMMLStructure, Constraint


def show_atoms(atoms, show=True):
    """show atoms object(s)"""
    if show:
        visualize.view(atoms)


def display_amml_structure(obj, show=True):
    """display an atomic structure using ASE"""
    show_atoms(obj.params[0].value.to_ase(), show=show)


def display_amml_trajectory(obj, show=True):
    """display an AMML trajectory using ASE"""
    traj = obj.params[0].value
    if traj.filename:
        images = io.read(traj.filename, index=':')
        show_atoms(images, show=show)


def display_vibration(obj, show=True):
    """display a vibrational normal mode"""
    try:
        assert isinstance(obj.params[0].value, AMMLStructure)
        assert isinstance(obj.params[1].value, pandas.Series)
        assert isinstance(obj.params[1].value[0], pint.Quantity)
        assert isinstance(obj.params[1].value[0].magnitude, numpy.ndarray)
    except AssertionError as err:
        raise RuntimeTypeError(str(err)) from err
    atoms = obj.params[0].value.to_ase()[0]
    hessian = obj.params[1].value[0].to('eV / angstrom**2').magnitude
    mode = -1
    if len(obj.params) > 2:
        tab = obj.params[2].value
        if 'constraints' in tab.columns:
            if not all(isinstance(c, Constraint) for c in tab['constraints'][0]):
                raise RuntimeTypeError('constraints have incorrect type')
            atoms.set_constraint([c.to_ase()[0] for c in tab['constraints'][0]])
        if 'mode' in tab.columns:
            mode = tab['mode'][0].magnitude
    try:
        vib_data = VibrationsData(atoms, hessian)
    except ValueError as err:
        raise RuntimeValueError(str(err)) from err
    n_modes = len(vib_data.get_modes(all_atoms=True))
    mode %= n_modes
    images = []
    for image in vib_data.iter_animated_mode(mode):
        displ = vib_data.get_modes(all_atoms=True)[mode]
        image.calc = SinglePointCalculator(image, forces=displ)
        images.append(image)
    show_atoms(images, show=show)


def display_neb(obj, show=True):
    """display an NEB simulation from provided trajectory"""
    traj = obj.params[0].value
    if traj.filename:
        images = io.read(traj.filename, index=':')
        nebt = NEBTools(images)
        nebt.plot_bands()
        if show:
            pyplot.show()


def display_bs(obj, show=True):
    """display a band structure using ASE"""
    assert issubclass(obj.params[0].type_, pandas.DataFrame)
    assert isinstance(obj.params[0].value, pandas.DataFrame)
    bs_dct = dict(next(obj.params[0].value.iterrows())[1])
    bs_dct['energies'] = bs_dct['energies'].to('eV').magnitude
    bs_dct['reference'] = bs_dct['reference'].to('eV').magnitude
    bp_dct = bs_dct['band_path']
    bp_dct = dict(next(bp_dct.iterrows())[1])
    sp_dct = bp_dct['special_points']
    sp_dct = dict(next(sp_dct.iterrows())[1])
    sp_dct = {k: v.to('angstrom**-1').magnitude for k, v in sp_dct.items()}
    bp_dct['special_points'] = sp_dct
    bp_dct['cell'] = bp_dct['cell'].to('angstrom').magnitude
    bp_dct['kpts'] = bp_dct['kpts'].to('angstrom**-1').magnitude
    band_path = BandPath(**bp_dct)
    bs = BandStructure(band_path, bs_dct['energies'], bs_dct['reference'])
    plt_kwargs = {}
    if len(obj.params) > 1:
        assert issubclass(obj.params[1].type_, pandas.DataFrame)
        assert isinstance(obj.params[1].value, pandas.DataFrame)
        plt_dct = dict(next(obj.params[1].value.iterrows())[1])
        if 'emin' in plt_dct:
            plt_kwargs['emin'] = plt_dct['emin'].to('eV').magnitude
        if 'emax' in plt_dct:
            plt_kwargs['emax'] = plt_dct['emax'].to('eV').magnitude
    bs.plot(show=show, **plt_kwargs)


def display_eos(obj, show=True):
    """display fit to equation of state"""
    volumes = obj.params[0].value
    energies = obj.params[1].value
    eos_kwargs = {}
    if len(obj.params) == 3:
        eos_kwargs['eos'] = obj.params[2].value
    eos_obj = EquationOfState(volumes, energies, **eos_kwargs)
    eos_obj.plot(show=show)
