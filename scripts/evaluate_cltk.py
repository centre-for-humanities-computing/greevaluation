import json
import os
import re
from pathlib import Path
from typing import Any, Dict

import cltk
import spacy
from spacy.scorer import Scorer
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.vocab import Vocab

PRED_DIR = "predictions/cltk/"
GOLD_DIR = "corpus/binary"
EVALUATION_DIR = "metrics"

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
    # We load a reference model so the scorer knows what and where to evaluate.
    reference_model = spacy.load("grc_dep_treebanks_trf")
    scorer = Scorer(nlp=reference_model)
    # We go throught the three datasets
    version = str(cltk.__version__).split()[-1]
    out_dir = os.path.join(EVALUATION_DIR, "cltk", version)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for dataset in ["perseus", "proiel", "joint"]:
        pred_path = os.path.join(PRED_DIR, f"{dataset}_fixed.spacy")
        gold_path = os.path.join(GOLD_DIR, f"{dataset}_norm.spacy")
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
