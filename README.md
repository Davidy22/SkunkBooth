![Image of skukbooth logo](Images\img_with_text.png)

[![GitHub issues](https://img.shields.io/github/issues/Davidy22/scholarlySkunkJam?style=for-the-badge)](https://github.com/Davidy22/scholarlySkunkJam/issues) [![GitHub forks](https://img.shields.io/github/forks/Davidy22/scholarlySkunkJam?style=for-the-badge)](https://github.com/Davidy22/scholarlySkunkJam/network)  [![GitHub stars](https://img.shields.io/github/stars/Davidy22/scholarlySkunkJam?style=for-the-badge)](https://github.com/Davidy22/scholarlySkunkJam/stargazers) [![PyPI](https://img.shields.io/badge/PyPI-GO%20HERE-yellow?style=for-the-badge&logo=pypi)](https://pypi.org/project/skunkbooth/) [![Python](https://img.shields.io/badge/Python-TRUE-brightgreen?style=for-the-badge&logo=python)](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwimlcXOwPHxAhXt4nMBHR1LDBUQFjAAegQICxAD&url=https%3A%2F%2Fwww.python.org%2F&usg=AOvVaw0QREvGsjwHKp2GtoYvs1JH)

# Index
- [Skunkbooth](#skunkbooth)
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
    - [Logs](#logs)

# Skunkbooth
A camera app in terminal. One more reason to stay inside the box you call terminal.
### Idea
  Fill something here plis.

# Usage
### Installation
Install using pip !
```shell
pip install skunkbooth
```

### Run
After installation, use `skunkbooth` command to launch camera.

```shell
skunkbooth
```
### Media location
The photos and videos that you take is present in the following these locations
- MacOS and Linux
```shell
ls ~/skunkbooth/pictures
```

- Windows
```powershell
dir C:\Users\<username>\skunkbooth\pictures
```

# Contributing
[Poetry](https://python-poetry.org/) is used for package management. For setting up your environment, follow along :-

### Install Poetry

- MacOS, Linux or WSL
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

- Windows Powershell
```shell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

### Clone the repo
```shell
git clone https://github.com/Davidy22/scholarlySkunkJam.git
cd scholarlySkunkJam
```
### Activate poetry shell
```shell
poetry shell
```

### Install dev deps
```shell
poetry install
```

### Run the application
```shell
python3 -m skunkbooth.main
```

### Logs
Logs are located in `skunkbooth` folder.
- macOS and Linux
```shell
ls ~/skunkbooth/.logs
```

- Windows
```powershell
dir C:\Users\<username>\skunkbooth\.logs
```
# Acknowledgements
- Davidy22, [Github Profile](https://github.com/Davidy22)
- Trisanu-007,[Github Profile](https://github.com/Trisanu-007)
- dhananjaylatkar, [Github Profile](https://github.com/dhananjaylatkar)
- shriram1998, [Github Profile](https://github.com/shriram1998)
- garuna-m6,, [Github Profile](https://github.com/garuna-m6)
