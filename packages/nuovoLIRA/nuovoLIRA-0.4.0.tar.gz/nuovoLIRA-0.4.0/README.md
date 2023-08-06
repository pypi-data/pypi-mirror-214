nuovoLIRA
==============================

# What is it? 
A method to implement the Bayesian model described here: [https://nuovolira.tiiny.site/](https://nuovolira.tiiny.site/).

# Installation 
```
pip install --upgrade pip 
pip install nuovoLIRA 
``` 

# Main Features 
- Algorithms that sample from the conditional distributions of the NuovoLIRA model 

# Source Code
The source code is currently hosted on GitHub at [https://github.com/bmartin9/nuovolira-pypi](https://github.com/bmartin9/nuovolira-pypi).

# Example Usage 
To sample from the conditional distribution of $Z$ (equation (33) in  [https://nuovolira.tiiny.site/](https://nuovolira.tiiny.site/)) using the Swendsen Wang algorithm do

```
from nuovoLIRA.models.deconvolver import * 
from numpy.random import default_rng

random_state = default_rng(seed=SEED) 
Z_init = np.random.choice([0, 1], size=(10,10), p=[1./3, 2./3])
data = np.random.randint(0,40,size=(10,10))

Z_sampler = Sample_Z(random_state=random_state,
                        initial_Z = Z_init,
                        beta = 2,
                        lam_b = 1,
                        lam_e = 20,
                        y = data
)

Z_new = Z_sampler.Z_update(Z_init) 
```

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
