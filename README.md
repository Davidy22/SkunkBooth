- [Photobooth](#photobooth)
- [Usage](#usage)
      - [Installation](#installation)
      - [Run](#run)
      - [Media location](#media-location)
- [Contributing](#contributing)
      - [Install Poetry](#install-poetry)
      - [Clone the repo](#clone-the-repo)
      - [Activate poetry shell](#activate-poetry-shell)
      - [Install dev deps](#install-dev-deps)
      - [Run the application](#run-the-application)
# Photobooth

A camera app in terminal. One more reason to stay inside terminal.

# Usage
#### Installation
```shell
pip install skunkbooth
```

#### Run
After installation, use `skunkbooth` command to launch camera.

```shell
skunkbooth
```
#### Media location

- macOS and Linux
```shell
cd ~/Pictures/skunkbooth
```

- Windows
```shell
TBD
```

# Contributing
[Poetry](https://python-poetry.org/) is used for package management.

#### Install Poetry

- macOS, Linux or WSL
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

- Windows Powershell
```shell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

#### Clone the repo
```shell
git clone https://github.com/Davidy22/scholarlySkunkJam.git
cd scholarlySkunkJam
```
#### Activate poetry shell
```shell
poetry shell
```

#### Install dev deps
```shell
poetry install
```

#### Run the application
```shell
python3 -m skunkbooth.main
```
