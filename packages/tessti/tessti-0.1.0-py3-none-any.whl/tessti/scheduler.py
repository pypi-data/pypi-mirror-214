from __future__ import annotations
from typing import Any
import os
import toml
import shutil
from pathlib import Path
from copy import deepcopy


class HPCScheduler:

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.config = toml.load(config_path)
        self.template = toml.load(self.template_path)

    @property
    def parent(self) -> Path:
        return Path(self.config_path).resolve().parent

    @property
    def jobs_dir(self) -> Path:
        return Path(self.parent / self.config['slurm']['jobs_dir']).resolve()

    @property
    def template_path(self) -> Path:
        return self.parent / 'template.toml'

    @property
    def slurm_script_params(self) -> tuple[str | int | list[str]]:
        return (self.config['slurm']['working_dir'],
                self.config['slurm']['jobs_dir'],
                self.config['slurm']['partition'],
                self.config['slurm']['account'],
                self.config['slurm']['node'],
                self.config['slurm']['task'],
                self.config['slurm']['cpu'],
                self.config['slurm']['gpu'],
                self.config['slurm']['ram'],
                self.config['slurm']['constraint'],
                self.config['slurm']['modules'],
                self.config['slurm']['commands'])

    def setup_jobs_env(self) -> None:
        self.jobs_dir.mkdir(exist_ok=True)
        shutil.copyfile(self.template_path, self.jobs_dir / 'template.toml')
        shutil.copyfile(self.config_path,   self.jobs_dir / 'schedule.toml')

    def write_config(self, key: str, value: Any) -> Path:
        config = deepcopy(self.template)
        name = f"{self.config['slurm']['name']}_{key}={value}"
        config['name'] = name
        config['args'][key] = value
        path = (self.jobs_dir / name).with_suffix('.toml')
        with open(path, 'w') as file:
            toml.dump(config, file)
        return path

    def write_configs(self) -> list[Path]:
        config_paths = list()
        for key, values in self.config['parameters'].items():
            for value in values:
                path = self.write_config(key, value)
                config_paths.append(path)
        return config_paths

    def prepare_jobs(self) -> list[Path]:
        self.setup_jobs_env()
        return self.write_configs()

    def write_slurm_job_files(self, config_paths: list[Path]) -> None:
        for config_path in config_paths:
            config = toml.load(config_path)
            job_name = config['name']
            script = get_slurm_script(job_name, *self.slurm_script_params)
            script_path = str(self.jobs_dir / f'{job_name}.job')
            with open(script_path, 'w') as file:
                file.write(script)

    def submit_slurm_schedule(self) -> None:
        jobs_paths = list(self.jobs_dir.glob('*.job'))
        for path in jobs_paths:
            os.system(f'chmod +x {path}')
            os.system(f'sbatch {path}')

    def run(self) -> None:
        config_paths = self.prepare_jobs()
        self.write_slurm_job_files(config_paths)
        self.submit_slurm_schedule()


# _______________________________________________________________________________________________ #


def get_slurm_script(
    job_name: str,
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
) -> str:
    working_dir = str(Path(working_dir).resolve())
    stem = Path(jobs_dir) / job_name
    config, output = f'{stem}.toml', f'{stem}.out'
    slurm = f"""#! /bin/bash


# +------------------------------------------------------------------------------------+ #
# |                                  SLURM PARAMETERS                                  | #
# +------------------------------------------------------------------------------------+ #

#SBATCH -p {partition} -A {account}
#SBATCH -N {node}
#SBATCH -n {task}
#SBATCH -c {cpu}
#SBATCH --gres=gpu:{gpu}
#SBATCH --mem={ram}G
#SBATCH --constraint="{constraint}"
#SBATCH -o {output}

"""
    env = """
# +------------------------------------------------------------------------------------+ #
# |                                ENVIRONNEMENT SET UP                                | #
# +------------------------------------------------------------------------------------+ #

"""
    for module in modules:
        env += f"module load {module}\n"
    for command in commands:
        env += f"{command}\n"
    env += f"cd {working_dir}\n\n"
    run = f"""
# +------------------------------------------------------------------------------------+ #
# |                                 RUN PYTHON SCRIPT                                  | #
# +------------------------------------------------------------------------------------+ #

python schedule.py --config {config}
"""
    return slurm + env + run
