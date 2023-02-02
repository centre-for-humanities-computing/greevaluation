"""
Evaluate udpipe models using spacy.Scorer
"""
import os
import re
import json
from typing import Any, Dict

import spacy
from spacy.scorer import Scorer
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.vocab import Vocab


PRED_DIR = "predictions/udpipe"
GOLD_DIR = "corpus/binary"
EVALUATION_DIR = "metrics"


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


def main():
    reference_model = spacy.load("grc_dep_treebanks_trf")
    scorer = Scorer(nlp=reference_model)

    # version hardcoded following
    # https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3131
    version = "2.5.0"

    for model in ["grc-perseus", "grc-proiel"]:

        out_dir = os.path.join(EVALUATION_DIR, model, version)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        for dataset in ["perseus", "proiel", "joint"]:
            pred_path = os.path.join(PRED_DIR, f"{model}_{dataset}.spacy")
            gold_path = os.path.join(GOLD_DIR, f"{dataset}.spacy")
            pred_db = DocBin().from_disk(pred_path)
            gold_db = DocBin().from_disk(gold_path)
            pred_docs = pred_db.get_docs(reference_model.vocab)
            gold_docs = gold_db.get_docs(reference_model.vocab)
            examples = [
                Example(predicted=pred, reference=gold)
                for pred, gold in zip(pred_docs, gold_docs)
            ]
            scores = scorer.score(examples=examples)
            out_path = os.path.join(out_dir, f"{dataset}.json")
            write_scores(scores, path=out_path)


if __name__ == "__main__":
    main()
