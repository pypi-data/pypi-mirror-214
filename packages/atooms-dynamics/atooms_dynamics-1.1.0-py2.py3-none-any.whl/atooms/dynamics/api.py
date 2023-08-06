import os
import numpy
import random

from atooms.core.utils import setup_logging, mkdir, rmf
from atooms.models import f90
from atooms.simulation import Simulation
from atooms.trajectory import Trajectory, TrajectoryXYZ, change_species
from atooms.simulation.observers import write_config, write_thermo, Scheduler, target_rmsd

from .newtonian import VelocityVerlet, NosePoincare
from .stochastic import LangevinOverdamped

def _clear_logging():
    import logging
    log = logging.getLogger()
    for h in log.handlers[-2:]:
        log.removeHandler(h)

# TODO: some parts can be refactored via factory / facade?

def md(file_inp, file_out, method='velocity-verlet', model=None,
       T=-1.0, Q=5.0, nsteps=0, checkpoint_interval=0, config_number=0,
       thermo_number=0, thermo_interval=0,
       thermo_fields='steps,temperature,potential energy per particle,pressure,conserved energy,rmsd',
       interval_thermostat=5000, rmsd=-1.0, verbose=False, seed=1,
       skin=0.3, dt=0.002, block='', parallel=False, fmt=None,
       restart=False, dry=False):
    """
    Molecular dynamics simulation
    """

    # Initialize
    random.seed(seed)
    numpy.random.seed(seed)

    # Always log to file
    mkdir(os.path.dirname(file_out))
    if not restart:
        rmf(file_out + '.log')
    setup_logging(level=20, filename=file_out + '.log')
    if verbose:
        setup_logging(level=20)

    # Read initial state
    # We read the last config of file_inp
    with Trajectory(file_inp, fmt=fmt) as th:
        system = th[-1]

    # Setup interaction
    system = change_species(system, 'F')
    if system.number_of_dimensions == 3:
        system.interaction = f90.Interaction(model, helpers='helpers_3d.f90', parallel=parallel)
    else:
        system.interaction = f90.Interaction(model, parallel=parallel)
    system.interaction.neighbor_list = f90.VerletList(skin=skin, parallel=parallel)

    # Simulation backend
    if method == 'velocity-verlet':
        bck = VelocityVerlet(system, timestep=dt)
    elif method == 'nose-poincare':
        bck = NosePoincare(system, timestep=dt, mass=Q, temperature=T)
    elif method == 'massive-thermostat':
        bck = VelocityVerlet(system, timestep=dt)

        def massive_thermostat(sim, T):
            sim.system.temperature = T
    else:
        raise ValueError('unknown method {}'.format(method))

    # Thermostat
    if T > 0:
        system.temperature = T

    # Fix targeting
    if rmsd > 0 and nsteps == 0:
        nsteps = int(1e7)

    # Simulation
    sim = Simulation(bck, output_path=file_out, steps=nsteps,
                     enable_speedometer=True, restart=restart,
                     checkpoint_interval=checkpoint_interval)
    sim.checkpoint_variables = ['species', 'position', 'velocity',
                                'radius', 'position_unfolded']
    sim.trajectory_class = TrajectoryXYZ
    if method == 'massive-thermostat':
        sim.add(massive_thermostat, interval_thermostat, T)

    # Writing trajectory file
    if config_number == 0:
        if len(block) > 0:
            sim.add(write_config, Scheduler(block=[int(_) for _ in block.split(',')]))
    else:
        sim.add(write_config, Scheduler(calls=config_number))

    # Writing thermodynamic data
    thermo_fields = thermo_fields.split(',')
    _func = {'conserved energy': lambda x: x.backend.conserved_energy}
    if thermo_number > 0:
        sim.add(write_thermo, Scheduler(calls=thermo_number), fields=thermo_fields, functions=_func)
    elif thermo_interval > 0:
        sim.add(write_thermo, Scheduler(thermo_interval), fields=thermo_fields, functions=_func)

    # Targeting
    if rmsd > 0:
        sim.add(target_rmsd, Scheduler(5000), rmsd)

    # Run
    if not dry:
        sim.run()
        _clear_logging()

    return sim


def ld(file_inp, file_out, method='overdamped', model=None, T=-1.0,
       nsteps=0, interval_thermostat=5000, config_number=0, rmsd=-1.0,
       thermo_number=0, thermo_interval=0, verbose=False, skin=0.3,
       dt=0.002, friction=1.0, random='PCG', seed=1, block=''):
    """
    Langevin dynamics simulation
    """

    # Random generator
    numpy.random.seed(seed)
    if random in ['PCG', 'PCG64']:
        random = numpy.random.default_rng(seed=seed)
    elif random in ['MT', 'MT19937']:
        random = numpy.random
    else:
        raise ValueError('unknown random generator {}'.format(random))

    mkdir(os.path.dirname(file_out))

    # Always log to file
    setup_logging(level=20, filename=file_out + '.log')
    if verbose:
        setup_logging(level=20)

    # Read initial state
    with Trajectory(file_inp) as th:
        system = th[-1]

    # Setup interaction
    system = change_species(system, 'F')
    system.interaction = f90.Interaction(model)
    system.interaction.neighbor_list = f90.VerletList(skin=skin)

    # BACKEND SPECIFIC
    # Simulation backend
    bck = LangevinOverdamped(system, timestep=dt, friction=friction, temperature=T, random=random)

    # Fix targeting
    if rmsd > 0 and nsteps == 0:
        nsteps = int(1e7)

    # Simulation
    sim = Simulation(bck, output_path=file_out, steps=nsteps, enable_speedometer=True)
    sim.trajectory_class = TrajectoryXYZ

    # Writing
    if config_number == 0:
        if len(block) > 0:
            sim.add(write_config, Scheduler(block=[int(_) for _ in block.split(',')]))
    else:
        sim.add(write_config, Scheduler(calls=config_number))

    if thermo_number > 0:
        sim.add(write_thermo, Scheduler(calls=thermo_number))
    elif thermo_interval > 0:
        sim.add(write_thermo, Scheduler(thermo_interval))

    if rmsd > 0:
        sim.add(target_rmsd, Scheduler(50000), rmsd)

    # Run
    sim.run()
    _clear_logging()

    # Write final configuration
    with Trajectory(file_out + '.chk.xyz', 'w', fmt='xyz') as th:
        th.variables = ['id', 'pos', 'vel']
        th.precision = 12
        th.write(sim.system)

    return sim


if __name__ == '__main__':
    import argh
    argh.dispatch_command(md)
