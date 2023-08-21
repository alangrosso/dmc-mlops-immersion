
spark_submit_cmd="spark-submit --master local[*] --deploy-mode client --py-files spark.zip spark/run_modeling.py --root_path /home/jovyan/SparkProjects/Project1/source_data/ --checkpoint_path /home/jovyan/SparkProjects/Project1/source_data/checkpoints/"
eval $spark_submit_cmd