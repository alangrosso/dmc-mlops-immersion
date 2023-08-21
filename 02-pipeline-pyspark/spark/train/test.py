from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import PipelineModel, Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

from datetime import datetime


def create_dummy_model(spark, model_name):
    features_columns = ["f1", "f2", "f3", "f4"]

    df = create_dummy_data(spark)
    # df = df.withColumn('target', col('target').cast(IntegerType()).alias('target'))
    df = df.withColumn('target', col('target').cast(DoubleType()).alias('target'))

    # ML pipeline
    vectorAssembler = VectorAssembler().setInputCols(features_columns).setOutputCol("features")

    rf = RandomForestClassifier(numTrees=150, maxDepth=7, featureSubsetStrategy="auto", labelCol="target")

    pipeline = Pipeline().setStages([vectorAssembler, rf])
    model = pipeline.fit(df)
    # model_writer(model)

    df_predicted = model.transform(df)

    return df, df_predicted


def create_dummy_data(spark):
    df = spark.range(0, 15800)
    df = df.select("id", rand(seed=10).alias("f1"), randn(seed=27).alias("f2"),
                   rand(seed=14).alias("f3"), randn(seed=35).alias("f4"),
                   rand(seed=453).alias("target")) \
        .withColumn("target", round(col("target")))
    return df
