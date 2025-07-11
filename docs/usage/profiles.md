# Reference guide for population corruption profiles
Crptr can be run with a range of different parameters to configures rates and degrees of corruption. The [example population corruptor](../../src/main/python/populations_crptr/population_corruptor.py) abstracts these into corruption profile, which can be selected in the [config file](../../src/main/python/populations_crptr/config.py) (see [configuration guide](./configuration.md)).

Three pre-existing profile options are provided (as defined in [Tom Dalton's thesis, 7.4.2](https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/26784/Thesis-Tom-Dalton-complete-version.pdf?sequence=4&isAllowed=y)):
- [`profile_a`](../../src/main/python/populations_crptr/example_profiles/profile_a.py) 
- [`profile_b`](../../src/main/python/populations_crptr/example_profiles/profile_b.py)
- [`profile_c`](../../src/main/python/populations_crptr/example_profiles/profile_c.py)

However, you can modify these or add entirely new profiles with ease.

## Profiles
Each profile module contains a single class, defining a series of attributes. This should look similar to:

```python
class CorruptionProfileA:
    PROPORTION_TO_CORRUPT = 0.4
    MAX_MODIFICATIONS_PER_ATTR = 2
    MODIFICATIONS_PER_RECORD = 4
    # ATTR_LEVEL_PROPORTION is defined in Thesis but unused
    ATTR_LEVEL_PROPORTION = 0.75
    RECORD_LEVEL_PROPORTION = 0.25
```

### Attributes
All of the following attributes must be defined in a profile, otherwise errors with occur if usage is attempted:
- **`PROPORTION_TO_CORRUPT`** - the proportion of records in the record-set to corrupt.
    - Value between 0-1
- **`MAX_MODIFICATIONS_PER_ATTR`** - the maximum number of modifications that can be applied to a single attribute on a record.
    - Value $\geq$ 0
- **`MODIFICATIONS_PER_RECORD`** - the number of modifications that are applied to each record being corrupted.
    - Value $\geq$ 0
- **`RECORD_LEVEL_PROPORTION`** -  the proportion of modifications to be applied at the ‘record level’.
    - Value between 0-1

Optional:
- **`ATTR_LEVEL_PROPORTION`** - the proportion of modifications to be applied at the ‘attribute level’.
    - 'Attr_level_proportion' is defined in the profiles in Tom's thesis, so is included for consistency with these, but isn't used at all by the corruptor. 

## Importing new profiles
If you choose to define new Profile modules (following the style described above) and wish to use them with the config file for the example population corruptor, remember to properly import your new profiles at the top of the file. 

This should look similar to:

```python
from populations_crptr.example_profiles.profile_name import CorruptionProfileName
```
