import argparse
import xyz_py as xyzp
import xyz_py.atomic as atomic
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import pathlib
import os
import copy
import subprocess
import pandas as pd
import scipy.constants as constants
import numpy as np
import extto

from . import plotter
from . import extractor
from . import job
from . import utils as ut

# Change matplotlib font size to be larger
mpl.rcParams.update({'font.size': 12})

# Set user specified font name
if os.getenv('orto_fontname'):
    try:
        plt.rcParams['font.family'] = os.getenv('orto_fontname')
    except ValueError:
        ut.cprint('Error in orto_fontname environment variable', 'red')
        sys.exit(1)

_SHOW_CONV = {
    'on': True,
    'save': False,
    'show': True,
    'off': False
}

_SAVE_CONV = {
    'on': True,
    'save': True,
    'show': False,
    'off': False
}


def extract_coords_func(uargs):
    '''
    Wrapper for extract_coords function
    '''

    # Open file and extract coordinates
    labels, coords = extractor.get_coords(
        uargs.output_file,
        coord_type=uargs.type,
        index_style=uargs.index_style
    )

    # Save to new .xyz file
    xyzp.save_xyz(
        f'{uargs.output_file.stem}_coords.xyz',
        labels,
        coords,
        comment=f'Coordinates extracted from {uargs.output_file}'
    )

    return


def gen_job_func(uargs):
    '''
    Wrapper for CLI gen_job call

    Parameters
    ----------
    uargs : argparser object
        User arguments

    Returns
    -------
    None
    '''

    for input_file in uargs.input_files:

        oj = job.OrcaJob(
            input_file
        )

        # Get orca module load command
        orca_args = [
            'orca_load'
        ]

        required = [
            'orca_load'
        ]

        for oarg in orca_args:
            uarg_val = getattr(uargs, oarg)
            if len(uarg_val):
                oarg_val = copy.copy(uarg_val)
            elif os.getenv(f'orto_{oarg}'):
                try:
                    if len(os.getenv(f'orto_{oarg}')):
                        oarg_val = os.getenv(f'orto_{oarg}')
                except ValueError:
                    ut.red_exit(
                        (
                            f'Error in orto_{oarg} environment variable'
                        )
                    )
            elif oarg in required:
                ut.red_exit(
                    (
                        f'Missing orto_{oarg} environment variable or '
                        f'--{oarg} argument'
                    )
                )
            else:
                oarg_val = ''

            if oarg == 'orca_load':
                oarg = 'load'
                if 'module load' not in oarg_val:
                    oarg_val = f'module load {oarg_val}'

            setattr(oj, oarg, oarg_val)

        # Submitter configuration options
        # currently hardcoded for slurm
        config = {}

        # Load number of procs and amount of memory from orca input file
        try:
            n_procs = extractor.NProcsInputExtractor.extract(oj.input_file)[0]
        except extto.DataNotFoundError:
            ut.red_exit(f'Missing Number of processors in {oj.input_file}')
        try:
            maxcore = extractor.MaxCoreInputExtractor.extract(oj.input_file)[0]
        except extto.DataNotFoundError:
            ut.red_exit(f'Missing Max Core Memory in {oj.input_file}')

        # If memory and procs specified as arguments, give warning when
        # these are smaller than the number in the input file
        if uargs.n_procs:
            if n_procs > uargs.n_procs:
                ut.red_exit('Too few processors requested for input file')
            # Use cli value
            config['ntasks_per_node'] = uargs.n_procs
        else:
            # Use orca file value
            config['ntasks_per_node'] = n_procs

        if uargs.memory:
            if uargs.memory * uargs.n_procs < n_procs * maxcore:
                ut.red_exit('Requested too little memory for orca input')
            config['mem_per_cpu'] = uargs.memory
        else:
            # Use orca file value
            config['mem_per_cpu'] = maxcore

        # Get xyz file name and check it exists and is formatted correctly
        try:
            xyz_file = extractor.XYZFileInputExtractor.extract(oj.input_file)
        except extto.DataNotFoundError:
            xyz_file = []

        try:
            xyzline = extractor.XYZInputExtractor.extract(oj.input_file)
        except extto.DataNotFoundError:
            xyzline = []

        if not len(xyz_file) and not len(xyzline):
            ut.red_exit('Error: missing or incorrect *xyzfile or *xyz line in input') # noqa

        if len(xyz_file) > 1 or len(xyzline) > 1 or len(xyz_file + xyzline) > 1: # noqa
            ut.red_exit('Error: multiple *xyzfile or *xyz lines in input. Only one can be present') # noqa

        if len(xyz_file):
            xyz_file = pathlib.Path(xyz_file[0])
            if not xyz_file.is_file():
                ut.red_exit('Error: xyz file specified in input cannot be found') # noqa

            if not uargs.skip_xyz:
                try:
                    xyzp.check_xyz(
                        xyz_file.absolute(),
                        allow_indices=False
                    )
                except xyzp.XYZError as e:
                    ut.red_exit(
                        f'{e}\n Use -sx to skip this check at your peril'
                    )

        # Check if MORead and/or MOInp are present
        try:
            moread = extractor.MOReadExtractor.extract(oj.input_file)
        except extto.DataNotFoundError:
            moread = []
        try:
            moinp = extractor.MOInpExtractor.extract(oj.input_file)
        except extto.DataNotFoundError:
            moinp = []

        # Error if only one word present or if more than one of each word
        if len(moinp) ^ len(moread):
            ut.red_exit('Error: Missing one of MOInp or MORead')
        if len(moinp) + len(moread) > 2:
            ut.red_exit('Error: Multiple MORead and/or MOInp detected')

        if len(moinp):
            # Error if input orbitals have same stem as input file
            moinp = pathlib.Path(moinp[0])
            if moinp.stem == oj.input_file.stem:
                ut.red_exit(
                    'Error: Stem of orbital and input files cannot match'
                )

            # Error if cannot find orbital file
            if not moinp.exists():
                ut.red_exit(f'Error: Cannot find orbital file - {moinp}')

        # Check for simple input line beginning with !
        try:
            extractor.SimpleInputExtractor.extract(oj.input_file)
        except extto.DataNotFoundError:
            ut.red_exit(
                'Error: Missing simple input line (or !) in input file'
            )

        # Add call to orca_2mkl
        if not uargs.no_molden:
            oj.post_orca += 'orca_2mkl {} -molden'.format(oj.input_file.stem)

        # Write job script
        # with submitter configuration options specified
        oj.write_script(True, **config)

        # Submit to queue
        if not uargs.no_sub:
            subprocess.call(
                'cd {}; {} {}; cd ../'.format(
                    oj.input_file.parents[0],
                    oj.Job.SUBMIT_COMMAND,
                    oj.job_file
                    ),
                shell=True
            )

    return


