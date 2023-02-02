"""
"""
import os

from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

import sparknlp
from sparknlp.annotator import *
from sparknlp.common import *
from sparknlp.base import *
from sparknlp.pretrained import ResourceDownloader
from sparknlp.training import CoNLLU

from scripts.spark.spark_pipelines import pipe_spark_perseus, pipe_spark_proiel


# --- pipeline initialization ----
spark = sparknlp.start()
pipeline = pipe_spark_perseus()

# --- data ---
TEXT_DIR = "/work/greevaluation/corpus/text_sents"

# for dataset in ["proiel", "perseus", "joint"]:
#     print(f" - Predicting: {dataset}")
#     path = os.path.join(RAW_DIR, f"{dataset}.txt")
#     with open(path) as in_file:
#         text = in_file.read()

path = os.path.join(TEXT_DIR, 'proiel.txt')
with open(path) as fin:
    text = fin.read()

# List[List[single str]]
sentences = text.split('\n')
sentences = [[sent] for sent in sentences]

# --- inference ---
data = spark.createDataFrame(sentences).toDF("text")
output = pipeline.fit(data).transform(data)

# --- export ---
lemmas = [row.result for row in output.select("lemma.result").collect()]
pos = [row.result for row in output.select("pos.result").collect()]