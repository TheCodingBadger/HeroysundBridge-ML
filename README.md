markdown

# HerøysundBridge-ML
🔍 Master's Thesis project on using machine learning as part of a Structural Health Monitoring (SHM) assessment on a damaged, post-tensioned bridge. This is an open-source file repository for the master's project "Machine Learning-Assisted Structural Health Monitoring of Herøysund Bridge". Models and datasets can be provided upon request.

For more information or to request models and datasets, please contact:

- Erling Husøy at [Erling.Husoy@multiconsult.no](mailto:Erling.Husoy@multiconsult.no)
- Emil Steen at [Emil.steen@betonmast.no](mailto:Emil.steen@betonmast.no)

We will soon be unavailable through NTNU's email system, but you can reach us at the provided addresses.

## TensorFlow-GPU Requirements (NOTE: CODE CAN BE RUN WITHOUT HTIS REQUIREMENT)
To run the code using TensorFlow-GPU, ensure that your system meets the following requirements:

1. **CUDA-Capable Graphics Card**: Ensure that you have a compatible NVIDIA graphics card installed in your system.

2. **Required NVIDIA® Software**:
    - **NVIDIA® GPU drivers version 450.80.02 or higher**.
        - Note: Can be checked with the command `nvidia-smi` in PowerShell.
    - **CUDA® Toolkit 11.8**.
    - **cuDNN SDK 8.6.0**.

Without these requirements, TensorFlow-GPU will not be able to utilize the GPU for computations, and the code may fall back to CPU execution, leading to slower performance.

## Windows Subsystem for Linux (WSL)
In order to take use of the GPU, follow  dowload instructions from: https://learn.microsoft.com/en-us/windows/wsl/install
Command in powershell: wsl --install

## Setting Up a Virtual Environment and Installing Dependencies
NOTICE: Please note that the build of this repository is around Python 3.11.7.

1. Setting Up a Virtual Environment:

Before you start, it's recommended to set up a virtual environment. This ensures that the dependencies of the project don't interfere with your system Python and other projects.

For Windows:

python -m venv venv
venv\Scripts\activate

You should now see (venv) at the beginning of your terminal prompt, indicating that you're in the virtual environment.

2. Installing Dependencies:

With the virtual environment activated, install the project's dependencies using the following command:

pip install -r requirements.txt

This will install all required packages listed in the requirements.txt file.

3. Deactivating the Virtual Environment:

When you're done, you can deactivate the virtual environment and return to your system Python with:

deactivate

## Useful commands in python/PowerShell/Command Prompt
py -3.11 -m venv venv
.\venv\Scripts\activate
py --version
py -m pip install -U pip wheel
py -m pip install -r requirements.txt



**From TensorFlow-docs:**
*Verify the installation*
*Verify the GPU setup:*
    python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
    If a list of GPU devices is returned, you've installed TensorFlow success