def plot_abs_func(uargs):
    '''
    Wrapper for CLI plot abs call

    Parameters
    ----------
    uargs : argparser object
        User arguments

    Returns
    -------
    None
    '''

    version = extractor.OrcaVersionExtractor.extract(uargs.output_file)

    if not len(version):
        ut.cprint(
            'Warning: Cannot find version number in Orca output file',
            'black_yellowbg'
        )
        version = [6, 0, 0]

    if version[0] < 6:
        if uargs.intensity_type == 'electric':
            all_data = extractor.OldAbsorptionElectricDipoleExtractor.extract(
                uargs.output_file
            )
        else:
            all_data = extractor.OldAbsorptionVelocityDipoleExtractor.extract(
                uargs.output_file
            )
    elif version[0] >= 6:
        if uargs.intensity_type == 'electric':
            all_data = extractor.AbsorptionElectricDipoleExtractor.extract(
                uargs.output_file
            )
        else:
            all_data = extractor.AbsorptionVelocityDipoleExtractor.extract(
                uargs.output_file
            )

    # Plot each section
    for it, data in enumerate(all_data):

        if uargs.x_lim is None:
            if uargs.x_unit == 'wavenumber':
                uargs.x_lim = [0, max(data['energy (cm^-1)'])]
            if uargs.x_unit == 'wavelength':
                # 1 to 2000 nm
                uargs.x_lim = [5000., 10000000.]

        if uargs.x_cut is None:
            iup = -2
            ilow = 0
        else:
            ilow = min(
                [
                    it
                    for it, val in enumerate(data['energy (cm^-1)'])
                    if (val - uargs.x_cut[0]) > 0
                ]
            )
            iup = max(
                [
                    it
                    for it, val in enumerate(data['energy (cm^-1)'])
                    if (uargs.x_cut[1] - val) > 0
                ]
            )

        if len(all_data) > 1:
            save_name = f'absorption_spectrum_section_{it:d}.png'
        else:
            save_name = 'absorption_spectrum_section.png'

        # Plot absorption spectrum
        fig, ax = plotter.plot_abs(
            data['energy (cm^-1)'][ilow: iup+1],
            data['fosc'][ilow: iup+1],
            show=_SHOW_CONV[uargs.plot],
            save=_SAVE_CONV[uargs.plot],
            save_name=save_name,
            x_lim=uargs.x_lim,
            y_lim=uargs.y_lim,
            x_unit=uargs.x_unit,
            linewidth=uargs.linewidth,
            lineshape=uargs.lineshape,
            window_title=f'Absorption Spectrum from {uargs.output_file}',
            show_osc=not uargs.no_osc
        )

        if uargs.x_unit == 'wavenumber':
            ax[0].set_xlim([0, 50000])
        if uargs.x_unit == 'wavelength':
            ax[0].set_xlim([0, 2000])
        plt.show()

    return


