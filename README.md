<!-- ![Image of skukbooth logo](Images/skunkbooth_readme.png) -->
<div align="center">
   <img src="Images/skunkbooth_readme.png" alt="Skunkbooth Logo" width="143" height="143">
</div>

[![GitHub issues](https://img.shields.io/github/issues/Davidy22/scholarlySkunkJam?style=for-the-badge)](https://github.com/Davidy22/scholarlySkunkJam/issues) &nbsp;&nbsp; [![GitHub forks](https://img.shields.io/github/forks/Davidy22/scholarlySkunkJam?style=for-the-badge)](https://github.com/Davidy22/scholarlySkunkJam/network) &nbsp;&nbsp; [![GitHub stars](https://img.shields.io/github/stars/Davidy22/scholarlySkunkJam?style=for-the-badge)](https://github.com/Davidy22/scholarlySkunkJam/stargazers)&nbsp;&nbsp; [![PyPI](https://img.shields.io/badge/PyPI-GO%20HERE-yellow?style=for-the-badge&logo=pypi)](https://pypi.org/project/skunkbooth/) &nbsp;&nbsp; [![Python](https://img.shields.io/badge/Python-TRUE-brightgreen?style=for-the-badge&logo=python)](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwimlcXOwPHxAhXt4nMBHR1LDBUQFjAAegQICxAD&url=https%3A%2F%2Fwww.python.org%2F&usg=AOvVaw0QREvGsjwHKp2GtoYvs1JH)

- [Skunkbooth](#skunkbooth)
  - [Why](#why)
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

### Why

Why leave your termial just to capture an image? You can now capture funky images
straight from your beloved box (aka termial).
Don't worry about the OS you are using becase, we support all the modern operating systems.
All you need is `python3`.

# Usage

### Installation

```shell
pip install skunkbooth
```

### Run

After installation, use `skunkbooth` command to launch camera.

```shell
skunkbooth
```

### Media location

The photos and videos that you take are present in the following location

- MacOS and Linux

```shell
ls ~/skunkbooth/pictures
```

- Windows

```powershell
dir C:\Users\<username>\skunkbooth\pictures
```

# Contributing

[Poetry](https://python-poetry.org/) is used for package management.
For setting up your environment, follow along.

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
tail -f ~/skunkbooth/.logs/skunkbooth.log
```

- Windows (powershell)

```powershell
Get-Content C:\Users\<username>\skunkbooth\.logs\skunkbooth.log -Wait
```
