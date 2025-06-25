# Crptr
Crptr is a software that modifies data based on given probabilities and methods in order to simulate errors and variations occur in real-world data. 

Originally developed by [Ahmad Alsadeeqi](https://github.com/alsediqi) (see [original Crptr repository](https://github.com/alsediqi/crptr-old)). This fork was developed by [Tom Dalton](https://github.com/tomsdalton), to extend the existing application for PhD research to evaluate record linkage methods and algorithms. 

The software is written in Python 3.0 and consists of two main packages:
- `crptr` - the original Crptr application (updated to Python 3.0)
- `populations_crptr` - the extensions for use with population data.

## Basic usage
The Crptr software is versatile and can be configured to any number of different applications, not just synthetic population corruption, but this guide will stick to the basics of population corruption.

The [populations_crptr](./src/main/python/populations_crptr/) package contains corruptor definitions and example configurations for synthetic populations CSVs in the TD format (these can be generated using the [Valipop application](https://github.com/stacs-srg/valipop)).

An example runner for these, [population_corruptor.py](./src/main/python/populations_crptr/population_corruptor.py), is included in the package. This takes the filepath to a records directory (containing "birth_records.csv", "marriage_records.csv" and "death_records.csv") as a CLI parameter. To run this, use the following commands from the root of the repository:

```sh
# Clone the repository and cd into it
git clone https://github.com/stacs-srg/crptr-fork.git
cd crptr-fork

# Creates a virtual environment for running the application, installs the
# requirements, and the Crptr packages in an editable format.
python3 -m venv venv
pip install -r requirements.txt
pip install -e .

# Run the corruptor with example input file
python src/main/python/populations_crptr/population_corruptor.py src/main/resources/example-inputs/TD_300
```

This will produce output similar to:
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

The corrupted records and a log file detailing corruptions made will be output to the results directory specified in the output.

Details such as the results output directory, corruption profiles, and corruptor types (OCR or standard) can be modified using the [config module](src/main/python/populations_crptr/config.py).

## License 
Crptr is published under the [Mozilla Public License](./LICENSE).
