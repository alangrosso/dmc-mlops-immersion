import pandas as pd
import numpy as np
import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
# from dotenv import load_dotenv
import mlflow
import mlflow.sklearn
import logging
import warnings
import sys
import pdb
import os

# load_dotenv()

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# Mlflow tracking uri
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Get url from DVC
import dvc.api

print('Directorio: ', os.getcwd())

PATH_REPO = os.getcwd()
print('Repo: ', PATH_REPO)
PATH_DATOS = os.path.join('05-mlflow-dvc', 'train_data', 'wine-quality.csv')
print('Datos: ', PATH_DATOS)

VERSION = 'v1'  # tag or git-commit | actualizar
print('Version: ', VERSION)

hora_actual = datetime.datetime.now()
hora_actual_str = hora_actual.strftime("%Y%m%d-%H%M%S")
run_name = 'train-' + hora_actual_str

data_url = dvc.api.get_url(
    path=PATH_DATOS,
    repo=PATH_REPO,
    rev=VERSION
)
print('Data url: ', data_url)

mlflow.set_experiment('wine_quality_demo')

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(18)

    # tracking_uri = mlflow.get_tracking_uri()
    # print("Tracking uri: {}".format(tracking_uri))
    # artifact_uri = mlflow.get_artifact_uri()
    # print("Artifact uri: {}".format(artifact_uri))
    # registry_uri = mlflow.get_registry_uri()
    # print("Registry uri: {}".format(registry_uri))

    # Read the wine-quality csv file from the remote repository
    # pdb.set_trace()
    data = pd.read_csv(data_url, sep=",")
    print('Número de filas del dataset: ', data.shape[0])
    print('Número de columnas del dataset: ', data.shape[1])

    feature_cols = ['volatile acidity', 'citric acid', 'residual sugar', 'chlorides', 'total sulfur dioxide', 'quality']
    data = data[feature_cols]

    # Log data params
    mlflow.log_param('run_name', run_name)
    mlflow.log_param('data_url', data_url)
    mlflow.log_param('data_version', VERSION)
    mlflow.log_param('input_rows', data.shape[0])
    mlflow.log_param('ipput_cols', data.shape[1])

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    # Log artifacts: columns used for modeling
    cols_x = pd.DataFrame(list(train_x.columns))
    cols_x.to_csv('05-mlflow-dvc/features.csv', header=False, index=False)
    mlflow.log_artifact('05-mlflow-dvc/features.csv')

    cols_y = pd.DataFrame(list(train_y.columns))
    cols_y.to_csv('05-mlflow-dvc/targets.csv', header=False, index=False)
    mlflow.log_artifact('05-mlflow-dvc/targets.csv')

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.001
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2

    # train
    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=15)
    lr.fit(train_x, train_y)

    # predict
    predicted_qualities = lr.predict(test_x)

    # metrics
    rmse, mae, r2 = eval_metrics(test_y, predicted_qualities)
    mlflow.log_param('rmse', rmse)
    mlflow.log_param('mae', mae)
    mlflow.log_param('r2', r2)
    mlflow.log_param('alpha', alpha)
    mlflow.log_param('l1_ratio', l1_ratio)
    print("metrics")
    print("--------")
    print("rmse", rmse)
    print("mae", mae)
    print("r2", r2)
