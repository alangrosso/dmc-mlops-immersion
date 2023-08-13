# **Continuous Integration con Github**

Ejecutar test de código mediante un workflow de CI.

## **Ambiente virtual**

### virtualenv

Crear ambiente virtual:

```ssh
python3.10 -m venv py_env
source py_env/bin/activate
pip install -r requirements.txt
```

### Conda

Instalar Miniconda / Anaconda.

## **Desarrollo**

    a. Test unitarios

```ssh
# Todos los test
pytest tests/ . -v --disable-warnings

# Testear un archivo
pytest tests/test_math_func.py -v --disable-warnings

# Testear una función del archivo
pytest tests/test_math_func.py::test_add -v --disable-warnings
```

    b. Code Coverage

```ssh
# Coverage de todos los test   
pytest --cov=src tests/ -v --disable-warnings

#
pytest --cov=src tests/ -v --disable-warnings --cov-report term-missing
```

    c. Linting

```ssh
# Evaluamos todo el código
flake8 src/ tests/

# Obtener comentarios sobre las actualizaciones que se deben realizar al código
pylint tests/test_math_func.py

# Limpiar automáticamente el código.
autopep8 --in-place --aggressive --aggressive tests/test_math_func.py
```

## **Workflow Github**

Crear workflow que se desencadene cuando se produzca un evento en el repositorio. En este ejemplo, permite realizar test sobre el código cada vez que se realiza alguna modificación.

```ssh
# Directorio
mkdir .github
cd .github
mkdir workflows
cd workflows
# Archivo que detecta cambios en el código y lo ejecuta
touch ci_tests.yaml
```

En el archivo `workflow.yaml` generar el flujo de trabajo que se desea implementar.

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
git commit -m "feat(01-ci-github): añadir archivos al repo"
git push origin dev

# Merge con rama main:

git checkout main
git merge dev -m "merge 01-ci-github sin conflictos"
```