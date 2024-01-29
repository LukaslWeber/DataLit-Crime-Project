# DataLit-Crime-Project
 This is our project submission for the "Data Literacy" course by Prof. Dr. Philipp Hennig.

# Topic: Analyzing the "Polizeiliche Kriminalstatistik" (PKS)
The PKS refers to crime statistics released by the Bundeskriminalamt (German Federal Office of Criminal Investigation). 
Within the scope of this project, we conduct an exploratory data analysis on various tables found in the PKS, focusing either on spatial or temporal data.

# Overview
- exp contains our analyses in spatial_exploration.ipynb and temporal_exploration.ipynb along with related plots
- dat contais all used datasets sorted by source and years
- src contains necessary files to import and process the data
- doc contains our report and figures

# Installation manual
Installation via ``pip`` is recommended. If prompted, we can also provide a conda environment which wasn't as reliable as a pip-based environment in our tests.

## Virual Environment
### Windows
Create a virtual environment by running in your repository:
```
python -m venv .venv
```

Activate the environment:
```
.venv\Scripts\activate
```

You can then install the required packages with:
```
python -m pip install -r requirements.txt
```

### Unix and MacOS
Create a virtual environment by running:
```
python -m venv .venv
```

Activate the environment:
```
source .venv/bin/activate
```
You can then install the required packages with:
```
python -m pip install -r requirements.txt
```


