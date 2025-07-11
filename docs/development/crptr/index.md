# Development with Crptr
The original Crptr library, as developed by [Ahmad Alsadeeqi](https://github.com/alsediqi) is a versatile tool which can be configured to corrupt any given data-set.

## Overview of structure
The following is a brief overview of the structure of the `Crptr` package, to get you started in your development.

### [`crptr.crptr.py`](../../../src/main/python/crptr/crptr.py)
This module is the main class for the *crptr* tool and contains the main functionality for corrupting datasets. 

The `corrupt_records` function takes a python dictionary of records (of \<id, record\> pairs) as a parameter and corrupts them based on a number of configuration parameters (which are provided when instantiating the `Crptr` object). These parameters are:
- `number_of_mod_records` The number of modified (corrupted) records that are to be generated. 
- `number_of_org_records` The original number of records.
- `attribute_name_list` List of attributes (fields) in dataset.
- `max_num_dup_per_rec` Maximum number of modified (corrupted) records that can be generated for a single original record.
- `num_dup_dist` Probability distribution used to create the duplicate records for one original record ('uniform', 'poisson', or 'zipf')
- `max_num_mod_per_attr` The maximum number of modifications to be applied on a single attribute.
- `num_mod_per_rec` The number of modification that are to be applied to a record
- `attr_mod_prob_dict` Dictionary contains probabilities that determine how likely an attribute is selected for random modification (corruption).
    - Keys are attribute names and values are probability values, which sum to 1.0.
- `attr_mod_data_dict` A dictionary which, for each attribute that is to be modified, contains a list which of pairs of probabilities and corruptor objects (i.e. subclasses of `corruptValues.base`).


### [`crptr.corrupt_records`](../../../src/main/python/crptr/corrupt_records/)
This package contains a base-class defining a generic corruptor class for **corrupting whole records**, and a number of implementations of this for different sorts of corruption (such as clearing records, duplicating, swapping attributes).

### [`crptr.corrupt_values`](../../../src/main/python/crptr/corrupt_values/)
This package contains a base-class defining a generic corruptor class for **corrupting individual attributes** and a number of implementations of this for different sorts of corruption (such as phonetic errors, keyboard errors, missing values, and transcription errors such as unknown characters).

### [`crptr.position_functions.py`](../../../src/main/python/crptr/position_functions.py)
A module containing common randomisation functions for selecting a position in a string to modify/corrupt.

### [`crptr.base_functions.py`](../../../src/main/python/crptr/base_functions.py)
A module containing functions for checking the type and range of variables, and validate parameters.
