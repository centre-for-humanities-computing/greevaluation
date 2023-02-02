"""
Generate predictions of the test sets
"""

from typing import Optional, Dict, Any
import os
import spacy
import spacy_stanza
from spacy.scorer import Scorer
import re
from wasabi import Printer
from spacy import util
from spacy.training.corpus import Corpus
from pathlib import Path
from spacy.cli.evaluate import handle_scores_per_type
from spacy.language import Language
import srsly


def evaluate(
    nlp: Language,
    data_path: str,
    output: str,
    gold_preproc: bool = False,
    silent: bool = True,
    spans_key: str = "sc",
) -> Dict[str, Any]:
    msg = Printer(no_print=silent, pretty=not silent)
    data_path = util.ensure_path(data_path)
    output_path = util.ensure_path(output)
    if not Path(data_path).exists():
        msg.fail("Evaluation data not found", data_path, exits=1)
    corpus = Corpus(data_path, gold_preproc=gold_preproc)
    dev_dataset = list(corpus(nlp))
    reference_model = spacy.load("grc_dep_treebanks_trf")
    scorer = Scorer(nlp=reference_model)
    scores = nlp.evaluate(dev_dataset, scorer=scorer)
    metrics = {
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
        "SPAN P": f"spans_{spans_key}_p",
        "SPAN R": f"spans_{spans_key}_r",
        "SPAN F": f"spans_{spans_key}_f",
        "SPEED": "speed",
    }
    results = {}
    data = {}
    for metric, key in metrics.items():
        if key in scores:
            if key == "cats_score":
                metric = metric + " (" + scores.get("cats_score_desc", "unk") + ")"
            if isinstance(scores[key], (int, float)):
                if key == "speed":
                    results[metric] = f"{scores[key]:.0f}"
                else:
                    results[metric] = f"{scores[key]*100:.2f}"
            else:
                results[metric] = "-"
            data[re.sub(r"[\s/]", "_", key.lower())] = scores[key]

    msg.table(results, title="Results")
    data = handle_scores_per_type(scores, data, spans_key=spans_key, silent=silent)

    if output_path is not None:
        srsly.write_json(output_path, data)
        msg.good(f"Saved results to {output_path}")
    return data


GOLD_DIR = "corpus/binary"
OUT_DIR = "metrics"
STANZA_VERSION = "1.0.0"


def main():
    for model_name in ["perseus", "proiel"]:
        for dataset in ["proiel", "perseus", "joint"]:
            print(f" - Evaluating: {dataset}")
            nlp = spacy_stanza.load_pipeline("grc", package=model_name)
            gold_path = os.path.join(GOLD_DIR, f"{dataset}.spacy")
            out_dir = os.path.join(
                OUT_DIR,
                f"stanza-grc-{model_name}",
                STANZA_VERSION,
            )
            Path(out_dir).mkdir(parents=True, exist_ok=True)
            out_path = os.path.join(out_dir, f"{dataset}.json")
            evaluate(nlp, data_path=gold_path, output=out_path)


if __name__ == "__main__":
    main()
