"""
Compiling Spark pretrained pipelines for Ancient Greek 
"""

import sparknlp
from sparknlp.annotator import *
from sparknlp.common import *
from sparknlp.base import *
from sparknlp.pretrained import ResourceDownloader


def pipe_spark_proiel():
    '''
    pos:
    https://nlp.johnsnowlabs.com/2022/05/01/pos_proiel_grc_3_0.html

    lemma:
    https://nlp.johnsnowlabs.com/2022/05/01/lemma_proiel_grc_3_0.html
    '''
    document = DocumentAssembler() \
        .setInputCol("text") \
        .setOutputCol("document")

    sentence = SentenceDetectorDLModel.pretrained("sentence_detector_dl", "xx") \
        .setInputCols(["document"]) \
        .setOutputCol("sentence")

    tokenizer = Tokenizer() \
        .setInputCols(["sentence"]) \
        .setOutputCol("token") 

    pos = PerceptronModel.pretrained("pos_proiel", "grc") \
        .setInputCols(["sentence", "token"]) \
        .setOutputCol("pos")

    lemma = LemmatizerModel.pretrained("lemma_proiel", "grc") \
        .setInputCols(["token"]) \
        .setOutputCol("lemma")

    pipeline = Pipeline(stages=[document, sentence, tokenizer, pos, lemma])

    return pipeline


def pipe_spark_perseus():
    '''
    pos:
    https://nlp.johnsnowlabs.com/2022/04/01/pos_perseus_grc_3_0.html

    lemma:
    https://nlp.johnsnowlabs.com/2022/03/31/lemma_perseus_grc_3_0.html
    '''
    document = DocumentAssembler() \
        .setInputCol("text") \
        .setOutputCol("document")

    sentence = SentenceDetectorDLModel.pretrained("sentence_detector_dl", "xx") \
        .setInputCols(["document"]) \
        .setOutputCol("sentence")

    tokenizer = Tokenizer() \
        .setInputCols(["sentence"]) \
        .setOutputCol("token") 

    pos = PerceptronModel.pretrained("pos_perseus", "grc") \
        .setInputCols(["sentence", "token"]) \
        .setOutputCol("pos")

    lemma = LemmatizerModel.pretrained("lemma_perseus", "grc") \
        .setInputCols(["token"]) \
        .setOutputCol("lemma")

    pipeline = Pipeline(stages=[document, sentence, tokenizer, pos, lemma])

    return pipeline
