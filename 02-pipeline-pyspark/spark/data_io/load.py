from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StructType
from pyspark.ml import PipelineModel

from datetime import datetime
from utils.constant import *


def get_data(spark: SparkSession, path: str) -> DataFrame:
    df = spark.read.parquet(path)
    return df


def get_data_csv(spark: SparkSession, path: str) -> DataFrame:
    df = spark.read.option("header", True).csv(path)
    return df


def get_data_csv_set_schema(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    df = spark.read.csv(path, header=True, schema=schema)
    return df


def df_writer(df: DataFrame, path: str):
    df.write.mode('overwrite').parquet(path)


def df_shape(df: DataFrame):
    print((df.count(), len(df.columns)))
    print("SHAPE OF DATAFRAME: (ABOVE)")


def convert_parquet_to_csv(spark: SparkSession, path_parquet: str, path_csv: str):
    df = get_data(spark, path_parquet)
    df.coalesce(1).write.mode('overwrite').csv(path_csv, header=True)


def model_writer(model, info):
    now = datetime.now()  # current date and time
    now_str = now.strftime("%Y%d%m_%H%M%S")

    model.save(info[pysparkml_model_path] + f"{now_str}/model")


def get_model(info, name):
    return PipelineModel.load(info[pysparkml_model_path] + f"{name}/model")
