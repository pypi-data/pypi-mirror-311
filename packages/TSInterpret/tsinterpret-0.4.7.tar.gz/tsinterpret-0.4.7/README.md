<p align="center">
    <img src="./docs/img/logo.png" alt="TSInterpret Logo" height="300"/>
</p>
<p align="center">
  <a href="https://github.com/fzi-forschungszentrum-informatik/TSInterpret/actions/workflows/unit-tests.yml">
    <img src="https://github.com/fzi-forschungszentrum-informatik/TSInterpret/actions/workflows/unit-tests.yml/badge.svg" alt="tests">
  </a>
    <img alt="PyPI" src="https://img.shields.io/pypi/v/tsinterpret">
    <a href="https://codecov.io/gh/fzi-forschungszentrum-informatik/TSInterpret" > 
        <img src="https://codecov.io/gh/fzi-forschungszentrum-informatik/TSInterpret/branch/main/graph/badge.svg?token=1IGZKTLZ4J"/> 
    </a>
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/tsinterpret">
    <img alt="GitHub" src="https://img.shields.io/github/license/fzi-forschungszentrum-informatik/TSInterpret">
    <a style="border-width:0" href="https://doi.org/10.21105/joss.05220">
  <img src="https://joss.theoj.org/papers/10.21105/joss.05220/status.svg" alt="DOI badge" >
</a>
</p>

TSInterpret is a Python library for interpreting time series classification.
The ambition is to faciliate the usage of time series interpretability methods. The Framework supports Sklearn, Tensorflow, Torch and in some cases predict functions. A listing of implemented algorithms and supported frameworks can be found in our <a href="https://fzi-forschungszentrum-informatik.github.io/TSInterpret/">Documentation</a>. More information on our framework can be found in our <a href="https://arxiv.org/abs/2208.05280"> paper<a>.

## 💈 Installation
```shell
pip install TSInterpret
```
You can install the latest development version from GitHub as so:
```shell
pip install https://github.com/fzi-forschungszentrum-informatik/TSInterpret/archive/refs/heads/main.zip
```



## 🍫 Quickstart
The following example creates a simple Neural Network based on tensorflow and interprets the Classfier with Integrated Gradients and Temporal Saliency Rescaling [1].
For further examples check out the <a href="https://fzi-forschungszentrum-informatik.github.io/TSInterpret/">Documentation</a>.

[1] Ismail, Aya Abdelsalam, et al. "Benchmarking deep learning interpretability in time series predictions." Advances in neural information processing systems 33 (2020): 6441-6452.

### Import
```python
import pickle
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as snst
from tslearn.datasets import UCR_UEA_datasets
import tensorflow as tf 

```
### Create Classifcation Model
This Section uses a pretrained Classification Model to illustrate the use of our package. For running the example, please clone our repository and comment the variable  PATH_TO_YOUR_CLASSIFICATION_MODEL in. The code in this section can also be replaces with your personal classification model written in torch or tensorflow.
```python

# Load data.
dataset='BasicMotions'
train_x,train_y, test_x, test_y=UCR_UEA_datasets().load_dataset(dataset)
enc1=sklearn.OneHotEncoder(sparse=False).fit(train_y.reshape(-1,1))
train_y=enc1.transform(train_y.reshape(-1,1))
test_y=enc1.transform(test_y.reshape(-1,1))

# Load a model.
#e.g., PATH_TO_YOUR_CLASSIFICATION_MODEL=f'./TSInterpret/ClassificationModels/models/{dataset}/cnn/{dataset}best_model.hdf5'
model_to_explain = tf.keras.models.load_model(PATH_TO_YOUR_CLASSIFICATION_MODEL)

```
### Explain & Visualize Model
```python
from TSInterpret.InterpretabilityModels.Saliency.TSR import TSR
int_mod=TSR(model_to_explain, train_x.shape[-2],train_x.shape[-1], method='IG',mode='time')
item= np.array([test_x[0,:,:]])
label=int(np.argmax(test_y[0]))

exp=int_mod.explain(item,labels=label,TSR =True)

%matplotlib inline  
int_mod.plot(np.array([test_x[0,:,:]]),exp)

```
<p align="center">
    <img src="./docs/img/ReadMe.png" alt="Algorithm Results" height="200"/>
</p>

## :monocle_face: Why a special package for the interpretability of time series predictors? 

Compared to other data types like tabular, image, or natural language data, time series data is unintuitive to understand. Approaches to the explainability of tabular regression and classification often assume independent features.  Compared to images or textual data, humans cannot intuitively and instinctively understand the underlying information contained in time series data. Further, research has shown that applying explainability algorithms for tabular, image, or natural language data often yields non-understandable  and inaccurate explanations, as they do not consider the time component (e.g., highlighting many unconnected time-steps, instead of features or time slices [1]). 
Increasing research has focused on developing and adapting approaches to time series (survey: [2]). However, with no unified interface, accessibility to those methods is still an issue. TSInterpret tries to facilitate this by providing a PyPI package with a unified interface for multiple algorithms, documentation, and learning resources (notebooks) on the application.

[2] Rojat, Thomas, et al. "Explainable artificial intelligence (xai) on timeseries data: A survey." arXiv preprint arXiv:2104.00950 (2021).

## 👐 Contributing

Feel free to contribute in any way you like, we're always open to new ideas and approaches.

- If you have questions, spotted a bug or ideas, feel free to open an [issue](https://github.com/fzi-forschungszentrum-informatik/TSInterpret/issues/new/choose).
- Before opening a pull request, we also encourage users to open an issue for discussion. 

Details on how to Contribute can be found  [here](https://github.com/fzi-forschungszentrum-informatik/TSInterpret/blob/main/CONTRIBUTING.md).

## 🏫 Affiliations
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/de/thumb/4/44/Fzi_logo.svg/1200px-Fzi_logo.svg.png?raw=true" alt="FZI Logo" height="200"/>
</p>

## Citation

If you use TSInterpret in your research, please consider citing it and the authors' original papers. The authors' original papers are cited in the documentation and the paper below.

```
@article{Höllig2023, 
doi = {10.21105/joss.05220}, 
url = {https://doi.org/10.21105/joss.05220}, 
year = {2023}, 
publisher = {The Open Journal}, 
volume = {8}, 
number = {85}, 
pages = {5220}, 
author = {Jacqueline Höllig and Cedric Kulbach and Steffen Thoma}, 
title = {TSInterpret: A Python Package for the Interpretability of Time Series Classification}, journal = {Journal of Open Source Software} } 
```
