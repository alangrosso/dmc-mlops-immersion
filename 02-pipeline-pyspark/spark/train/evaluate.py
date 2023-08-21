from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.dataframe import DataFrame

from pyspark.ml.classification import RandomForestClassifier, LogisticRegression
from pyspark.ml import PipelineModel, Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from data_io.load import *
from utils.constant import *


def print_mc(info, matriz_conf, dataset_type="train"):
    matriz_conf = pd.DataFrame(matriz_conf)
    matriz_conf.index = ["Real_0", "Real_1"]
    matriz_conf.columns = ["Pred_0", "Pred_1"]
    # matriz_conf.to_csv(info + f"confusion_matrix/cm_{dataset_type}.csv", index=False)

    print(matriz_conf)


def evaluation(info, model, data, labelCol="default", dataset_type="train"):
    predictions = model.transform(data)
    evaluator = BinaryClassificationEvaluator(labelCol=labelCol, metricName="areaUnderROC")
    auc = evaluator.evaluate(predictions)
    print('Area Under ROC', auc)

    # EVALUATION
    y_true = predictions.select(labelCol).collect()
    y_pred = predictions.select('prediction').collect()
    print(classification_report(y_true, y_pred))

    matriz_conf = confusion_matrix(y_true, y_pred)
    print_mc(info, matriz_conf, dataset_type)


def get_metric(df_predictions, labelCol="target", predictionCol="prediction",
               metric="accuracy"):
    if metric in ["accuracy", "weightedPrecision", "weightedRecall", "f1"]:
        evaluator = MulticlassClassificationEvaluator(labelCol=labelCol,
                                                      predictionCol=predictionCol,
                                                      metricName=metric)
        value = evaluator.evaluate(df_predictions)
    elif metric in ["areaUnderROC", "areaUnderPR"]:
        evaluator = BinaryClassificationEvaluator(labelCol=labelCol,
                                                  metricName=metric)
        value = evaluator.evaluate(df_predictions)
    else:
        print("Do not exist Metric Name --> {}".format(metric))
    return value
