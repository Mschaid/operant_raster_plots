# %%
import numpy as np
import pandas as pd
import os
import OpperantBehaviorTools as obt
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns

abspath = input(r"R:\Mike\Behavior\JS_for_raster\test_data_fold")
print('creating directories')

# directory that contains raw data directories
raw_data_path = os.path.join(abspath, 'raw_data')

# create new directoy data to store csvs+
extracted_data = obt.create_new_dir(abspath, 'extracted_data')

# creates new directory to save compiled data that is processed and analyzed

# directory that contains parameter files
param_dir = os.path.join(abspath, 'parameters')
parameters_path = obt.list_subdirs(param_dir)

# create list of all med files to be read
files = obt.list_subdirs(raw_data_path)
# filters files to ensure csv files are not read
med_files = [f for f in files if not f.endswith('csv')]


def read_params(path):
    """Function to load paremeters from json files -> to be used to rename columns in dataframe """

    with open(path) as f:
        params = json.load(f)
    return params


def find_param(params: list, regex: str,) -> str:
    for i in params:
        if re.match(regex, i):
            return i


print('reading med files and coverting to csvs')

# read all med files with empty parameter file and save as feather files
for f in med_files:
    obt.read_medpc(f, path_to_save=extracted_data)


print("renaming parameters")


def get_names(f): return os.path.basename(f).split(
    '.')[0]  # function to get names of parameters


def rename_params(path):

    df = pd.read_csv(path)
    if 'Right' in df['MSN'][0]:
        df = df.rename(columns=parameter['left_right_liq'])
    elif 'Center' in df['MSN'][0]:
        df = df.rename(columns=parameter['center_liq'])
    else:  # if parameter file is not found, the csv file is deleted
        os.remove(path)
    df.to_csv(path)


parameter = {get_names(f): read_params(f)
             for f in parameters_path}

read_files_csv = obt.list_subdirs(extracted_data)


for f in read_files_csv:
    print(f)
    rename_params(f)

# list of csvs I had to manually enter bc med didnt save


# %%
df = pd.read_csv(read_files_csv[5])


def clean_data(df):
    cols = ['Left nose ITI timestamps', 'Left nose cue reward timestamps',
            'Right nose ITI timestamps', 'Right nose cue reward timestamps']
    return (df[cols]
            .rename(columns=lambda c: c.replace(' ', '_').lower())
            .fillna(-1000)
            .transpose()
            )


behav = clean_data(df)
behav.columns
# %%
# TODO: need to figure out how to get event names and label plot
arr = np.array(behav)
fig, ax = plt.subplots()
ax.eventplot(
    arr,
    orientation="horizontal",
    linelengths=0.5,
    linewidth=1,
    rasterized=True,
)
ax.set_xlim(0,)
plt.show()

# %%
