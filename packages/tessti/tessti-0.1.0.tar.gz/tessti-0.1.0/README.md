# TESSTI - The Easiest SLURM Scheduler There Is

Tessti has been made to be the simplest SLURM scheduler possible. <br>
It does not offer much but it works, and is extremely easy to use.


## Getting Started

Suppose you run locally a script named `script.py` in a folder `/some/path/` with some arguments:
```
cd /some/path
python script.py --arg1 value1 --arg2 value2
```

You want to schedule many executions of this script with different values for arguments `arg1` and `arg2`.

Then you only need to create a file called `schedule.py` aside `script.py` with a call to the unique **tessti** function `schedule()`:

```python
from tessti import schedule

schedule(
    ...,
    file='script',
    function='some_function',
    args=dict(arg1=value1, arg2=value2),
    schedule=dict(arg1=[other_value1, other_value2], arg2=[other_value3, other_value4])
)
```

`file`, `function`, and `args` specicy the basic setup you want to replicate, and `schedule` the values that will be used for each job.


## The `schedule` function

The `schedule` function is the only things you'll see from tessti. <br>
Here are descripted all its arguments (some defaults values are made for a specific HPC I use, you should most likely update them):

- SLURM parameters:
    - `working_dir: str`: relative or absolute path of the directory containing the script to schedule. <br>
    *Defaults to '.'*.
    - `jobs_dir: str`: relative or absolute path of the directory in which the SLURM inputs and outputs files will be placed. <br>
    *Defaults to 'jobs'*. 
    - `partition: str`: HPC partition to use. <br>
    *Defaults to 'publigpu'*. 
    - `account: str`: HPC account to use. <br>
    *Defaults to 'miv'*.
    - `node: int`: number of node(s). <br>
    *Defaults to 1*.
    - `task: int`: number of task(s) per node. <br>
    - `cpu: int`: CPU cores per task. <br>
    *Defaults to 1*.
    - `gpu: int`: GPU per node. <br>
    *Defaults to 1*.
    - `ram: int`: RAM memory in Go. <br>
    *Defaults to 16*.
    - `constraint: str`: Any constraint for the nodes requested. <br>
    *Defaults to `'gpua100|gpurtx6000|gpurtx5000|gpuv100'`.*
    - `modules: list[str]`: Modules that must the loaded before executing a job. <br>
    *Defaults to `['python/Anaconda3-2019', 'cuda/cuda-11.8', 'gcc/gcc-11']`.*
    - `commands: list[str]`: Any command that must be executed before executing a job.
    *Defaults to `['source /usr/local/Anaconda/Anaconda3-2019.07/etc/profile.d/conda.sh', 'conda deactivate', 'conda activate torch2cu118']`*.
- Job parameters:
    - `file: str`: name of the file each job must execute. The '.py' extension is not required.
    - `function: str`: name of the function within `file.py` that each job must execute.
    - `args: dict[Any: Any]`: Base args of the function within `file.py` that each job must execute. For each job, exactly one of these args will be overwritten.
- Scheduler parameters:
    - `name: str`: base name for the whole schedule. Created jobs will be named alike `name_arg1=valu1.job`.
    - `schedule: dict[str: Sequence[Any]]`: Sequence of values for each arg that must be set in a separated job.


## A simple example

The relevant code can be found in the [example](example/) folder.

The file `script.py` contains a function `add` with the following signature:
```python
add(a: int, b: int) -> int:
```

The file `schedule.py` is aside the `script.py` and its content is the following:

```python
from tessti import schedule

schedule(
    ...,  # SLURM parameters
    file='script',
    function='add',
    args=dict(a=0, arg2=0),
    schedule=dict(a=[1, 2], b=[4, 5])
)
```

This schedule sets the defaults values for the `add()` function both to 0 through the `arg` keyword argument. <br>
It schedules four jobs: <br>
    - one with `a=1, b=0` (first scheduled value for `a`, default value for `b`). <br>
    - one with `a=2, b=0` (second scheduled value for `a`, default value for `b`). <br>
    - one with `a=0, b=4` (default value for `a`, first scheduled values for `b`). <br>
    - one with `a=0, b=5` (default value for `a`, second scheduled value `b`). <br>