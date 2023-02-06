import argparse
import json
import os
import re
from pathlib import Path
from typing import Any, Dict

import spacy
from spacy.scorer import Scorer
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.vocab import Vocab


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("pred_path", type=str)
    parser.add_argument("gold_path", type=str)
    parser.add_argument("dest", type=str)
    return parser


SPANS_KEY = "sc"
METRICS = {
    "TOK": "token_acc",
    "TAG": "tag_acc",
    "POS": "pos_acc",
    "MORPH": "morph_acc",
    "LEMMA": "lemma_acc",
    "UAS": "dep_uas",
    "LAS": "dep_las",
    "NER P": "ents_p",
    "NER R": "ents_r",
    "NER F": "ents_f",
    "TEXTCAT": "cats_score",
    "SENT P": "sents_p",
    "SENT R": "sents_r",
    "SENT F": "sents_f",
    "SPAN P": f"spans_{SPANS_KEY}_p",
    "SPAN R": f"spans_{SPANS_KEY}_r",
    "SPAN F": f"spans_{SPANS_KEY}_f",
    "SPEED": "speed",
}


def write_scores(scores: Dict[str, Any], path: str) -> None:
    """Writes scores to disk in spacy's json format.

    NOTE
    ----
    This is note my code, I took it from spaCy directly.
    """
    results = {}
    data = {}
    for metric, key in METRICS.items():
        if key in scores:
            if key == "cats_score":
                metric = (
                    metric + " (" + scores.get("cats_score_desc", "unk") + ")"
                )
            if isinstance(scores[key], (int, float)):
                if key == "speed":
                    results[metric] = f"{scores[key]:.0f}"
                else:
                    results[metric] = f"{scores[key]*100:.2f}"
            else:
                results[metric] = "-"
            data[re.sub(r"[\s/]", "_", key.lower())] = scores[key]
    with open(path, "w") as out_file:
        json.dump(data, out_file)


def main() -> None:
    # Parsing commandline arguments
    parser = create_parser()
    args = parser.parse_args()
    out_path = args.dest
    pred_path = args.pred_path
    gold_path = args.gold_path
    # Making sure that the folder exists
    Path(os.path.dirname(out_path)).mkdir(parents=True, exist_ok=True)
    # We load a reference model so the scorer knows what and where to evaluate.
    reference_model = spacy.load("grc_dep_treebanks_trf")
    scorer = Scorer(nlp=reference_model)
    pred_db = DocBin().from_disk(pred_path)
    gold_db = DocBin().from_disk(gold_path)
    pred_docs = pred_db.get_docs(reference_model.vocab)
    gold_docs = gold_db.get_docs(reference_model.vocab)
    examples = [
        Example(predicted=pred, reference=gold)
        for pred, gold in zip(pred_docs, gold_docs)
    ]
    scores = scorer.score(examples=examples)
    write_scores(scores, path=out_path)
