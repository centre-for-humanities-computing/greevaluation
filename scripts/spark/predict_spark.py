"""Produces predictions with SparkNLP in the form of CONLLU-U
"""

import os
from typing import List
from pathlib import Path
import pandas as pd
import sparknlp
from spark_pipelines import pipe_spark_perseus
from utils import load_conllu, CONLLU_FIELDS, fix_punctuation

# --- data ---
TEXT_DIR = "corpus/text_sents"
GOLD_DIR = "corpus/conllu"
OUT_DIR = "predictions/spark"


def main() -> None:
    # Ensure output path exists
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    # Initialize Spark pipeline
    spark = sparknlp.start()
    pipeline = pipe_spark_perseus()
    for dataset in ["proiel", "perseus", "joint"]:
        print(f" - Predicting: {dataset}")
        # Loading dataset
        path = os.path.join(TEXT_DIR, f"{dataset}.txt")
        with open(path) as in_file:
            # Has to be list of lists
            sentences: List[List[str]] = [[sent] for sent in in_file]
        # Wranling data into a Spark dataframe
        data = spark.createDataFrame(sentences).toDF("text")
        output = pipeline.fit(data).transform(data)
        # Collecting lemmas
        lemmas = [
            row.result for row in output.select("lemma.result").collect()
        ]
        # Flattening
        lemmas = [lemma for sentence in lemmas for lemma in sentence]
        # Collecting upos tags
        upos = [row.result for row in output.select("pos.result").collect()]
        upos = [pos for sentence in upos for pos in sentence]
        # Loading gold standard
        gold = load_conllu(os.path.join(GOLD_DIR, f"{dataset}.conllu"))
        # Putting predictions into a CONLL-U format
        pred_conllu = pd.DataFrame(columns=CONLLU_FIELDS)
        pred_conllu["LEMMA"] = lemmas
        pred_conllu["FORM"] = lemmas
        pred_conllu["UPOS"] = upos
        pred_conllu["ID"] = 0
        pred_conllu = fix_punctuation(pred_conllu)
        pred_conllu["ID"] = gold["ID"]
        pred_conllu["FORM"] = gold["FORM"]
        # Getting the columns in the right order
        # This also makes sure that all of them are there
        pred_conllu = pred_conllu[CONLLU_FIELDS]
        out_path = os.path.join(OUT_DIR, f"{dataset}.conllu")
        print(f" - Saving {dataset}")
        pred_conllu.to_csv(
            out_path, sep="\t", na_rep="_", header=False, index=False
        )


if __name__ == "__main__":
    main()

# written = 0

# with open("perseus_pred.txt", "w") as f:
# for i in range(len(lemmas)):
# gold_lemma = gold["LEMMA"][i]
# pred_lemma = lemmas[i]
# f.write(f"Index: [{i}] | Gold: {gold_lemma} | Pred: {pred_lemma}\n")
