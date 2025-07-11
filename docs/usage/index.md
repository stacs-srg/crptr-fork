# Crptr usage instructions
Both of the crptr packages are incredibly versatile and contain a number of highly-customisable tools, which can be adjusted to a number of use-cases. For more details on how to utilise and develop applications with these, see the [development guides](../development/index.md).

## Populations corrupter 
The [populations_crptr](./src/main/python/populations_crptr/) package contains corruptor definitions and example configurations for synthetic populations CSVs in the TD format (these can be generated using the [Valipop application](https://github.com/stacs-srg/valipop)).

An example runner for these, [population_corruptor.py](./src/main/python/populations_crptr/population_corruptor.py), is also included in the package.

For detailed usage information about the `populations_crptr` package, see:
- **[Population corruptor usage guide](population_corruptor_guide.md)**
    - Contains details on how to use the example runner to corrupt synthetic populations.
- **[Population corruptor configuration guide](configuration.md)**
    - Details configuration options for the example runnner.
- **[Log files explanation](log_files.md)**
    - An explanation of the log-files output by the example runner and the provided corruptor definitions.
- **[Corruption profiles guide](profiles.md)**
    - A guide to corruption profiles (used by the example runner) and tuning corruption parameters.
    