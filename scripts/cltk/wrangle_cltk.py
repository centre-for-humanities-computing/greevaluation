"""Script that normalizes tokens in the gold standard
texts with CLTK's normalizer and fixes CLTK's punctuation.
"""
import os

from utils import load_conllu, fix_punctuation

CONLLU_PATH = "corpus/conllu"


def main() -> None:
    for dataset in ["proiel", "perseus", "joint"]:
        in_path = os.path.join(CONLLU_PATH, f"{dataset}.conllu")
        gold_table = load_conllu(in_path)
        gold_table["MISC"] = "_"
        out_path = os.path.join(CONLLU_PATH, f"{dataset}_norm.conllu")
        gold_table.to_csv(out_path, sep="\t", index=False, header=False)
        pred_table = load_conllu(
            os.path.join("predictions/cltk", f"{dataset}.conllu")
        )
        pred_table = fix_punctuation(pred_table)
        pred_table["FORM"] = gold_table["FORM"]
        pred_table.to_csv(
            os.path.join("predictions/cltk", f"{dataset}_fixed.conllu"),
            sep="\t",
            index=False,
            header=False,
        )


if __name__ == "__main__":
    main()
