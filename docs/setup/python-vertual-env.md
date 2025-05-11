# Python Version Management with pyenv

## 1. Check Python Version
To display the current Python version (e.g., Python 3.12.2 or the version set with `pyenv`):

```bash
python --version
```

## 2. List Installed Versions
To list all installed Python versions and see which one is active (marked with `*`):

```bash
pyenv versions
```

## 3. Check Active Python Environment
To check which Python environment is currently active:

```bash
pyenv version
```

## 4. Create a Python Virtual Environment
To create a new Python virtual environment (e.g., `virLanggraphEnv` using Python 3.12.2):

```bash
pyenv virtualenv 3.12.2 virLanggraphEnv
```

## 5. Activate a Python Environment
To activate a specific Python environment (e.g., `virLanggraphEnv`):

```bash
pyenv activate virLanggraphEnv
```

## 6. Set a Local Python Environment (.python-version)
1. The `pyenv local` command sets a directory-specific Python version by creating a `.python-version` file in the current directory.
2. This ensures automatic activation of the specified Python environment whenever the directory is accessed.
3. To set a specific Python environment as the local version (e.g., `virLanggraphEnv`):

```bash
pyenv local virLanggraphEnv
```

## 7. Uninstall a Python Environment
To uninstall a specific Python environment (e.g., `virLanggraphEnv`):

```bash
pyenv uninstall virLanggraphEnv
```

## 8. Locate Python and Pip
### 8.1 Check the Shim
The shim is a pointer to the actual `pip` or `python` binary, depending on the currently activated Python environment:

```bash
which pip
which python
```

### 8.2 Find the Actual Path
To display the actual path to the current Python binary (not just the shim):

```bash
pyenv which pip
pyenv which python
```

## 9. Example Workflow
Activate the environment and verify the `pip` path:

```bash
pyenv activate virLanggraphEnv
pyenv which pip
```