def plot_ir_func(uargs):
    '''
    Wrapper for CLI plot_ir call

    Parameters
    ----------
    uargs : argparser object
        User arguments

    Returns
    -------
    None
    '''

    # Extract frequency information
    data = extractor.FrequencyExtractor().extract(uargs.output_file)

    if not len(data):
        ut.red_exit(f'Cannot find frequencies in file {uargs.output_file}')

    data = data[0]

    # Plot uvvis spectrum
    fig, ax = plotter.plot_ir(
        data['energy (cm^-1)'],
        data['t2 (a.u.^2)'],
        linewidth=uargs.linewidth,
        lineshape=uargs.lineshape,
        window_title=f'Infrared Spectrum from {uargs.output_file}',
        show=True
    )

    return


def distort_func(uargs):
    '''
    Distorts molecule along specified normal mode

    Parameters
    ----------
    args : argparser object
        command line arguments

    Returns
    -------
        None

    '''

    # Open file and extract coordinates
    labels, coords = extractor.get_coords(
        uargs.output_file
    )

    # Extract frequency information
    _fext = extractor.FrequencyExtractor()
    _fext(uargs.output_file, process=True)

    coords += uargs.scale * _fext.data[0]['displacements'][:, uargs.mode_number] # noqa

    comment = (
        f'Coordinates from {uargs.output_file} distorted by 1 unit of'
        f' Mode #{uargs.mode_number}'
    )

    labels_nn = xyzp.remove_label_indices(labels)

    xyzp.save_xyz('distorted.xyz', labels_nn, coords, comment=comment)

    return


def print_freq_func(uargs) -> None:

    # Extract frequency information
    _fext = extractor.FrequencyExtractor()
    _fext(uargs.output_file, process=True)

    if not len(_fext.data):
        ut.red_exit(f'Cannot find frequencies in file {uargs.output_file}')

    print('Frequencies (cm^-1)')

    if uargs.num is None:
        uargs.num = len(_fext.data[0]['energy (cm^-1)'])

    for frq in _fext.data[0]['energy (cm^-1)'][:uargs.num]:
        print(f'{frq:.2f}')

    return


def print_natorbs_func(uargs) -> None:
    '''
    Prints Loewdin Natural Orbital contributions

    Parameters
    ----------
    args : argparser object
        command line arguments

    Returns
    -------
        None

    '''

    _ext = extractor.LoewdinCompositionExtractor()

    _ext(uargs.output_file, process=True)

    [contributions, occupations] = _ext.data[0]

    active_ints = [
        it for it, val in enumerate(occupations)
        if 0 < val < 2
    ]

    contributions = [
        {
            key: val
            for key, val in contrib.items()
            if key[4:6].rstrip() in uargs.elements
            and key[7].rstrip() in uargs.shell
            and val > uargs.threshold
        }
        for contrib in contributions
    ]

    if uargs.active:
        print('Contribution to (Natural) Active Orbitals')
        for ai in active_ints:
            if not len(contributions[ai]):
                continue
            print(f'{ai} (Occ={occupations[ai]}):')
            for ao, pc in contributions[ai].items():
                print(f'{ao} : {pc} %')

    else:
        for it, occ in enumerate(occupations):
            if not len(contributions[it]):
                continue
            print(f'{it} (Occ={occ}):')
            for ao, pc in contributions[it].items():
                print(f'{ao} : {pc} %')

    return


