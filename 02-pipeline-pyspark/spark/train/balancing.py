from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

from data_io.load import get_data, df_writer


def under_sampling(df_abt_init, to_under_class=0, labelCol="target"):
    df_abt_init = df_abt_init.orderBy(rand())  # randomize data
    df_abt_init = df_abt_init.checkpoint()

    df_abt_1 = df_abt_init.filter(col(labelCol) != to_under_class)
    class_minor_obs = df_abt_1.count()

    df_abt_0 = df_abt_init.filter(col(labelCol) == to_under_class) \
        .limit(class_minor_obs)

    df_abt = df_abt_1.union(df_abt_0)
    return df_abt


def stratify_sampling(df, labelCol, splitList=[0.8, 0.2], seed=20):
    zeros = df.filter(col(labelCol) == 0)
    ones = df.filter(col(labelCol) == 1)
    # split datasets into training and testing
    train0, test0 = zeros.randomSplit(splitList, seed=seed)
    train1, test1 = ones.randomSplit(splitList, seed=seed)
    # stack datasets back together
    train = train0.union(train1)
    # train = train.checkpoint()

    test = test0.union(test1)
    # test = test.checkpoint()

    return train, test
