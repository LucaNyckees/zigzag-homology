
# Computing Levelset Zigzag Homology

This is a project done by Luca Nyckees and Nicolas Berkouk, with the [Laboratory of Topology and Neuroscience at EPFL](https://www.epfl.ch/labs/hessbellwald-lab/).


## Table of Content

* [People](#people)
* [Description](#description)
* [Project Organization](#project-organization)
* [Streamlit Web App](#streamlit)
* [Related Articles and Useful References](#refs)
* [Interesting Material 🔍](#material)

## People

Nicolas Berkouk : [Website](https://nberkouk.github.io/)<br />
Luca Nyckees : [GitHub](https://github.com/LucaNyckees)

## Description

Zigzag persistence, as introduced by Carlsson and De Silva [[1]](https://arxiv.org/abs/0812.0197), offers a way to better understand the persistence of topological features observed in a family of spaces or pointclouds by generalizing the setting of persistent homology. In this project, we aim at providing a tool to compute levelset zigzag persistence. The idea is to deduce the results from computations on extended persistence, which are already implemented in C++. To this end, we make use of Python bindings.

<img width="450" alt="figure" src="https://github.com/LucaNyckees/zigzag/blob/main/figures/11-Figure2-1.png">

A bijection between the extended persistence barcode and the zigzag barcode can be established via so-called "diamond moves", involving the presence of relative Mayer-Vietoris diamonds, illustrated in the animation below. The precise statement is formulated as the *Strong Diamond Principle* - sometimes called the *Pyramid Theorem* - in [[1]](https://arxiv.org/abs/0812.0197). The whole process relies on consecutive transformations between two sequences of spaces that differ only at one point, so that the difference can be expressed by a relative Mayer-Vietoris diamond.

<img width="550" alt="figure" src="https://github.com/LucaNyckees/zigzag/blob/main/figures/pyramid_zigzag.gif">

## Project Organization
------------
```
├── LICENSE
|
├── config files (.env, .ini, ...)
|
├── README.md
│
├── docs/               
│
├── requirements.txt  
|
├── __main__.py
│
├── src/                
|     ├── __init__.py
|     └── _version.py
|
└── tests/
```
   
--------

## Streamlit Web App

You can launch the Streamlit web application with the following commands. First, open a shell/terminal and go to the directory in which you saved the project - for example :

```
cd Desktop/levelset/zigzag
```
Then, go directly to the source code with 

```
cd src
```

Finally, type the command below in your shell and enjoy the app!
```
streamlit run st_app.py
```
For an original theme configuration, you may replace the last command with this one :
```
streamlit run st_app.py --theme.primaryColor="#3271e2" --theme.backgroundColor="#357dc5" --theme.secondaryBackgroundColor="#68708c" --theme.textColor="#dadde6"
```

## Related Articles and Useful References

[[1]](https://arxiv.org/abs/0812.0197) - Zigzag Persistence\
[[2]](https://arxiv.org/abs/2105.00518) - Computing Optimal Persitent Cycles for Levelset Zigzag on Manifold-like Complexes\
[[3]](https://arxiv.org/abs/0911.2142) - Quantifying Transversality by Measuring the Robustness of Intersections\
[[4]](https://www.mrzv.org/publications/robustness-levelsets/esa/) - The Robustness of Level Sets

## Interesting Material 🔍

+ Tutorial on Python bindings [[click here]](https://realpython.com/python-bindings-overview/)
+ Video lectures on topological data analysis by Henry Adams [[click here]](https://www.math.colostate.edu/~adams/teaching/dsci475spr2021/)

## Virtual environment
Use the following command lines to create and use venv python package:
```
python3.10 -m venv venv
```
Then use the following to activate the environment:
```
source venv/bin/activate
```
You can now use pip to install any packages you need for the project and run python scripts, usually through a `requirements.txt`:
```
python -m pip install -r requirements.txt
```
When you are finished, you can stop the environment by running:
```
deactivate
```
