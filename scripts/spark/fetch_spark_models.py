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


# --- pipeline components ----
spark = sparknlp.start()

document = DocumentAssembler() \
    .setInputCol("text") \
    .setOutputCol("document")

sentence = SentenceDetectorDLModel.pretrained("sentence_detector_dl", "xx") \
    .setInputCols(["document"]) \
    .setOutputCol("sentence")

tokenizer = Tokenizer() \
    .setInputCols(["sentence"]) \
    .setOutputCol("token") 

lemma = LemmatizerModel.pretrained("lemma_proiel", "grc") \
    .setInputCols(["token"]) \
    .setOutputCol("lemma")

pipeline = Pipeline(stages=[document, sentence, tokenizer, lemma])

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
    # text = fin.readlines()


# --- inference ---
# List[List[single str]]

text_sample = "Δελφῶν οἶδα ἐγὼ οὕτω ἀκούσας γενέσθαι"
senteces = [
    [text_sample],
    [text_sample]
]

data = spark.createDataFrame([[text]]).toDF("text")
output = pipeline.fit(data).transform(data)

# --- export ---
lemmas = [row.result for row in output.select("lemma.result").collect()]

