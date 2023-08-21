# **Pipeline PySpark**

Levantar un pipeline de Pyspark (en Docker), llevando a cabo un proceso de data engineering donde se crearán features y un modelo de machine learning distribuido en Spark ML.

## **Ambiente virtual**

### virtualenv

Crear ambiente virtual:

```ssh
python3.10 -m venv py_env
source py_env/bin/activate
pip install -r requirements.txt
```

## **Desarrollo**

1. Descargar imagen de Pyspark

Ver detalle en `Dockerfile`.

```ssh
# Crear imagen
docker build -t pyspark-lab -f Dockerfile .

# Verificar que se haya creado imagen
docker images
docker images | grep pyspark-lab

# Eliminar imagen
docker image rm pyspark-lab
```

2. Directorios y archivos

```ssh
# Crear Directorio
mkdir spark
mkdir utils

# Crear archivos
touch spark_submit.sh
touch spark/__init__.py
touch spark/run_modelling.py

# Completar código en cada archivo

# Comprimir
zip -r spark.zip spark
```

3. Train

Ejecutar entrenamiento del modelo.

```ssh
docker run -v $PWD:/home/jovyan/SparkProjects/Project1/ --name spark_submit_run_pyspark_example pyspark-lab:latest

# Alternativa: eliminar contenedor cuando se detiene
docker run --rm -v $PWD:/home/jovyan/SparkProjects/Project1/ --name spark_submit_run_pyspark_example pyspark-lab:latest
```

4. Test

- En `titanic.py` actualizar `get_model()` con nombre de modelo creado; en este caso se genera con fecha y hora.
- Comentar `train_titanic()` y descomentar `predict_titanic()`.
- Ejecutar nuevamente.

```ssh
docker run --rm -v "$PWD:/home/jovyan/SparkProjects/Project1/" --name spark_submit_run_pyspark_example pyspark-lab:latest
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
git commit -m "feat(02-pipeline-pyspark): añadir archivos al repo"
git push origin dev

git add .
git commit -m "fix(02-pipeline-pyspark): corregir README"
git push origin dev

# Merge con rama main:

git checkout main
git merge dev -m "feat(02-pipeline-pyspark): merge sin conflictos"
```

