# **Pipeline Machine Learning**

Objetivo: predecir el genero musical de una canción.

## **Ambiente virtual**

### conda

Crear archivo `environment.yaml`. Agregar las librerias necesarias para desarrollar el proyecto.

```ssh
# Crear ambiente virtual
conda env create -f environment.yaml
# Activar
conda activate virtual_mlflow
# Configurar kernel
ipython kernel install --user --name=virtual_mlflow

# Salir de entorno
conda deactivate

# Remover entorno
conda env remove --name virtual_mlflow --all
```
### virtualenv

Crear archivo `requirements.txt`. Agregar las librerias necesarias para desarrollar el proyecto.

```ssh
# Crear ambiente virtual
python3.10 -m venv py_env
# Activar
source py_env/bin/activate
# Instalar librerias 
pip install --upgrade pip
pip install -r requirements.txt

# Configurar kernel
ipython kernel install --user --name=py_env

# Salir de entorno
deactivate

# Remover entorno
rm -r py_env
```

## **Pipeline ML (secuencial)**

### 1. Download

Descargar datos.

```ssh
mlflow run ./download -P step=download_data -P file_url="https://github.com/alangrosso/mlflow-pipeline/blob/main/data/genres_mod.parquet?raw=true" -P artifact_name=raw_data.parquet -P artifact_description="Pipeline for data downloading" --experiment-name genre_classification --run-name download_data
```

Visualizar resultados en interfaz de MLflow:

```ssh
mlflow ui
```

### 2. Preprocess

Preprocesamiento de los datos (feature engineering).

```ssh
mlflow run ./preprocess -P step=preprocess -P input_step=download_data -P input_artifact=raw_data.parquet -P artifact_name=preprocessed_data.csv -P artifact_description="Pipeline for data preprocessing" --experiment-name genre_classification --run-name preprocess
```

### 3. Check data

Ejecutar Tests sobre los datos.

```ssh
mlflow run ./check_data -P step=check_data -P input_step=preprocess -P reference_artifact=preprocessed_data.csv -P sample_artifact=preprocessed_data.csv -P ks_alpha=0.05 --experiment-name genre_classification --run-name check_data
```

### 4. Segregate

Train test split.

```ssh
mlflow run ./segregate -P step=segregate -P input_step=preprocess -P input_artifact=preprocessed_data.csv -P artifact_root=data -P test_size=0.3 -P stratify=genre --experiment-name genre_classification --run-name segregate
```

### 5. Model

Entrenamiento del modelo.

```ssh
mlflow run ./random_forest -P step=random_forest -P input_step=segregate -P train_data=data/data_train.csv -P model_config=rf_config.yaml -P export_artifact=model_export -P random_seed=42 -P val_size=0.3 -P stratify=genre --experiment-name genre_classification --run-name random_forest
```

### 6. Evaluate

Evaluar performance del modelo.

```ssh
mlflow run ./evaluate -P step=evaluate -P input_model_step=random_forest -P model_export=model_export -P input_data_step=segregate -P test_data=data/data_test.csv --experiment-name genre_classification --run-name evaluate
```

## **Pipeline ML (full)**

Ejecutamos todos los componentes del pipeline. Nos apoyamos con `Hydra` (framework para manejar complejidad de parámetros).

```ssh
# Componentes del pipeline
├── download/
├── preprocess/
├── check_data/
├── segregate/
├── random_forest/
└── evaluate/

# Archivos para ejecutar pipeline ML
├── MLproject
├── config.yaml
├── environment.yaml
└── main.py
```

Reproducimos todo el pipeline.

```ssh
mlflow run .
```

## **Optimización de hiperparámetros**

Ejecutar por consola los comandos con los hiperparámetros.

```ssh
mlflow run . -P hydra_options="-m random_forest_pipeline.random_forest.n_estimators=60,80 random_forest_pipeline.random_forest.max_depth=range(3,11,4) random_forest_pipeline.random_forest.min_samples_split=15,30"
```

## **Mejor modelo**

Asignamos el mejor modelo a `Producción`.

```ssh
python best_model.py 
```

## **Predictions**

Realizamos nuevas predicciones.

```ssh
python predictions.py
```

## **Conda**

Opciones para remover todos los ambientes creados por Conda.

```ssh
# Verificar ambientes
conda env list

# Eliminar todos los ambientes 
for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda remove --name $e --all -y;done
```

## **Github**

Generar los commits para evidenciar los avances del proyecto:

```ssh
# Crear repo

# Iniciar

git init
git pull

git branch dev
git checkout dev

git add .
git commit -m "feat(03-pipeline-ml): añadir archivos al repo"
git push origin dev

git add .
git commit -m "fix(03-pipeline-ml): corregir README"
git push origin dev

# Merge con rama main:

git checkout main
git merge dev -m "feat(03-pipeline-ml): merge sin conflictos"
```
