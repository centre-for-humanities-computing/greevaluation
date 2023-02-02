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
TEXT_DIR = "/work/greevaluation/corpus/text"

# for dataset in ["proiel", "perseus", "joint"]:
#     print(f" - Predicting: {dataset}")
#     path = os.path.join(RAW_DIR, f"{dataset}.txt")
#     with open(path) as in_file:
#         text = in_file.read()

path = os.path.join(TEXT_DIR, 'proiel.txt')
with open(path) as fin:
    text = fin.read()

# List[List[single str]]
# sentences = text.split('\n')
# sentences = [[sent] for sent in sentences]
sentences = [[text]]

# --- inference ---
data = spark.createDataFrame(sentences).toDF("text")
output = pipeline.fit(data).transform(data)

# --- export ---
tokens = [row.result for row in output.select("token.result").collect()]
sentences = [row.result for row in output.select("sentence.result").collect()]
lemmas = [row.result for row in output.select("lemma.result").collect()]
pos = [row.result for row in output.select("pos.result").collect()]

# sentence id
sentence_ids = output.select("token.metadata").collect()
sentence_ids  = [tok['sentence'] for tok in sentence_ids[0][0]]

# save this in conllu in some way
output_df = pd.DataFrame({
    'token': tokens[0],
    'lemma': lemmas[0],
    'pos': pos[0],
    'sentence_id': sentence_ids
})

tagged_df = pd.DataFrame([])
for sent_id, sent_annotations in output_df.groupby('sentence_id'):
    token_ids = list(range(1, len(sent_annotations) + 1))
    sent_annotations['id'] = token_ids
    sent_annotations = sent_annotations.drop('sentence_id', axis=1)
    tagged_df = tagged_df.append(sent_annotations)