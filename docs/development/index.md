# Developing with Crptr
The [Crptr repository](https://github.com/stacs-srg/crptr-fork) consists of two packages, both of which can be easily built-upon/modified.

## Packages
### `crptr`
This package contains the base Crptr software which modifies data based on given probabilities and methods in order to simulate errors and variations occur in real-world data.

[Read more about developing `Crptr` here](./crptr/index.md).

### `populations_crptr`
This package contains implementations/extensions of the `crptr` package for the purpose of corrupting synthetic populations in the TD format (which can be generated using the [Valipop application](https://github.com/stacs-srg/valipop)).

[Read more about developing `populations_crptr` here](./populations_crptr/index.md).

## Virtual environment
When developing with Crptr, ensure that your virtual environment is set-up correctly, with both packages install in **editable** mode (using the `-e` flag). 

To setup the venv properly, run the following commands:
```sh
# Create the venv
python3 -m venv venv
# Activate the venv
source venv/bin/activate
# Install requirements
pip install -r requirements.txt
# Install packages ('crptr' and 'populations_crptr' in editable mode)
pip install -e .
```

To exit the venv, simply run the command: `deactivate`.

For all subsequent uses of the venv, after the intial setup, only `source venv/bin/activate` is required.