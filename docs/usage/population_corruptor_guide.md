# Basic population corruption with crptr guide
The [populations_crptr](./src/main/python/populations_crptr/) package contains corruptor definitions and example configurations for synthetic populations CSVs in the TD format (these can be generated using the [Valipop application](https://github.com/stacs-srg/valipop)).

An example runner for these, [population_corruptor.py](../../src/main/python/populations_crptr/population_corruptor.py), is included in the package. This takes the filepath to a records directory (containing "birth_records.csv", "marriage_records.csv" and "death_records.csv") as a CLI parameter and corrupts them (according to a number of options set in [config.py](../../src/main/python/populations_crptr/config.py)).

The following guide will demonstrate how to install, use and configure this application.

## 1. Prerequisites
Before we begin, you will need to have installed the following tools on your system for this walkthrough:
- [Git](https://git-scm.com/)
- [Python 3](https://www.python.org/)

## 2. Installation
Before running the corruptor, you will need to install the repository and setup a virtual environment to run it in.

### 2.1 Installing the repository
To run the corruptor, you must first install the `crptr` repository, using the following command:
```sh
# In a terminal (Windows/macOS/Linux)
git clone https://github.com/stacs-srg/crptr-fork.git
```

### 2.2. Setting up the virtual environment
To setup the virtual environment and install the relevant requirements, navigate into the previously-installed repository (using `cd crptr-fork`) and run the following commands:
```sh
# In a terminal (Windows/macOS/Linux)
python3 -m venv venv
```
```sh
# In a terminal (macOS/Linux)
source venv/bin/activate

# In a terminal (Windows)
venv\Scripts\activate
```
```sh
# In a terminal (Windows/macOS/Linux)
pip install -r requirements.txt
pip install -e .
```

To exit the venv, simply run the command: `deactivate`.

For all subsequent uses of the venv, after the intial setup, only `source venv/bin/activate` is required.

### 2.3. Verifying installation
To verify that everything has been installed correctly, run the following command in the venv:

```sh
# In a terminal (Windows/MacOs/Linux)
python -m populations_crptr.population_corruptor
```

Which should output the following message:
```txt
Usage: python population_corruptor.py <filepath>
```

### 3. Execution
To run the corruptor with the example dataset, run the following command in the venv:
```sh
# In a terminal (Windows/MacOs/Linux)
python -m populations_crptr.population_corruptor src/main/resources/example-inputs/TD_300
```

By default, assuming [config.py](../../src/main/python/populations_crptr/config.py) is unmodified, will run a standard corruptor non-deterministically.
This should be reasonably quick, given the small size of the example dataset, and produce output similar to:

```txt
Running crptr for src/main/resources/example-inputs/TD_300
2025/06/25 12-04-24.811 :: Corrupting src/main/resources/example-inputs/TD_300/birth_records.csv...
Elapsed time: 00-00-00-160
2025/06/25 12-04-24.971 :: Corrupting src/main/resources/example-inputs/TD_300/marriage_records.csv...
Elapsed time: 00-00-00-120
2025/06/25 12-04-25.091 :: Corrupting src/main/resources/example-inputs/TD_300/death_records.csv...
Elapsed time: 00-00-00-154
Results output to results/default/2025-06-25T12-04-24-809
```

A `results/` will now exist at the root of the repository, and the results for the specific run will be located in a directory named similar to:

```txt
results/default/2025-06-25T12-04-24-809
```

The specific path can also be seen at the end of the terminal output.

### 3.1. Results
Within the results directory for the run, you will find a `records/` directory (containing the newly corrupted version of "birth_records.csv", "marriage_records.csv" and "death_records.csv") and a log file, which will be named similar to:

```txt
default2025-06-25T12-04-24-809.log
```

This log-file provides details on the configurations used for the run, including the corruption probability parameters and the randomisation seed, aswell as the individual corruptions made. For more information on this file, see the [log files documentation](./log_files.md).

### 3.2. Configuration
The above guide uses the default configuration for the corruptor, but this can be modified in a number of ways (e.g changing corruptor types, profiles, output directories) using the [config module](src/main/python/populations_crptr/config.py). An example (default) configuration of config.py is shown below:

```python
class Config:
    PROFILE = CorruptionProfileA
    CORRUPTORS = StandardCorruptorsTD
    OUTPUT_DIR = "results"
    PURPOSE = "default"
    LOOKUP_FILES_DIR = "src/main/resources/lookup-files"
    DETERMINISTIC = False
    SEED = None
```

For details on how to configure the corruptor, see the [configuration guide](configuration_guide.md). 
