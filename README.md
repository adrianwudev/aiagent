## Get Started
- setup virtual environment
python -m venv venv

- activate venv
.\venv\Scripts\activate

- install packages
pip install -r .\requirements.txt



## Prerequisite

#### Install Python 3.13.0 using pyenv

1.  **Install `pyenv-win`:**
    Open PowerShell and execute the following commands to clone `pyenv-win` to your user directory and set environment variables:

    ```powershell
    cd $HOME
    git clone [https://github.com/pyenv-win/pyenv-win.git](https://github.com/pyenv-win/pyenv-win.git) .pyenv
    [System.Environment]::SetEnvironmentVariable('PYENV_ROOT', "$HOME\.pyenv", 'User')
    [System.Environment]::SetEnvironmentVariable('Path', "$HOME\.pyenv\pyenv-win\bin;<span class="math-inline">HOME\\\.pyenv\\pyenv\-win\\shims;</span>{env:Path}", 'User')
    ```
    * **Important:** Close and reopen your PowerShell window to apply the environment variable changes.

2.  **Verify `pyenv-win` Installation:**
    In the new PowerShell window, run:
    ```powershell
    pyenv --version
    ```
    You should see the `pyenv-win` version number.

3.  **Install Python 3.13.0:**
    Use `pyenv-win` to download and install Python 3.13.0:
    ```powershell
    pyenv install 3.13.0
    ```
    This process downloads the official Python installer and installs it within `pyenv-win`'s managed directory.

4.  **Set Global Python Version (Optional but Recommended):**
    To make Python 3.13.0 the default for all new PowerShell sessions:
    ```powershell
    pyenv global 3.13.0
    ```

5.  **Verify Installed Python Version:**
    Confirm the active Python version:
    ```powershell
    python --version
    ```
    This should output `Python 3.13.0`.

#### Create and Activate a Virtual Environment for a New Project
It is strongly recommended to create a dedicated virtual environment for each project. This isolates project dependencies, preventing conflicts between different projects.

1. Navigate to your project directory:
    ```powershell
    cd D:\my_new_project
    ```
2. Ensure the correct Python version is set for the project (optional but good practice):
    ```powershell
    pyenv local 3.13.0
    ```

You are now set up to manage multiple Python versions with `pyenv-win`, ensuring isolated project environments.