def parse_cutoffs(cutoffs):

    if len(cutoffs) % 2:
        raise argparse.ArgumentTypeError('Error, cutoffs should come in pairs')

    for it in range(1, len(cutoffs), 2):
        try:
            float(cutoffs[it])
        except ValueError:
            raise argparse.ArgumentTypeError(
                'Error, second part of cutoff pair should be float'
            )

    parsed = {}

    for it in range(0, len(cutoffs), 2):
        parsed[cutoffs[it].capitalize()] = float(cutoffs[it + 1])

    return parsed


def print_pop_func(uargs) -> None:

    if uargs.flavour in ['loewdin', 'lowdin']:
        data = extractor.LoewdinPopulationExtractor().extract(
            uargs.output_file
        )[0]
    elif uargs.flavour in ['mulliken']:
        data = extractor.MullikenPopulationExtractor().extract(
            uargs.output_file
        )[0]

    charges = data[0]
    spins = data[1]

    # Extract structure
    labels, coords = extractor.get_coords(uargs.output_file)

    labels = xyzp.add_label_indices(
        labels,
        start_index=0,
        style='sequential'
    )

    if uargs.cutoffs:
        cutoffs = parse_cutoffs(uargs.cutoffs)
    else:
        cutoffs = {}

    # Generate dictionary of entities
    entities_dict = xyzp.find_entities(
        labels, coords, adjust_cutoff=cutoffs, non_bond_labels=uargs.no_bond
    )

    # Calculate charge and spin density of each fragment
    ut.cprint(f'{uargs.flavour.capitalize()} Population Analysis', 'cyan')
    ut.cprint('Entity: Charge Spin', 'cyan')
    ut.cprint('-------------------', 'cyan')
    print()
    for entity_name, entities in entities_dict.items():
        for entity in entities:
            _chg = sum([charges[labels[ind]] for ind in entity])
            _spin = sum([spins[labels[ind]] for ind in entity])
            ut.cprint(
                f'{entity_name} : {_chg:.4f}  {_spin:.4f}',
                'cyan'
            )

    return


def plot_susc_func(uargs) -> None:
    '''
    Plots susceptibility data from output file

    Parameters
    ----------
    args : argparser object
        command line arguments

    Returns
    -------
        None

    '''

    # Create extractor
    _ext = extractor.SusceptibilityExtractor()

    # apply to output file
    _ext(uargs.output_file, process=True)

    if not len(_ext.data):
        ut.red_exit(
            f'Cannot find susceptibility output in {uargs.output_file}'
        )

    if not uargs.quiet:
        ut.cprint(
            f'Found {len(_ext.data)} susceptibility blocks in file...',
            'green'
        )
        ut.cprint(
            '... plotting each separately',
            'green'
        )

    # Load experimental data if provided
    if uargs.exp_file is not None:
        exp_data = pd.read_csv(
            uargs.exp_file,
            comment='#',
            skipinitialspace=True
        )

    # Plot data
    data = _ext.data

    # Conversion factors from cm3 K mol^-1 to ...
    convs = {
        'A3 K': 1E24 / constants.Avogadro,
        'A3 mol-1 K': 1E24,
        'cm3 K': 1 / constants.Avogadro,
        'cm3 mol-1 K': 1,
        'emu K': 1 / (4 * constants.pi * constants.Avogadro),
        'emu mol-1 K': 1 / (4 * constants.pi)
    }

    unit_labels = {
        'A3 K': r'\AA^3 \ K',
        'A3 mol-1 K': r'\AA^3 \ mol^{-1} \ K',
        'cm3 K': r'cm^3 \ K',
        'cm3 mol-1 K': r'cm^3 \ mol^{-1} \ K',
        'emu K': r'emu \ K',
        'emu mol-1 K': r'emu \ mol^{-1} \ K',
    }

    for dataframe in data:

        fig, ax = plotter.plot_chit(
            dataframe['chi*T (cm3*K/mol)'] * convs[uargs.susc_units],
            dataframe['Temperature (K)'],
            fields=dataframe['Static Field (Gauss)'],
            window_title=f'Susceptibility from {uargs.output_file}',
            y_unit=unit_labels[uargs.susc_units],
            show=_SHOW_CONV[uargs.plot] if uargs.exp_file is None else False,
            save=_SAVE_CONV[uargs.plot] if uargs.exp_file is None else False,
        )
        if uargs.exp_file is not None:
            ax.plot(
                exp_data['Temperature (K)'],
                exp_data['chi*T (cm3*K/mol)'] * convs[uargs.esusc_units],
                lw=0,
                marker='o',
                fillstyle='none',
                color='k',
                label='Experiment'
            )
            fig.tight_layout()
            ax.legend(frameon=False)

        _ylim = ax.get_ylim()
        ax.set_ylim(0, _ylim[1])

        if _SAVE_CONV[uargs.plot]:
            plt.savefig('chit_vs_t.png', dpi=500)

        if _SHOW_CONV[uargs.plot]:
            plt.show()

    return


