# **MLFLOW & DVC**

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
dvc remote add -d dvc-agr './05-mlflow-dvc/external_storage/'

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

- Commit archivos.

```
git add 05-mlflow-dvc/
git commit -m "feat(05-mlflow-dvc): primera version codigo + data"

# crear tag para tracking de version de data
git tag -a 'v1' -m 'version-1 wine-quality.csv'

# Comandos adicionales

## eliminar un tag localmente 
git tag -d NOMBRE_DEL_TAG

## eliminar un tag específico
git push --delete origin NOMBRE_DEL_TAG

## eliminar el tag de GitHub (remotamente) después de haberlo eliminado localmente
git push origin :refs/tags/NOMBRE_DEL_TAG
```

- Ejecutar modelo.

```
python 05-mlflow-dvc/train.py
```

Verificar MLflow: `http://127.0.0.1:5000/`.

## Probar la funcionalidad de DVC

Eliminar un conjunto de datos.

```
# Remover train-data
rm -rf 05-mlflow-dvc/train_data/wine-quality.csv

# Remover train-data de cache
rm -rf .dvc/cache

# Devolver el archivo: 
dvc pull
```

- Verificar que se haya recuperado: 05-mlflow-dvc/train_data/wine-quality.csv.

## Nueva versión del dataset

Modificar un dataset existente.

```
# Remover train-data de Git
git rm -r --cached '05-mlflow-dvc/train_data/wine-quality.csv'
git commit -m "detener tracking 05-mlflow-dvc/train_data/wine-quality.csv" 

# Opción 1: Remover algunas filas del dataset
sed -i.old '2005,3004d' 05-mlflow-dvc/train_data/wine-quality.csv

# Opción 2:  Remover filas del dataset generando copia de respaldo
sed -i.bak '2005,3004d' 05-mlflow-dvc/train_data/wine-quality.csv

# Agregar a DVC
dvc add 05-mlflow-dvc/train_data/wine-quality.csv

# Agregar a git
git add 05-mlflow-dvc/train_data/wine-quality.csv.dvc

# Commit 
git commit -m "train_data: remover 1000 filas"

# Crear tag (v2) para tracking de data
git tag -a 'v2' -m 'version-2 wine-quality.csv remover 1000 filas'

# Push versión del dataset a DVC storage: 
dvc push

# Verificar push a DVC
ls -lR 05-mlflow-dvc/external_storage/

# Ejecutar modelo (actualizar VERSION)
python 05-mlflow-dvc/train.py
```

Verificar MLflow: `http://127.0.0.1:5000/`.