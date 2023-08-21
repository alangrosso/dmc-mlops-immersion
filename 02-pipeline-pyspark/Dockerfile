FROM jupyter/pyspark-notebook:latest

USER root

RUN apt-get update && \
    apt-get install -y zip unzip && \
    apt-get install -y make

WORKDIR SparkProjects/Project1

ENTRYPOINT ["sh","spark_submit.sh"]

CMD []