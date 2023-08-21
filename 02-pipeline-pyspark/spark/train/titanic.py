from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *

import os
from datetime import datetime

from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import RandomForestClassifier, LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator, \
    MulticlassClassificationEvaluator
from utils.constant import *
from data_io.load import model_writer, get_model
from train.evaluate import get_metric

def train_titanic(spark: SparkSession, info):
    print("TRAINING ...", flush=True)

    schema = StructType(
        [StructField("PassengerId", StringType()),
         StructField("Survival", DoubleType()),
         StructField("Pclass", DoubleType()),
         StructField("Name", StringType()),
         StructField("Sex", StringType()),
         StructField("Age", DoubleType()),
         StructField("SibSp", DoubleType()),
         StructField("Parch", DoubleType()),
         StructField("Ticket", StringType()),
         StructField("Fare", DoubleType()),
         StructField("Cabin", StringType()),
         StructField("Embarked", StringType())
         ])

    df_raw = spark \
        .read \
        .option("header", "true") \
        .schema(schema) \
        .csv(info[titanic_data_path] + "train.csv")

    df = df_raw.na.fill(0)

    sexIndexer = StringIndexer() \
        .setInputCol("Sex") \
        .setOutputCol("SexIndex") \
        .setHandleInvalid("keep")

    embarkedIndexer = StringIndexer() \
        .setInputCol("Embarked") \
        .setOutputCol("EmbarkedIndex") \
        .setHandleInvalid("keep")

    vectorAssembler = VectorAssembler() \
        .setInputCols(
        ["Pclass", "SexIndex", "Age", "SibSp", "Parch", "Fare", "EmbarkedIndex"]) \
        .setOutputCol("features")

    rf = RandomForestClassifier(
        featuresCol="features",
        labelCol='Survival',
        predictionCol="prediction",
        numTrees=50,
        maxDepth=11
    )

    rf_params = {param[0].name: param[1] for param in
                 rf.extractParamMap().items()}
    print("hyperparameters ->", flush=True)
    print(rf_params, flush=True)

    # lr = LogisticRegression(
    #     featuresCol="features",
    #     labelCol='Survival',
    #     predictionCol="prediction",
    #     maxIter=5,
    #     regParam=1,
    #     elasticNetParam=0,
    #     tol=0.001
    # )
    # lr_params = {param[0].name: param[1] for param in
    #              lr.extractParamMap().items()}
    # print("hyperparameters ->", flush=True)
    # print(lr_params, flush=True)

    pipeline = Pipeline().setStages(
        [sexIndexer, embarkedIndexer, vectorAssembler, rf]
    )

    trainDF, testDF = df.randomSplit([0.8, 0.2], seed=24)

    model = pipeline.fit(trainDF)
    df_pipeline_predicted = model.transform(testDF)
    df_pipeline_predicted \
        .select("PassengerId", "Survival", "prediction") \
        .show(55, truncate=False)

    for metric in ["areaUnderROC", "areaUnderPR", "accuracy",
                   "weightedPrecision", "weightedRecall", "f1"]:
        metric_value = get_metric(
            df_pipeline_predicted,
            labelCol="Survival",
            predictionCol="prediction",
            metric=metric
        )
        print("metric -> ", metric, " ; value -> ", metric_value, flush=True)

    # save pyspark model
    model_writer(model, info)


def predict_titanic(spark: SparkSession, info):
    print("TESTING ...", flush=True)

    schema = StructType(
        [StructField("PassengerId", StringType()),
         StructField("Survival", DoubleType()),
         StructField("Pclass", DoubleType()),
         StructField("Name", StringType()),
         StructField("Sex", StringType()),
         StructField("Age", DoubleType()),
         StructField("SibSp", DoubleType()),
         StructField("Parch", DoubleType()),
         StructField("Ticket", StringType()),
         StructField("Fare", DoubleType()),
         StructField("Cabin", StringType()),
         StructField("Embarked", StringType())
         ])

    df_raw = spark \
        .read \
        .option("header", "true") \
        .schema(schema) \
        .csv(info[titanic_data_path] + "train.csv")

    df = df_raw.na.fill(0)

    model = get_model(info, "20231404_190543") # actualizar con nombre de modelo FECHA_DE_MODELO
    
    df_pipeline_predicted = model.transform(df)
    df_pipeline_predicted.select("PassengerId", "Survival", "prediction").show(
        55, truncate=False)

    for metric in ["areaUnderROC", "areaUnderPR", "accuracy",
                   "weightedPrecision", "weightedRecall", "f1"]:
        metric_value = get_metric(
            df_pipeline_predicted,
            labelCol="Survival",
            predictionCol="prediction",
            metric=metric
        )
        print("metric -> ", metric, " ; value -> ", metric_value, flush=True)


def run(spark: SparkSession, info):
    # ** 1. train a pyspark model
    train_titanic(spark, info)

    # ** 2. predict with a pyspark model
    # predict_titanic(spark, info)
