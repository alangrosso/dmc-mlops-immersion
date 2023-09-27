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

## **Continuous Machine Learning (CML)**

Configurar archivos para Github:

```ssh
/config.yaml

evaluate/run.py
```

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

Al inicio de cada trabajo del workflow, GitHub crea automáticamente un secreto `GITHUB_TOKEN` único para usarlo en el workflow. Se usa GITHUB_TOKEN para autenticarse en el workflow.

Crear nueva rama para CML.

```ssh
git checkout -b cml
```

Subir pipeline a Github.

```ssh
git add 04-pipeline-ml-ci-cd/
git add .github/workflows/
git add .gitignore

git commit -m "feat(04-pipeline-ml-ci-cd): crear branch cml y agregar pipeline"
git push origin cml
```

Verificar que se haya ejecutado workflow.

```ssh
# Agregar files a dev
git checkout dev
git commit -m "fix(04-pipeline-ml-ci-cd): agregar files de branch cml a dev"
git push origin dev

# Merge con rama main:
git checkout main
git merge dev -m "feat(04-pipeline-ml-ci-cd): merge sin conflictos"
```