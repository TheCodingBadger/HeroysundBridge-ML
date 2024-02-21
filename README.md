# HeroysundBridge-ML
🔍 Master's Thesis project on using machine learning as a part of a SHM assesment on a damaged, post-tensioned bridge. 

## TensorFlow-GPU Requirements
To run the code using TensorFlow-GPU, ensure that your system meets the following requirements:

1. CUDA-Capable Graphics Card: TensorFlow-GPU requires a CUDA-capable GPU for acceleration. Ensure that you have a compatible NVIDIA graphics card installed in your system.

2. CUDA Toolkit: It is necessary to have the CUDA Toolkit installed on your system. TensorFlow-GPU interacts with the CUDA Toolkit to execute computations on the GPU. Make sure to install the version of the CUDA Toolkit that is compatible with your graphics card and TensorFlow version.

3. The following NVIDIA® software are only required for GPU support (From: https://www.tensorflow.org/install/pip#software_requirements):

    NVIDIA® GPU drivers version 450.80.02 or higher.
        Note: Could be checked with command "nvidia-smi" in PowerrShell
    CUDA® Toolkit 11.8.
    cuDNN SDK 8.6.0.

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