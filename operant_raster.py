

import numpy as np
import pandas as pd
import os
import OpperantBehaviorTools as obt
import json
import re
import matplotlib.pyplot as plt


abspath = input(
    'Hi Dr. Jilly, please enter the path to the folder you wish to analyze: ')
# abspath = r'R:\Mike\Behavior\JS_for_raster\test_data_fold'

# directory that contains raw data directories
raw_data_path = os.path.join(abspath, 'raw_data')

# create new directoy data to store csvs+
extracted_data = obt.create_new_dir(abspath, 'extracted_data')
raster_tiffs = obt.create_new_dir(abspath, 'raster_tiffs')
raster_svgs = obt.create_new_dir(abspath, 'raster_svgs')

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
        df.to_csv(path)

    elif 'Center' in df['MSN'][0]:
        df = df.rename(columns=parameter['center_liq'])
        df.to_csv(path)

    else:  # if parameter file is not found, the csv file is deleted
        os.remove(path)


parameter = {get_names(f): read_params(f)
             for f in parameters_path}

read_files_csv = obt.list_subdirs(extracted_data)

for f in read_files_csv:
    rename_params(f)

filtered_csvs = obt.list_subdirs(extracted_data)
len(filtered_csvs)

# %%

print('making raster plots')


def clean_data(df):
    cols = ['Left nose ITI timestamps', 'Left nose cue reward timestamps',
            'Right nose ITI timestamps', 'Right nose cue reward timestamps']
    return (df[cols]
            .rename(columns=lambda c: c.replace(' ', '_').lower())
            .fillna(-1000)
            .transpose()
            )


def make_raster(path):
    basename = os.path.basename(path).split('.')[0]
    df = pd.read_csv(path)

    behav = clean_data(df)

    arr = np.array(behav)
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle(
        f"date: {df['Start Date'][0]}   mouse: {df['Subject'][0].astype(int)}   program {df['MSN'][0]}", fontsize=20)

    colors1 = ['black', 'red', 'green', 'blue']
    behavior = [b.replace('_', ' ').capitalize() for b in behav.index]

    ax.eventplot(
        arr,
        orientation="horizontal",
        linelengths=0.5,
        linewidth=.75,
        color=colors1,
        rasterized=True,
    )

    ax.tick_params(length=0)
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(behavior, fontsize=16)
    ax.set_xlim(0,)
    ax.set_xticklabels([0, 1000, 2000, 3000, 4000], fontsize=16)
    ax.set_xlabel("Time (s)", fontsize=16)

    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    plt.rcParams['svg.fonttype'] = 'none'  # save text as text in svg
    plt.savefig(f"{raster_tiffs}\\{basename}.tiff",
                dpi=300,
                transparent=True)
    plt.savefig(f"{raster_svgs}\\{basename}.svg",
                dpi=300,
                transparent=True)


for f in filtered_csvs:
    make_raster(f)
# %%
