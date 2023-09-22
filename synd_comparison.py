# -*- coding: utf-8 -*-
"""synd-comparison.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T-qAZb323Oru0A4FpmwSeqcBLDoK0yQ6

**Define Models to be used for Synthetic Data Generation - CTGAN and TVAE**
"""

import pandas as pd
import numpy as np
import time

pip install sdv==0.18.0

from sdv.tabular import TVAE
from sdv.tabular import CTGAN

from sdv.evaluation import evaluate

import warnings
warnings.filterwarnings('ignore')

df1 = pd.read_csv("adult.csv")
df1.index.name = "adult"

df2 = pd.read_csv("breast_cancer.csv")
df2.index.name = "breast_cancer"

df3 = pd.read_csv("heart_cleveland_upload.csv")
df3.index.name = "heart"

df4 = pd.read_csv("Iris.csv")
df4.index.name = "iris"

df5 = pd.read_csv("creditcard.csv")
df5.index.name = "credit"

#df5.name

df1.head()

dfs = [df1, df2, df3, df4, df5]

# To store generated synthetic data
synthetic_data_mapping = {}

metrics=['CSTest', 'KSTest', 'ContinuousKLDivergence', 'DiscreteKLDivergence']
saved_models = {}

for df in dfs:
    print('\n' + '%'*40)
    print('\033[1m' + df.index.name + '\033[0m')
    #print(df.index.name)
    print('%'*40 + '\n')
    df.info()
    display(df.head())
    synthetic_data_mapping['syn_' + df.index.name] = []

model = CTGAN()

model.fit(df1)

syn_tab_data = model.sample(num_rows=200)

syn_tab_data.head()

model.save('syn_tab_model.pkl')



"""Handling anonymized field"""

model_pii = CTGAN(
       #primary_key='student_id',
       anonymize_fields={
            'native.country': 'country'
        }
    )

model_pii.fit(df1)

syn_tab_datapii = model.sample(num_rows=200)

syn_tab_datapii.head()

df1.nacountry.isin(syn_tab_datapii.native.country).sum()

def evaluate_model(model, df):

    print('Training in Progress - ' + model.__class__.__name__ + '_' + df.index.name + '\n')

    # Record training time
    start = time.time()
    model.fit(df)
    end = time.time()

    print( '\n' + model.__class__.__name__ + ' trained. \nTraining time: ' + str(end-start) + ' seconds \n')
    syn_data = model.sample(len(df))
    syn_data.name = df.index.name + '-' + model.__class__.__name__

    # Save Generated Synthetic Data for each model in a dictionary
    synthetic_data_mapping['syn_' + df.index.name].append(syn_data)

    # Record evaluation time
    start = time.time()
    ee = evaluate(syn_data, df, metrics=metrics , aggregate=False)
    end = time.time()
    print("Synthetic Data Evaluation - " +  model.__class__.__name__ + '_' + df.index.name + '\n')
    display(ee)
    print('\nEvaluation time: ' + str(end-start) + ' seconds \n')

    # Save the model
    saved_model_name = model.__class__.__name__ + '_' + df.index.name + '.pkl'
    model.save(saved_model_name)
    saved_models[saved_model_name] = model

CTGAN(df1)

#batch_sizes = [10, 30, 50, 100, 200, 300]
#batch_sizes = [10]
#epochs = [20, 30, 50, 100, 200, 300, 500, 1000]
#epochs = [20, 30]
#for (bs,ep) in enumerate(zip(batch_sizes,epochs)):
    #evaluate_model(CTGAN(batch_size=bs, verbose=True, epochs=ep),df1)

evaluate_model(CTGAN(),df1)

k = 0;
for df in dfs:
    evaluate_model(models_ctgan[k], df)
    evaluate_model(models_tvae[k], df)
    k += 1

saved_models

# Commented out IPython magic to ensure Python compatibility.
# %store synthetic_data_mapping

# Commented out IPython magic to ensure Python compatibility.
# %store df1
# %store df2
# %store df3
# %store df4
# %store df5

# Commented out IPython magic to ensure Python compatibility.
# %store df1.name
# %store df2.name
# %store df3.name
# %store df4.name
# %store df5.name

synthetic_data_mapping['syn_' + df1.name][0].head()

synthetic_data_mapping['syn_' + df1.name][1].name

"""**Visualisation**"""

import seaborn as sns
from matplotlib import pyplot as plt

fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(18,6))
sns.kdeplot(data=df1,ax=ax0, x='age', hue='income')
sns.kdeplot(data=synthetic_data_mapping['syn_' + df1.name][0],ax=ax1, x='age', hue='income', label='ctgan', ls='--')
sns.kdeplot(data=synthetic_data_mapping['syn_' + df1.name][1],ax=ax2, x='age', hue='income', label='tvae', ls='-.')
plt.show()

obj_data = df1.select_dtypes(include=['object']).copy()
obj_data.head()

synthetic_data_mapping[df1.name][1].groupby(['income']).size()

synthetic_data_mapping[df1.name][0].groupby(['income']).size()

df1.groupby('income').size()

# VBGMM
from sklearn.mixture import GaussianMixture

vbgmm = GaussianMixture(n_components=3, random_state=42)
col = df1['education.num'].values.reshape(-1,1)
vbg = vbgmm.fit(col)
vbg.means_.shape
vbg.means_

"""**VAE for Adult Census Data**

"import statsmodels.api as sm

m = sm.OLS.from_formula("income_code~ age + fnlwgt+ education_num + capital_gain + capital_loss + hours_per_week", merged_df)
"""
