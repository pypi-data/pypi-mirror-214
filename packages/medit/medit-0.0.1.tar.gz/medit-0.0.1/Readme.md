# MEdit - Markup Editor


## Installation

```sh
[<PYTHON> -m] pip[3] install [--upgrade] medit
```


## Usage


## Development & Contribution

```sh
pip3 install -U poetry pre-commit
git clone --recurse-submodules https://projects.om-office.de/frans/pocketrockit.git
cd pocketrockit
pre-commit install
# if you need a specific version of Python inside your dev environment
poetry env use ~/.pyenv/versions/3.10.4/bin/python3
poetry install
```

After modifications, this way a newly built wheel can be checked and installed:

```sh
poetry build
poetry run twine check dist/pocketrockit-0.0.25-py3-none-any.whl
python3 -m pip install --user --upgrade dist/pocketrockit-0.0.25-py3-none-any.whl
```

