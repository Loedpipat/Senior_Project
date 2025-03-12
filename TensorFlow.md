# TensorFlow Setup Guide
## Basic Information
- **How to install ref**: [Ref](https://www.youtube.com/watch?v=Ot8ETwu4fsg&list=PLvryaFgeDtavHuROwcZU5SSi3oKj_zDOG&index=6 )
---

## 0. Anaconda Download
- **Download Link**: [Web](https://www.anaconda.com/download/success)

## 1. Install Anaconda Python
- Open cmd or powershell on your OS:
    ```bash
    C:\>conda update conda
    C:\>conda install anaconda
    C:\>conda update python
    C:\>conda update --all
    C:\>conda create --name tf2
    C:\>conda activate tf2
    (tf2) C:\>conda install -c anaconda tensorflow
    (tf2) C:\>conda install numpy
    (tf2) C:\>conda install pandas
    (tf2) C:\>conda install matplotlib
    (tf2) C:\>python
    >>>import tensorflow as tf
    >>>tf.__version__
    >>>quit()
    ```
## 2. Jupyter Notebook
- Install Jupyter Notebook:
    ```bash
    (tf2) C:\>conda install ipykernel
    ```
- Create environment in Jupyter Notebook:
    ```bash
    (tf2) C:\>python -m ipykernel install --user --name tf2 --display-name "TensorFlow2"
    (tf2) C:\>jupyter notebook
    ```
## 3. Get Started
- Open your folder and put "cmd" on search bar:
    ```bash
    $ C:\Users\User\OneDrive\เดสก์ท็อป\TensorFlow>activate tf2
    $ (tf2) C:\Users\User\OneDrive\เดสก์ท็อป\TensorFlow>jupyter notebook
    ```