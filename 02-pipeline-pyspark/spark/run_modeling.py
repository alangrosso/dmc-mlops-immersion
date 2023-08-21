from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

import sys
import os
import argparse

from utils.constant import *
from train import titanic


def parse_cli_args():
    """
    Parse cli arguments
    returns a dictionary of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--root_path', action='store', dest=root_path, type=str,
                        help='Store', default=None)

    parser.add_argument('--checkpoint_path', action='store', 
                        dest=checkpoint_path, type=str,
                        help='Store', default=None)

    parser.add_argument('--app_env', action='store', dest=app_env, type=str,
                        help='Store', default=None)

    parser.add_argument('--year_month', action='store', dest=year_month,
                        type=str,
                        help='Store', default=None)

    parser.add_argument('--country', action='store', dest=country, type=str,
                        help='Store', default=None)

    parser.add_argument('--version', action='store', dest=version, type=str,
                        help='Store', default=None)

    parser.add_argument('--org', action='store', dest=org, type=str,
                        help='Store', default=None)

    known_args, unknown_args = parser.parse_known_args()
    known_args_dict = vars(known_args)
    return known_args_dict


if __name__ == '__main__':
    args = parse_cli_args()

    # Paths Data y Models
    # args[titanic_data_path] = f"{args[root_path]}/raw/"
    # args[titanic_data_path] = f"{args[root_path]}/raw_from_db/"
    # args[titanic_data_path] = f"{args[root_path]}/raw_parquet/"
    args[titanic_data_path] = f"{args[root_path]}/titanic_data/"
    args[pysparkml_model_path] = f"{args[root_path]}/pysparkml_model/"

    # Start Spark Environment
    spark = SparkSession.builder.getOrCreate()

    # Checkpointing tuning strategy
    sc = SparkContext.getOrCreate()
    # sc.setCheckpointDir(args[checkpoint_path])
    # sc.setLogLevel("WARN")
    sc.setLogLevel("ERROR")

    # # SPARK LOGIC
    # print("Hello World", "Spark pipeline !!")
    # print("python version --> ", sys.version)
    # print("pyspark version --> ", sc.version)
    # print("pyspark version --> ", spark.version)

    # TITANIC DEMO
    titanic.run(spark, args)