def plot_ailft_func(uargs) -> None:
    '''
    Plots AI-LFT orbital energies

    Parameters
    ----------
    args : argparser object
        command line arguments

    Returns
    -------
        None
    '''

    # Create extractor
    _ext = extractor.AILFTOrbEnergyExtractor()

    # apply to output file
    try:
        _ext(uargs.output_file, process=True)
    except ValueError as ve:
        ut.red_exit(str(ve))

    # Plot data
    data = _ext.data

    # Conversion factors from cm-1 to ...
    convs = {
        'cm-1': 1,
        'K': 1E24,
    }

    unit_labels = {
        'cm-1': r'cm^{-1}',
        'K': r'K',
    }

    for dit, dataframe in enumerate(data):

        if len(data) > 1:
            print()
            print(f'Section {dit+1:d}')
            print('---------')

        wfuncs = 100 * np.abs(dataframe['eigenvectors']) ** 2

        for e, wf in zip(dataframe['energies (cm^-1)'], wfuncs.T):
            print(f'E = {e * convs[uargs.units]} {uargs.units}:')
            for it, pc in enumerate(wf):
                if pc > 5.:
                    print(f'{pc:.1f} % {dataframe['orbitals'][it]}')
            if dit == len(wf):
                print('******')
            else:
                print()

        # mm_orbnames = ut.orbname_to_mathmode(dataframe['orbitals'])
        plotter.plot_ailft_orb_energies(
            dataframe['energies (cm^-1)'] * convs[uargs.units],
            groups=uargs.groups,
            occupations=uargs.occupations,
            # labels=mm_orbnames, # convert these to %ages
            window_title=f'AI-LFT orbitals from {uargs.output_file}',
            y_unit=unit_labels[uargs.units],
            show=_SHOW_CONV[uargs.plot],
            save=_SAVE_CONV[uargs.plot],
            save_name=f'{uargs.output_file.stem}_ailft_orbs_set_{dit+1:d}.png'
        )

        plt.show()

    return


