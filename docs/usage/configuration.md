# Configuration guide for the populations corruptor
The [example population corruptor](../../src/main/python/populations_crptr/population_corruptor.py) can be modified in a number of ways (e.g changing corruptor types, profiles, output directories) using the [config module](src/main/python/populations_crptr/config.py). For a more basic usage guide, [see here](population_corruptor_guide.md).

An example (default) configuration of config.py is shown below:

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

## Configuration options
All of these are required and removing any from the configuration file (or leaving them blank) could result in errors:
- **`PROFILE`** specifies a corruption profile (containing a number of parameters) from [populations_crptr.example_profiles](../../src/main/python/populations_crptr/example_profiles/). For more details on corruption profiles, the [corruption profiles guide](./profiles.md). Supported options include (as defined in [Tom Dalton's thesis, 7.4.2](https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/26784/Thesis-Tom-Dalton-complete-version.pdf?sequence=4&isAllowed=y)):
    - [`profile_a`](../../src/main/python/populations_crptr/example_profiles/profile_a.py) 
    - [`profile_b`](../../src/main/python/populations_crptr/example_profiles/profile_b.py)
    - [`profile_c`](../../src/main/python/populations_crptr/example_profiles/profile_c.py)
- **`CORRUPTORS`** specifies a set of corruptors to use from [populations_crptr.example_corruptors](../../src/main/python/populations_crptr/example_corruptors/). Supported options include:
    - [`standard_corruptors_td`](../../src/main/python/populations_crptr/example_corruptors/standard_corruptors_td.py)
    - [`ocr_corruptors_td`](../../src/main/python/populations_crptr/example_corruptors/ocr_corruptors_td.py)
- **`OUTPUT_DIR`** sets path to the root results directory.
- **`PURPOSE`** sets name used to categorise runs. Must be a valid name for files and directories.
    - Results of a specific run are written to `<results_save_location>/<run_purpose>/<timestamp>`
- **`LOOKUP_FILES_DIR`** sets path to directory of lookup-files, defining common variations to use for corruption.
- **`DETERMINISTIC`** sets whether to use a deterministic (pre-defined seed) approach to randomisation.
- **`SEED`** sets seed for use in deterministic runs.