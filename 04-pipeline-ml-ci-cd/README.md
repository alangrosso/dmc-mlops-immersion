# **Pipeline Machine Learning**

`genre_classification`: predecir el genero musical de una canción.

## **Pipeline ML**

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

## **Docker**

Crear red de Docker.

```ssh
docker network create deploy_net
```

Crear backend de Postgres.

```ssh
docker run --network deploy_net --expose=5432 -p 5432:5432 -d -v $PWD/pg_data_1/:/var/lib/postgresql/data/ --name pg_mlflow -e POSTGRES_USER='user_pg' -e POSTGRES_PASSWORD='pass_pg' postgres
```

Crear imagen de Docker. Archivos de configuración: `Dockerfile` y `deploy-script.sh`.

```ssh
docker build -t mlflow_deploy .
```

Correr contenedor con MLFlow. Actualizar archivo: `local.env` (variable `default_artifact_root`).

```ssh
docker run -d -p 7755:5000 -v $PWD/container_artifacts:$PWD/container_artifacts --env-file local.env --network deploy_net --name test mlflow_deploy
```

Verificar MLflow: `http://0.0.0.0:5000/`

## **Github**

Configurar archivos para Github:

```ssh
/config.yaml

evaluate/run.py
```

Agregar secretos en GitHub:

- Accede a tu repositorio: Inicia sesión en tu cuenta de GitHub y navega hasta el repositorio en el que deseas agregar los secretos.

- Abre la pestaña "Settings" (Configuración): En la parte superior de la página de tu repositorio, haz clic en la pestaña "Settings" (Configuración).

- Navega a "Secrets" (Secretos): En el menú de la izquierda, selecciona la opción "Secrets" (Secretos).

- Haz clic en "New repository secret" (Nuevo secreto de repositorio): En la página de secretos, verás un botón verde llamado "New repository secret" (Nuevo secreto de repositorio). Haz clic en él para agregar un nuevo secreto.

- Ingresa el nombre y el valor del secreto: Deberás proporcionar un nombre descriptivo para el secreto en el campo "Name" (Nombre) y el valor del secreto en el campo "Value" (Valor).

- Haz clic en "Add secret" (Agregar secreto): Una vez que hayas ingresado el nombre y el valor del secreto, haz clic en el botón "Add secret" (Agregar secreto) para guardar el secreto.

- Repite el proceso según sea necesario: Puedes agregar tantos secretos como desees repitiendo los pasos anteriores.

- Usa los secretos en tus flujos de trabajo: Una vez que hayas agregado los secretos, puedes acceder a ellos en tus flujos de trabajo de GitHub Actions utilizando la sintaxis ${{ secrets.NOMBRE_DEL_SECRETO }}, donde "NOMBRE_DEL_SECRETO" es el nombre que asignaste al secreto.

Crear archivos para CI y configurar workflow:

```ssh
# Crear carpetas
mkdir .github
cd .github
mkdir workflows
cd workflows

# Crear yaml
touch cml.yaml
```

Subir pipeline a Github.

```ssh
# Crear repo

# Iniciar

git init
git pull

git branch dev
git checkout dev

git add .
git commit -m "feat(04-pipeline-ml-ci-cd): añadir archivos al repo"
git push origin dev

git add .
git commit -m "fix(04-pipeline-ml-ci-cd): corregir cml.yaml y README"
git push origin dev

# Merge con rama main:

git checkout main
git merge dev -m "feat(04-pipeline-ml-ci-cd): merge sin conflictos"
```
