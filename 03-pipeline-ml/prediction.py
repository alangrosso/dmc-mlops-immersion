import itertools

import pandas as pd
import numpy as np

import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient

from sklearn.metrics import roc_auc_score, confusion_matrix, ConfusionMatrixDisplay

#============================ Setup

CREATED_BY = "AGR"

# Setear url
# mlflow.set_tracking_uri("http://127.0.0.1:5000/")  # Reemplaza con la URL correcta de tu servidor MLflow

# Cliente
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000/" # Reemplaza con la URL correcta de tu servidor MLflow
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

#============================ Importar IDs

temp = pd.read_csv("ids.csv")
# print(temp)

EXPERIMENT_ID = temp['EXPERIMENT_ID'][0]
RUN_ID = temp['RUN_ID'][0]
MODEL_VERSION = temp['MODEL_VERSION'][0]
REGISTERED_MODEL_NAME = temp['REGISTERED_MODEL_NAME'][0]
MODEL_STAGE = temp['MODEL_STAGE'][0]
# SOURCE = temp['SOURCE'][0]

print('*************************************************')
print(f"Experiment ID: {EXPERIMENT_ID} | Run ID: {RUN_ID}")
print(f"Model Version: {MODEL_VERSION} | Stage: {MODEL_STAGE}")
# print(f"Model Source: {SOURCE}")
      
#============================ Cargar el mejor modelo

# En caso se exportó
# MODEL_URI = ''
# best_model = mlflow.pyfunc.load_model(MODEL_URI)

# Model version
# SOURCE = f"models:/{REGISTERED_MODEL_NAME}/{MODEL_VERSION}"
# model = mlflow.pyfunc.load_model(model_uri=SOURCE)

# Model version y Stage
# SOURCE = f"models:/{REGISTERED_MODEL_NAME}/{MODEL_STAGE}"
# model = mlflow.pyfunc.load_model(model_uri=SOURCE)

# Para obtener Probabilidades
SOURCE = f"runs:/{RUN_ID}/model_export" # actualizar
model = mlflow.sklearn.load_model(model_uri=SOURCE)
pipe = model

#============================ Variables

# Get a list of the columns we used
## random_forest
# USED_COLUMNS = list(itertools.chain.from_iterable([x[2] for x in preprocessor.transformers]))
## evaluate
USED_COLUMNS = list(itertools.chain.from_iterable([x[2] for x in pipe['preprocessor'].transformers]))
print(USED_COLUMNS)

#============================ Nuevos datos: Validación (-n periodos de tiempo)

PRED_DATA_PATH_AUC = 'predictions/data_val_auc.csv' # reemplaza con tus datos de entrada
input_data = pd.read_csv(PRED_DATA_PATH_AUC, low_memory=False)
print(input_data.shape)

# Feature Engineering
input_data['title'].fillna(value='', inplace=True)
input_data['song_name'].fillna(value='', inplace=True)
input_data['text_feature'] = input_data['title'] + ' ' + input_data['song_name']

# Variables y Clase
input_data_X = input_data.copy()
input_data_y = input_data_X.pop('genre')

#======= Performance

# Considerar indicador de acuerdo a entrenamiento
# y_new_test -> y real

def test_model(source, y_new_test, X_new_data):
    model = mlflow.sklearn.load_model(source)
    pred_proba = model.predict_proba(X_new_data)
    score = roc_auc_score(y_new_test, pred_proba, average="macro", multi_class="ovo", labels=model.classes_)
    return score

print('*************************************************')

auc_dev =  test_model(SOURCE, input_data_y, input_data_X[USED_COLUMNS])
print(f"AUC: {auc_dev}")

#============================ Nuevos datos: Deploy (actual)

PRED_DATA_PATH = 'predictions/data_val.csv' # reemplaza con tus datos de entrada
input_data = pd.read_csv(PRED_DATA_PATH, low_memory=False)

input_data['title'].fillna(value='', inplace=True)
input_data['song_name'].fillna(value='', inplace=True)
input_data['text_feature'] = input_data['title'] + ' ' + input_data['song_name']

input_data_X = input_data.copy()
input_data_y = input_data_X.pop('genre')

#======= Predictions 

def generate_predictions(source, X_new_data):
    model = mlflow.pyfunc.load_model(source)
    y_pred = model.predict(X_new_data)
    return y_pred

def generate_predictions_proba(source, X_new_data):
    model = mlflow.sklearn.load_model(source)
    y_pred = model.predict_proba(X_new_data)[:, 1]
    return y_pred

print('*************************************************')

pred =  generate_predictions(SOURCE, input_data_X[USED_COLUMNS])
print(f"Género musical predicho: {pred[0]}")

pred_proba = generate_predictions_proba(SOURCE, input_data_X[USED_COLUMNS])
print(f"Probabilidad: {pred_proba[0]:.4f}")