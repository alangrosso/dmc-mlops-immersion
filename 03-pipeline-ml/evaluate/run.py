import os
import shutil
import argparse
import itertools
import logging
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, confusion_matrix, ConfusionMatrixDisplay

import mlflow

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def use_artifact(args):
    query = f"tag.step='{args.input_data_step}' and tag.current='1'"
    retrieved_run = mlflow.search_runs(experiment_ids=[mlflow.active_run().info.experiment_id],
                                       filter_string=query,
                                       order_by=["attributes.start_time DESC"],
                                       max_results=1)["run_id"][0]
    logger.info("retrieved run: " + retrieved_run)
    local_path = mlflow.tracking.MlflowClient().download_artifacts(retrieved_run, args.test_data)
    logger.info("input_artifact: " + args.test_data + " at " + local_path)
    return local_path


def use_model_artifact(args):
    query = f"tag.step='{args.input_model_step}' and tag.current='1'"
    retrieved_run = mlflow.search_runs(experiment_ids=[mlflow.active_run().info.experiment_id],
                                       filter_string=query,
                                       order_by=["attributes.start_time DESC"],
                                       max_results=1)["run_id"][0]
    logger.info("retrieved run: " + retrieved_run)
    model = mlflow.sklearn.load_model(f"runs:/{retrieved_run}/{args.model_export}")
    logger.info("retrieved model artifact: " + args.model_export)
    return model


def go(args):
    logger.info("Downloading and reading test artifact")
    test_data_path = use_artifact(args)
    df = pd.read_csv(test_data_path, low_memory=False)

    # Extract the target from the features
    logger.info("Extracting target from dataframe")
    X_test = df.copy()
    y_test = X_test.pop("genre")

    logger.info("Downloading and reading the exported model")
    pipe = use_model_artifact(args)

    # pipe = mlflow.sklearn.load_model(model_export_path)

    used_columns = list(itertools.chain.from_iterable([x[2] for x in pipe['preprocessor'].transformers]))
    pred_proba = pipe.predict_proba(X_test[used_columns])
    pred = pipe.predict(X_test[used_columns])

    logger.info("Scoring")
    score = roc_auc_score(y_test, pred_proba, average="macro", multi_class="ovo")

    mlflow.log_metric("AUC", score) # comentar para utilizar código en github: Continuos ML
    # with open("./metrics.txt", 'w') as outfile:
    #     outfile.write("AUC Test Dataset: %2.5f%%\n" % score)
    #     mlflow.log_metric("AUC", score)

    base_name_img = "./img/"
    if not os.path.exists(base_name_img):
        os.mkdir(base_name_img)

    logger.info("Computing confusion matrix")
    cm = confusion_matrix(y_true=y_test, 
        y_pred=pred, 
        labels=pipe.classes_)
    fig_cm, sub_cm = plt.subplots(figsize=(13, 13))
    cm_obj = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=pipe.classes_,
        )
    cm_obj.plot(ax=sub_cm, 
        xticks_rotation=90
        )
    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix\n', fontsize=25)
    fig_cm.savefig(base_name_img + 'confusion_matrix.png')

    mlflow.log_artifacts(base_name_img, "img")
    shutil.rmtree(base_name_img) # comentar para utilizar código en github: Continuos ML
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test the provided model on the test artifact",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--step", type=str, help="Current Step Name", required=True
    )

    parser.add_argument(
        "--input_model_step", type=str, help="Input Model Step Name", required=True
    )

    parser.add_argument(
        "--model_export",
        type=str,
        help="Fully-qualified artifact name for the exported model to evaluate",
        required=True,
    )

    parser.add_argument(
        "--input_data_step", type=str, help="Input Data Step Name", required=True
    )

    parser.add_argument(
        "--test_data",
        type=str,
        help="Fully-qualified artifact name for the test data",
        required=True,
    )

    args = parser.parse_args()

    with mlflow.start_run() as run:
        go(args)
        mlflow.set_tag("step", args.step)
        mlflow.set_tag("current", "1")
