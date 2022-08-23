<p align="center">
  <a href="" rel="noopener">
 <img width=400px height=210px src="https://github.com/aashrafh/mozart/blob/main/logo.svg" alt="Mozart logo"></a>
</p>

<p align="center"> :notes: Convert sheet music to a machine-readable version.
    <br> 
</p>

<p align="center">
  <a href="https://github.com/aashrafh/mozart/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/aashrafh/mozart" /></a>
  
   <a href="https://github.com/aashrafh/mozart/issues" alt="Issues">
        <img src="https://img.shields.io/github/issues/aashrafh/mozart" /></a>
  
  <a href="https://github.com/aashrafh/mozart/network" alt="Forks">
        <img src="https://img.shields.io/github/forks/aashrafh/mozart" /></a>
        
  <a href="https://github.com/aashrafh/mozart/stargazers" alt="Stars">
        <img src="https://img.shields.io/github/stars/aashrafh/mozart" /></a>
        
  <a href="https://github.com/aashrafh/mozart/blob/master/LICENSE" alt="License">
        <img src="https://img.shields.io/github/license/aashrafh/mozart" /></a>
</p>


---

## 📝 Table of Contents
- [About](#about)
- [Methodology](#methodology)
- [Install](#Install)
- [Technology](#tech)

## 🧐 About <a name = "about"></a>
The aim of this project is to develop a sheet music reader. This is called Optical Music Recognition (OMR). Its objective is to convert sheet music to a machine-readable version. We take a simplified version where we convert an image of sheet music to a textual representation that can be further processed to produce midi files or audio files like wav or mp3. 
<p align="center">
  <a href="" rel="noopener">
 <img src="https://github.com/aashrafh/Mozart/blob/main/about.png" alt="About"></a>
</p>

## :computer: Methodology <a name = "methodology"></a>

### 1. Noise Filtering and Binarization
<p align="center">
  <a href="" rel="noopener">
 <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_binary.png" alt="Binary Image"></a>
</p>

### 2. Segmentation

<p align="center">
  <a href="" rel="noopener">
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_seg_0.png" alt="Segment 1"></a><br> <br> 
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_seg_1.png" alt="Segment 2"></a><br> <br> 
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_seg_2.png" alt="Segment 3"></a>
</p>


### 3. Staff Line Detection and Removal

<p align="center">
  <a href="" rel="noopener">
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_without_staff_0.png" alt="No Staff Image 1"></a><br> <br> 
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_without_staff_1.png" alt="No Staff Image 2"></a><br> <br> 
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_without_staff_2.png" alt="No Staff Image 3"></a>
</p>

### 4. Construct The New Staff Lines

<p align="center">
  <a href="" rel="noopener">
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_with_new_staff_0.png" alt="New Staff Image 1"></a><br> <br> 
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_with_new_staff_1.png" alt="New Staff Image 2"></a><br> <br> 
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_with_new_staff_2.png" alt="New Staff Image 3"></a>
</p>


### 5. Symbol Detection and Recognition

<p align="center">
  <a href="" rel="noopener">
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_detected_0.png" alt="Result 1"></a><br> <br> 
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_detected_1.png" alt="Result 2"></a><br> <br> 
  <img src="https://github.com/aashrafh/Mozart/blob/main/output/imgs/02/02_detected_2.png" alt="Result 3"></a>
</p>


## 🏁 Install <a name = "Install"></a>
1. You can use the attached notebook for quick testing and visualization.
2. You can setup an environment on your local machine to run the project:
    1. Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
    2. ```conda env create -f requirements.yml```
    3. ```conda activate mozart```
    4. ```python3 main.py <input directory path> <output directory path>```

> You can find the dataset on [Google Drive](https://drive.google.com/drive/u/0/folders/1OVGA3CGnEKjyg_k_L8MP2RO5R3oDIbHE).

> Please check the following [issue](https://github.com/aashrafh/Mozart/issues/8) for another ```requirements.yml``` file. 


## ⛏️ Built Using <a name = "tech"></a>
- [Python 3.8.3](https://www.python.org/)
- [NumPy](https://numpy.org/doc/stable/index.html)
- [OpenCV](https://opencv.org/)
- [scikit-learn](https://scikit-learn.org/stable/)
- [scikit-image](https://scikit-image.org/)
