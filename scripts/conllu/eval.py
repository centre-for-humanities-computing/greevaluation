import os
from pathlib import Path
import argparse
import json
from typing import Dict

from _eval import load_conllu_file, evaluate


def to_spacy_metrics(results) -> Dict[str, float]:
    """Maps UDeps' metrics to SpaCy ones."""
    metrics = {
        "token_acc": results["Tokens"].aligned_accuracy,
        "tag_acc": results["XPOS"].aligned_accuracy,
        "pos_acc": results["UPOS"].aligned_accuracy,
        "morph_acc": results["UFeats"].aligned_accuracy,
        "lemma_acc": results["Lemmas"].aligned_accuracy,
        "dep_uas": results["UAS"].aligned_accuracy,
        "dep_las": results["LAS"].aligned_accuracy,
        "sents_p": results["Sentences"].precision,
        "sents_r": results["Sentences"].recall,
        "sents_f": results["Sentences"].f1,
    }
    return metrics


def write_metrics(metrics: Dict[str, float], path: str) -> None:
    """Writes metrics to disc in JSON format."""
    if not path.endswith(".json"):
        raise ValueError(
            f"Path: {path}, is not the right format, file extension has to be json"
        )
    # Making sure directory exists
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    with open(path, "w") as out_file:
        json.dump(metrics, out_file)


def create_parser() -> argparse.ArgumentParser:
    """Creates parser for main CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pred_path", help="Path to predictions.", type=str)
    parser.add_argument("gold_path", help="Path to gold standard.", type=str)
    parser.add_argument("dest", help="Path to output json file.", type=str)
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    # Loading files
    gold = load_conllu_file(args.gold_path)
    pred = load_conllu_file(args.pred_path)
    # Evaluating prediction
    results = evaluate(gold_ud=gold, system_ud=pred)
    # Turning it into spacy metrics format
    results = to_spacy_metrics(results)
    # Writing them to given path
    write_metrics(metrics=results, path=args.dest)


if __name__ == "__main__":
    main()