def read_args(arg_list=None):
    '''
    Reader for command line arguments. Uses subReaders for individual programs

    Parameters
    ----------
    args : argparser object
        command line arguments

    Returns
    -------
        None

    '''

    description = '''
    A package for working with Orca
    '''

    epilog = '''
    To display options for a specific program, use splash \
    PROGRAMFILETYPE -h
    '''
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    all_subparsers = parser.add_subparsers(dest='prog_grp')

    extract_subprog = all_subparsers.add_parser(
        'extract',
        description='Extract information from Orca file(s)'
    )

    extract_parser = extract_subprog.add_subparsers(dest='extract_grp')

    # If argument list is empty then call help function
    extract_subprog.set_defaults(func=lambda _: extract_subprog.print_help())

    extract_coords = extract_parser.add_parser(
        'coords',
        description='Extracts coordinates from Orca output file'
    )
    extract_coords.set_defaults(func=extract_coords_func)

    extract_coords.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name'
    )

    extract_coords.add_argument(
        '--type',
        type=str,
        help='Which coordinates to extract',
        choices=['opt', 'init'],
        default='init'
    )

    extract_coords.add_argument(
        '--index_style',
        type=str,
        help='Style of indexing used for output atom labels',
        choices=['per_element', 'sequential', 'sequential_orca', 'none'],
        default='per_element'
    )

    gen_subprog = all_subparsers.add_parser(
        'gen',
        description='Generate Orca files'
    )

    gen_parser = gen_subprog.add_subparsers(dest='gen_grp')

    # If argument list is empty then call help function
    gen_subprog.set_defaults(func=lambda _: gen_subprog.print_help())

    gen_job = gen_parser.add_parser(
        'job',
        description=(
            'Generate submission script for orca calculation.\n'
            'Job script should be executed/submitted from its parent directory'
        )
    )
    gen_job.set_defaults(func=gen_job_func)

    gen_job.add_argument(
        'input_files',
        type=str,
        nargs='+',
        help='Orca input file name(s)'
    )

    gen_job.add_argument(
        '--n_procs',
        type=int,
        default=0,
        help=(
            'Number of cores requested in submission system\n'
            ' This does not need to match the orca input, but must not be'
            'less\n. If not specified then value is read from input file.')
    )

    gen_job.add_argument(
        '--memory',
        '-mem',
        type=int,
        default=0,
        help=(
            'Per core memory requested in submission system (megabytes)\n'
            ' This does not need to match the orca input, but must not be'
            'less\n. If not specified then value is read from input file.'
        )
    )

    gen_job.add_argument(
        '--no_sub',
        '-ns',
        action='store_true',
        help=(
            'Disables submission of job to queue'
        )
    )

    gen_job.add_argument(
        '--no_molden',
        '-nm',
        action='store_true',
        help=(
            'Disables orca_2mkl call for molden file generation after calculation' # noqa
        )
    )

    gen_job.add_argument(
        '--skip_xyz',
        '-sx',
        action='store_true',
        help=(
            'Disables xyz file format check'
        )
    )

    gen_job.add_argument(
        '-om',
        '--orca_load',
        type=str,
        default='',
        help='Orca environment module (overrides environment variable)'
    )

    distort = gen_parser.add_parser(
        'distort',
        description='Distorts molecule along given normal mode'
    )
    distort.set_defaults(func=distort_func)

    distort.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name - must contain frequency section'
    )

    distort.add_argument(
        'mode_number',
        type=int,
        help='Mode to distort along - uses orca indexing and starts from zero'
    )

    distort.add_argument(
        '--scale',
        type=float,
        default=1,
        help='Number of units of distortion. Default is 1.'
    )

    plot_subprog = all_subparsers.add_parser(
        'plot',
        description='Plot data from orca file'
    )

    plot_parser = plot_subprog.add_subparsers(dest='plot_grp')

    # If argument list is empty then call help function
    plot_subprog.set_defaults(func=lambda _: plot_subprog.print_help())

    plot_abs = plot_parser.add_parser(
        'abs',
        description='Plots absorption spectrum from CI calculation output'
    )
    plot_abs.set_defaults(func=plot_abs_func)

    plot_abs.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name'
    )

    plot_abs.add_argument(
        '--intensity_type',
        type=str,
        choices=['velocity', 'electric'],
        default='electric',
        help='Type of intensity to plot (orca_mapspc uses electric)'
    )

    plot_abs.add_argument(
        '--linewidth',
        '-lw',
        type=float,
        default=2000,
        help=(
            'Width of signal (FWHM for Gaussian, Width for Lorentzian),'
            ' in Wavenumbers'
        )
    )

    plot_abs.add_argument(
        '--no_osc',
        action='store_true',
        help=(
            'Disables oscillator strength stem plots'
        )
    )

    plot_abs.add_argument(
        '--plot',
        '-p',
        choices=['on', 'show', 'save', 'off'],
        metavar='<str>',
        type=str,
        default='on',
        help=(
            'Controls plot appearance/save \n' # noqa
            ' - \'on\' shows and saves the plots\n'
            ' - \'show\' shows the plots\n'
            ' - \'save\' saves the plots\n'
            ' - \'off\' neither shows nor saves\n'
            'Default: on'
        )
    )

    plot_abs.add_argument(
        '--lineshape',
        '-ls',
        type=str,
        choices=['gaussian', 'lorentzian'],
        default='lorentzian',
        help='Lineshape to use for each signal'
    )

    plot_abs.add_argument(
        '--x_unit',
        type=str,
        choices=['wavenumber', 'wavelength'],
        default='wavenumber',
        help='x units to use for spectrum'
    )

    plot_abs.add_argument(
        '--x_lim',
        type=float,
        nargs=2,
        help='Wavenumber or Wavelength limits of spectrum'
    )

    plot_abs.add_argument(
        '--x_cut',
        type=float,
        nargs=2,
        help='Only include signals between these limits'
    )

    plot_abs.add_argument(
        '--y_lim',
        nargs=2,
        default=['auto', 'auto'],
        help='Epsilon limits of spectrum in cm^-1 mol^-1 L'
    )

    plot_ailft = plot_parser.add_parser(
        'ailft_orbs',
        description='Plots AI-LFT orbital energies from output file'
    )
    plot_ailft.set_defaults(func=plot_ailft_func)

    plot_ailft.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name'
    )

    plot_ailft.add_argument(
        '--groups',
        '-g',
        metavar='<str>',
        nargs='+',
        type=int,
        default=None,
        help=(
            'Group indices for each orbital. e.g. 1 1 1 2 2\n'
            'Controls x-staggering of orbitals'
        )
    )

    plot_ailft.add_argument(
        '--occupations',
        '-o',
        metavar='<str>',
        nargs='+',
        type=int,
        default=None,
        help=(
            'Occupation number of each orbital\n Adds electrons to each orb\n'
            'Must specify occupation of every orbital as 2, 1, -1, or 0'
        )
    )

    plot_ailft.add_argument(
        '--plot',
        '-p',
        choices=['on', 'show', 'save', 'off'],
        metavar='<str>',
        type=str,
        default='on',
        help=(
            'Controls plot appearance/save \n' # noqa
            ' - \'on\' shows and saves the plots\n'
            ' - \'show\' shows the plots\n'
            ' - \'save\' saves the plots\n'
            ' - \'off\' neither shows nor saves\n'
            'Default: on'
        )
    )

    plot_ailft.add_argument(
        '--units',
        '-u',
        choices=[
            'cm-1',
            'K'
        ],
        metavar='<str>',
        type=str,
        default='cm-1',
        help=(
            'Controls energy units of plot\n'
            'Default: cm-1'
        )
    )

    plot_susc = plot_parser.add_parser(
        'susc',
        description='Plots susceptibility data from output file'
    )
    plot_susc.set_defaults(func=plot_susc_func)

    plot_susc.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name'
    )

    plot_susc.add_argument(
        '--susc_units',
        '-su',
        choices=[
            'emu mol-1 K',
            'emu K',
            'cm3 mol-1 K',
            'cm3 K',
            'A3 mol-1 K',
            'A3 K'
        ],
        metavar='<str>',
        type=str,
        default='cm3 mol-1 K',
        help=(
            'Controls susceptibility units of calculated data \n'
            '(wrap with "")'
            'Default: cm3 mol-1 K'
        )
    )

    plot_susc.add_argument(
        '--plot',
        '-p',
        choices=['on', 'show', 'save', 'off'],
        metavar='<str>',
        type=str,
        default='on',
        help=(
            'Controls plot appearance/save \n' # noqa
            ' - \'on\' shows and saves the plots\n'
            ' - \'show\' shows the plots\n'
            ' - \'save\' saves the plots\n'
            ' - \'off\' neither shows nor saves\n'
            'Default: on'
        )
    )

    plot_susc.add_argument(
        '--exp_file',
        type=str,
        help=(
            'Experimental datafile as .csv with two columns:\n'
            '1. "Temperature (K)"\n'
            '2. "chi*T (cm3*K/mol)"\n'
        )
    )

    plot_susc.add_argument(
        '--esusc_units',
        '-esu',
        choices=[
            'emu mol-1 K',
            'emu K',
            'cm3 mol-1 K',
            'cm3 K',
            'A3 mol-1 K',
            'A3 K'
        ],
        metavar='<str>',
        type=str,
        default='cm3 mol-1 K',
        help=(
            'Controls susceptibility units of experimental data \n'
            '(wrap with "")'
            'Default: cm3 mol-1 K'
        )
    )

    plot_susc.add_argument(
        '--quiet',
        action='store_true',
        help='Suppresses text output'
    )

    plot_ir = plot_parser.add_parser(
        'ir',
        description='Plots IR spectrum from frequency calculation output'
    )
    plot_ir.set_defaults(func=plot_ir_func)

    plot_ir.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name'
    )

    plot_ir.add_argument(
        '--plot',
        '-p',
        choices=['on', 'show', 'save', 'off'],
        metavar='<str>',
        type=str,
        default='on',
        help=(
            'Controls plot appearance/save \n' # noqa
            ' - \'on\' shows and saves the plots\n'
            ' - \'show\' shows the plots\n'
            ' - \'save\' saves the plots\n'
            ' - \'off\' neither shows nor saves\n'
            'Default: on'
        )
    )

    plot_ir.add_argument(
        '--linewidth',
        '-lw',
        type=float,
        default=5,
        help=(
            'Width of signal (FWHM for Gaussian, Width for Lorentzian),'
            ' in Wavenumbers'
        )
    )

    plot_ir.add_argument(
        '--lineshape',
        '-ls',
        type=str,
        choices=['gaussian', 'lorentzian'],
        default='lorentzian',
        help='Lineshape to use for each signal'
    )

    print_subprog = all_subparsers.add_parser(
        'print',
        description='Print information from Orca file to screen'
    )

    print_parser = print_subprog.add_subparsers(dest='print_grp')

    # If argument list is empty then call help function
    print_subprog.set_defaults(func=lambda _: print_subprog.print_help())

    print_freq = print_parser.add_parser(
        'freq',
        description='Prints frequencies'
    )
    print_freq.set_defaults(func=print_freq_func)

    print_freq.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name - must contain Frequencies section'
    )

    print_freq.add_argument(
        '-n',
        '--num',
        type=int,
        default=None,
        help='Number of frequencies to print, default is all'
    )

    print_natorbs = print_parser.add_parser(
        'natorbs',
        description='Prints (natural) orbital compositions'
    )
    print_natorbs.set_defaults(func=print_natorbs_func)

    print_natorbs.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name - must contain LOEWDIN ORBITAL-COMPOSITIONS section' # noqa
    )

    print_natorbs.add_argument(
        '-t',
        '--threshold',
        type=float,
        default=1.,
        help='Orbitals with contribution >= threshold are printed. Default: 1'
    )

    print_natorbs.add_argument(
        '-e',
        '--elements',
        type=str,
        default=atomic.elements,
        nargs='+',
        help='Only print contributions from specified element(s) e.g. Ni'
    )

    print_natorbs.add_argument(
        '-s',
        '--shell',
        type=str,
        default=['s', 'p', 'd', 'f', 'g'],
        nargs='+',
        help='Only print contributions from specified shell(s) e.g. d'
    )

    print_natorbs.add_argument(
        '-a',
        '--active',
        action='store_true',
        help=(
            'Only print active orbitals'
        )
    )

    print_pop = print_parser.add_parser(
        'pop',
        description='Prints population analysis, and groups by fragment'
    )
    print_pop.set_defaults(func=print_pop_func)

    print_pop.add_argument(
        'output_file',
        type=pathlib.Path,
        help='Orca output file name - must contain population analysis section' # noqa
    )

    print_pop.add_argument(
        '--flavour',
        '-f',
        type=str,
        choices=['lowdin', 'loewdin', 'mulliken'],
        default='mulliken',
        help='Type of population analysis to print' # noqa
    )

    print_pop.add_argument(
        '--no_bond',
        '-nb',
        type=str,
        default=[],
        nargs='+',
        metavar='symbol',
        help='Atom labels specifying atoms to which no bonds can be formed'
    )

    print_pop.add_argument(
        '--cutoffs',
        type=str,
        nargs='+',
        metavar='symbol number',
        help='Modify cutoff used to define bonds between atoms'
    )

    # If argument list is empty then call help function
    parser.set_defaults(func=lambda _: parser.print_help())

    # select parsing option based on sub-parser
    args = parser.parse_args(arg_list)
    args.func(args)
    return args


def main():
    read_args()
    return
