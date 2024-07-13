# Operational Research Problem solver

# How to run?
### STEPS:

Clone the repository

### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n name_of_your_env_choice python=3.9 -y
```

```bash
conda activate name_of_your_env_choice
```

### STEP 02- install the requirements

```bash
pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your Google Gemini API credentials as follows:

```ini
GOOGLE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# Finally run the following command
streamlit run run.py
```

Now,
```bash
open up localhost:
```

### Techstack Used:

- Python
- Streamlit
- Pyomo

