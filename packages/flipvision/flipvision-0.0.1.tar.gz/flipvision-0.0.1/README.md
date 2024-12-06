# WT9011DCL-data-parsing

## Installation

1. Create python virtual environment e.g. venv:
```
python3 -m venv venv
source venv/bin/activate
```

2. If you want to just use the package:
```
pip install .
```

For contributors:
```
pip install -e ".[lint]"
pre-commit
```
The -e option is for installing in editable mode - meaning changes in the code under development will be immediately visible when using the package.

To run the package just type:
```
flipvision
```

To listen for imu data type:
```
flipvision -l
```


## Enter nix devshell

cd into the project directory

```
nix develop
```

This will create venv and install dependencies on the first run.
Exit the shell with `exit` command or ctrl-d

## Bleak
[Examples](https://github.com/hbldh/bleak/tree/master/examples)
