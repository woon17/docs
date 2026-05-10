# Python Version Management with pyenv

## Check Python Version
To display the current Python version (e.g., Python 3.12.2 or the version set with `pyenv`):

```bash
python --version
```

## List Installed Versions
To list all installed Python versions and see which one is active (marked with `*`):

```bash
pyenv versions
```

## Check Active Python Environment
To check which Python environment is currently active:

```bash
pyenv version
```

## Create a Python Virtual Environment
To create a new Python virtual environment (e.g., `virLanggraphEnv` using Python 3.12.2):

```bash
pyenv virtualenv 3.12.2 virLanggraphEnv
```

## Activate a Python Environment
To activate a specific Python environment (e.g., `virLanggraphEnv`):

```bash
pyenv activate virLanggraphEnv
```

## Set a Local Python Environment (.python-version)
1. The `pyenv local` command sets a directory-specific Python version by creating a `.python-version` file in the current directory.
2. This ensures automatic activation of the specified Python environment whenever the directory is accessed.
3. To set a specific Python environment as the local version (e.g., `virLanggraphEnv`):

```bash
pyenv local virLanggraphEnv
```

## Uninstall a Python Environment
To uninstall a specific Python environment (e.g., `virLanggraphEnv`):
1. Use pyenv virtualenv-delete if you want to be explicit that you're deleting a virtualenv
2. Use pyenv uninstall as the universal command for removing anything pyenv manages
```bash
pyenv virtualenv-delete virLanggraphEnv
pyenv uninstall virLanggraphEnv
```

## Locate Python and Pip
### Check the Shim
The shim is a pointer to the actual `pip` or `python` binary, depending on the currently activated Python environment:

```bash
which pip
which python
```

### Find the Actual Path
To display the actual path to the current Python binary (not just the shim):

```bash
pyenv which pip
pyenv which python
```

## Example Workflow
Activate the environment and verify the `pip` path:

```bash
pyenv activate virLanggraphEnv
pyenv which pip
```
