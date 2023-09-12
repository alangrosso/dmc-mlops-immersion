import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
import pandas as pd

#============================ Setup

CREATED_BY = "AGR"

# Setear url
# mlflow.set_tracking_uri("http://127.0.0.1:5000/")  # Reemplaza con la URL correcta de tu servidor MLflow

# Cliente
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000/" # Reemplaza con la URL correcta de tu servidor MLflow
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

#============================ Experimentos

# Verificamos cuantos experimentos se han ejecutado
temp_search = client.search_experiments()
temp_search = list(temp_search)
print(f"Número de experimentos: {len(temp_search)}")
experiment_list = [exp.name for exp in temp_search]
print(f"Nombres de los experimentos: {experiment_list}")

# Especifica el nombre de experimento
EXPERIMENT_NAME = "dev_genre_classification" # actualizar

# Obtener el objeto del experimento
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Verifica si el experimento existe
if experiment is not None:
    # Obtiene el ID del experimento
    EXPERIMENT_ID = experiment.experiment_id
    print(f"ID del experimento '{EXPERIMENT_NAME}': {EXPERIMENT_ID}")
else:
    print(f"No se encontró el experimento '{EXPERIMENT_NAME}'")

#============================ Mejor Modelo

# Busca todos los runs del experimento
runs = mlflow.search_runs(experiment_ids=mlflow.get_experiment_by_name(EXPERIMENT_NAME).experiment_id)

# Filtra los runs que corresponden a determinado componente
# Ejem, puede ser referido al modelo en este caso "random_forest"
COMPONENT_NAME = "random_forest" # actualizar
evaluate_runs = runs[runs["tags.mlflow.runName"] == COMPONENT_NAME] 

# Encuentra el run con la mejor métrica (por ejemplo, mayor "AUC")
best_run = evaluate_runs.sort_values(by="metrics.AUC", ascending=False).iloc[0]
RUN_ID = best_run.run_id
print(f"Mejor modelo Run ID: {RUN_ID}")
print(f"Mejor modelo AUC: {best_run['metrics.AUC']:.4f}") # elegir tipo de métrica de acuerdo a entrenamiento

# Obtiene la ruta del modelo guardado en el run
MODEL_URI = f"runs:/{RUN_ID}/model_export" # actualizar, en este caso, se parametrizó con "model_export" al ejecutar con Hydra
# MODEL_URI = f"mlruns:/{EXPERIMENT_ID}/{RUN_ID}/artifacts/model_export" # actualizar
print(f"Mejor modelo URI: {MODEL_URI}")

#============================ Guardar Mejor Modelo

# Guardar el mejor modelo en un archivo si es necesario
# mlflow.pyfunc.save_model(best_model, "best_model")

#============================ Registro del Modelo

# Definir las etiquetas que se desea agregar al modelo
tags = {
    "experiment_name": EXPERIMENT_NAME,
    "created_by": CREATED_BY,
}

REGISTERED_MODEL_NAME = "musical-genre" # actualizar

# Registra el modelo en MLflow con las etiquetas especificadas
mlflow.register_model(model_uri=MODEL_URI, 
    name=REGISTERED_MODEL_NAME, 
    tags=tags)

# Se genera una nueva versión en automático

print('*************************************************')
print("Modelo Registrado: {}".format(mv.name))
print("Version: {}".format(mv.version))
# print("Modelo registrado con etiquetas:", tags)
print('*************************************************')

#============================ Staging

# Todos los nuevos modelos van a etapa de prueba

TARGET_STAGE = "None"

latest_versions = client.get_latest_versions(name=REGISTERED_MODEL_NAME, stages=[TARGET_STAGE])

LATEST_VERSION = latest_versions[0].version

for version in latest_versions:
    # LATEST_VERSION = version.version
    print(f"Version: {version.version}, Stage: {version.current_stage}")

NEW_STAGE = "Staging"

client.transition_model_version_stage(
    name=REGISTERED_MODEL_NAME,
    version=LATEST_VERSION, 
    stage=NEW_STAGE,
    archive_existing_versions=True
)

print(f"Nuevo modelo {LATEST_VERSION} a stage {NEW_STAGE}")

#============================ Producción

# Definimos la versión 1 en Producción

MODEL_VERSION = 1 # actualizar
NEW_STAGE = "Production"

client.transition_model_version_stage(
    name=REGISTERED_MODEL_NAME,
    version=MODEL_VERSION,
    stage=NEW_STAGE,
    archive_existing_versions=True
    )

print(f"Model Version {MODEL_VERSION}, Stage {NEW_STAGE}")

#============================ Exportar mejor modelo

SOURCE = f"mlflow-artifacts:/{EXPERIMENT_ID}/{RUN_ID}/artifacts/best_model"
# SOURCE = 'mlflow-artifacts:/' + EXPERIMENT_ID + '/' + RUN_ID + '/artifacts/best_model'

#============================ Exportar  IDs

temp = pd.DataFrame()

temp['MLFLOW_TRACKING_URI'] = [MLFLOW_TRACKING_URI]
temp['CREATED_BY'] = CREATED_BY
temp['EXPERIMENT_ID'] = EXPERIMENT_ID
temp['RUN_ID'] = RUN_ID
temp['MODEL_VERSION'] = MODEL_VERSION
temp['REGISTERED_MODEL_NAME'] = REGISTERED_MODEL_NAME
temp['MODEL_STAGE'] = NEW_STAGE
temp['SOURCE'] = SOURCE

temp.to_csv("ids.csv", index=None)