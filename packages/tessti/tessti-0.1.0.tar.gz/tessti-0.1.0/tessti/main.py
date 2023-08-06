from __future__ import annotations
from typing import Any, Sequence
import toml
from pathlib import Path
from argparse import ArgumentParser
from .scheduler import HPCScheduler


def parse_config_path_arg() -> str | None:
    parser = ArgumentParser('Schedule multiple jobs or run a single job.')
    # if config is specified, launch single run, else, schedule multi runs
    parser.add_argument('--config', type=str, default=None)
    return parser.parse_args().config


def run(config_path: str | Path) -> None:
    config = toml.load(config_path)
    file = Path(config['run']['file'])
    if file.suffix == '.py':
        file = file.with_suffix('')
    function = config['run']['function']
    args = config['args']
    exec(f'from {file} import {function}')
    eval(f'{function}(**{args})')


def create_configs(
    *,
    # ___________________________________ SLURM #
    working_dir: str,
    jobs_dir: str,
    partition: str,
    account: str,
    node: int,
    task: int,
    cpu: int,
    gpu: int,
    ram: int,
    constraint: str,
    modules: list[str],
    commands: list[str],
    # _____________________________________ JOB #
    file: str,
    function: str,
    args: dict[Any: Any] = dict(),
    # ________________________________ SCHEDULE #
    name: str,
    schedule: dict[str: Sequence[Any]] = dict(),
) -> None:
    # template config
    template_config = dict()
    template_config['run'] = dict(file=file, function=function)
    template_config['args'] = args
    with open((Path(working_dir) / 'template').with_suffix('.toml'), 'w') as config_file:
        toml.dump(template_config, config_file)
    # schedule config
    schedule_config = dict()
    schedule_config['slurm'] = dict(name=name, working_dir=working_dir, jobs_dir=jobs_dir,
                                    partition=partition, account=account,
                                    node=node, task=task, cpu=cpu, gpu=gpu, ram=ram,
                                    constraint=constraint, modules=modules, commands=commands)
    schedule_config['parameters'] = dict()
    for key, values in schedule.items():
        schedule_config['parameters'][key] = values
    with open((Path(working_dir) / 'schedule').with_suffix('.toml'), 'w') as config_file:
        toml.dump(schedule_config, config_file)


def schedule(
    *,
    # ___________________________________ SLURM #
    working_dir: str = '.',
    jobs_dir: str = 'jobs',
    partition: str = 'publicgpu',
    account: str = 'miv',
    node: int = 1,
    task: int = 1,
    cpu: int = 1,
    gpu: int = 1,
    ram: int = 16,
    constraint: str = 'gpua100|gpurtx6000|gpurtx5000|gpuv100',
    modules: list[str] = ['python/Anaconda3-2019', 'cuda/cuda-11.8', 'gcc/gcc-11'],
    commands: list[str] = ['source /usr/local/Anaconda/Anaconda3-2019.07/etc/profile.d/conda.sh',
                           'conda deactivate',
                           'conda activate torch2cu118'],
    # _____________________________________ JOB #
    file: str,
    function: str,
    args: dict[Any: Any] = dict(),
    # ________________________________ SCHEDULE #
    name: str,
    schedule: dict[str: Sequence[Any]] = dict(),
) -> None:
    config_path = parse_config_path_arg()
    if config_path is not None:
        run(config_path)
        return
    params = locals()
    params.pop('config_path')
    create_configs(**params)
    schedule_config_path = Path(working_dir).resolve() / 'schedule.toml'
    HPCScheduler(config_path=schedule_config_path).run()
