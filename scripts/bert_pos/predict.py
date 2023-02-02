"""Predicts tags with the Ancient Greek BERT POS tagger and saves them to jsonl files."""
from typing import List, Tuple
import os
from pathlib import Path

import pandas as pd
from flair.models import SequenceTagger
from flair.data import Sentence

from utils import load_conllu

GOLD_DIR = "corpus/conllu/"
OUT_DIR = "predictions/bert_pos/"


def load_model() -> SequenceTagger:
    """Loads model from list."""
    working_dir = os.getcwd()
    os.chdir("models/bert_pos/Ancient-Greek-BERT")
    tagger = SequenceTagger.load("SuperPeitho-FLAIR-v2/final-model.pt")
    os.chdir(working_dir)
    return tagger


def sentencize(table: pd.DataFrame) -> List[str]:
    """Sentencizes Document based on CONLL-U table."""
    sentences: List[str] = []
    sentence = ""
    n_tokens = len(table.index)
    for i_token in range(n_tokens):
        is_sentence_end = (i_token < (n_tokens - 1)) and (
            table.iloc[i_token + 1]["ID"] < table.iloc[i_token]["ID"]
        )
        sentence += table.iloc[i_token]["FORM"] + " "
        if is_sentence_end:
            sentences.append(sentence)
            sentence = ""
    return sentences


def predict_tags(
    tagger: SequenceTagger, sentences: List[str]
) -> Tuple[List[str], List[str]]:
    """Returns tuple of tokens with pos tags."""
    tokens = []
    tags = []
    for sentence in sentences:
        flair_sent = Sentence(sentence)
        tagger.predict(flair_sent)
        for token in flair_sent:
            tokens.append(token.text)
            tags.append(token.tag)
    return tokens, tags


def main() -> None:
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    tagger = load_model()
    for dataset in ["proiel", "perseus", "joint"]:
        print(f" - Predicting: {dataset}")
        table = load_conllu(os.path.join(GOLD_DIR, f"{dataset}.conllu"))
        sentences = sentencize(table)
        pred = pd.DataFrame()
        pred["form"], pred["pos"] = predict_tags(tagger, sentences)
        print(" - Saving")
        pred.to_json(
            os.path.join(OUT_DIR, f"{dataset}.jsonl"),
            orient="records",
            lines=True,
        )
    print("DONE")


if __name__ == "__main__":
    main()
