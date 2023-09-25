# **MLFLOW & DVC**

Mlflow y DVC con Docker.

## Track & Push a DVC storage

- Instalar DVC.

```
# Instalar
pip install dvc==2.54.0

# Cli de DVC
sudo wget \
       https://dvc.org/deb/dvc.list \
       -O /etc/apt/sources.list.d/dvc.list
wget -qO - https://dvc.org/deb/iterative.asc | gpg --dearmor > packages.iterative.gpg
sudo install -o root -g root -m 644 packages.iterative.gpg /etc/apt/trusted.gpg.d/
rm -f packages.iterative.gpg
sudo apt update
sudo apt install dvc==2.54.0
```

- Configurar DVC.

```
# Inicializar (en directorio de repositorio)
git init
dvc init

# Establecer storage (en este caso: local)
mkdir 05-mlflow-dvc/external_storage/
dvc remote add -d dvc-agr 05-mlflow-dvc/external_storage/

# Verificar storages
cat .dvc/config
```

- Datos a utilizar: `train_data/wine-quality.csv`.

- Tracking train_data con DVC:

```
# Agregar data a Storage (DVC)
dvc add 05-mlflow-dvc/train_data/wine-quality.csv

# Trackear metadata con git
git add 05-mlflow-dvc/train_data/wine-quality.csv.dvc 05-mlflow-dvc/train_data/.gitignore

# Push 
dvc push

# Verificar push a DVC:
ls -lR 05-mlflow-dvc/external_storage/
```

- Verificar en `train_data/`: 

05-mlflow-dvc/train_data/wine-quality.csv.dvc
.gitignore (no trackear wine-quality.csv a git)

- Agregar archivos a Github

```
git add 05-mlflow-dvc/
git commit -m "feat(05-mlflow-dvc): primera version codigo + data"

# crear tag para tracking de version de data
git tag -a 'v1' -m 'version-1 wine-quality.csv'
```




```

```



```

```



## Test DVC functionality by removing the dataset



```
# remove the train-data file: 
rm -rf train_data/wine-quality.csv

# also, remove from the cache: 
rm -rf .dvc/cache

# bring back the file: 
dvc pull
```

- verify train_data/wine-quality.csv is back

## New version of the dataset

```
# alter the file by removing some rows: 
sed -i '.old' '2005,3004d' train_data/wine-quality.csv

# add to dvc (repeated procedure): 
dvc add train_data/wine-quality.csv

# add to git associated .dvc file (repeated procedure): 
git add train_data/wine-quality.csv.dvc

# commit changes: 
git commit -m "train_data: remove 1000 rows"

# create a tag (v2) for later tracking of your data: 
git tag -a 'v2' -m 'version-2 wine-quality.csv removed 1000 rows'

# push the version of your data to dvc storage: 
dvc push

# verify push to dvc: 
ls -lR external_storage/
```

## Put Mlflow in action

- Ejecutar Mlflow

```
# remove the dataset: 
rm -rf train_data/wine-quality.csv & rm -rf .dvc/cache

# reproduce dataset versions with dvc-api in: 
train.py
```

- train.py contains all mlflow tracking
- take a look in deploy-script.sh how to run mlflow server as a docker container
- go to mlflow-ui & look logged params, in my case: http://localhost:7755

### Notes to spin-up a mlflow docker container

```
# create docker network: 
docker network create cesar_net

# run a postgress container: 
docker run --network cesar_net --expose=5432 -p 5432:5432 -d -v $PWD/pg_data_1/:/var/lib/postgresql/data/ --name pg_mlflow -e POSTGRES_USER='user_pg' -e POSTGRES_PASSWORD='pass_pg' postgres

# build Dockerfile: 
docker build -t mlflow_cesar .
```

- modify env var default_artifact_root in local.env with your current directory

```
# run mlflow server container: 
docker run -d -p 7755:5000 -v $PWD/artifacts:$PWD/artifacts --env-file local.env --network cesar_net --name test mlflow_cesar
```

