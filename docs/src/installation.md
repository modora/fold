# Installation

Wheel distributions are provided in this package found in the `dist` folder and the releases tab. Download the target distribution and install using

```bash
pip install <path_to_wheel>
```

# Source

Requirements:

- Poetry

This project is developed using poetry as its project manager. Initialize and build the poetry project using

```bash
poetry install
poetry build
```

The built wheel will be found in the `dist` folder. Install the wheel using

```bash
pip install dist/<name_of_wheel>
```
