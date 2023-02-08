"""Script that fixes CLTK's punctuation.
"""
import os

from scripts.cltk.utils import fix_punctuation
from scripts.conllu.file import read_conllu_df, write_conllu_df

CONLLU_PATH = "corpus/conllu"


def main() -> None:
    for dataset in ["proiel", "perseus", "joint"]:
        in_path = os.path.join(CONLLU_PATH, f"{dataset}.conllu")
        gold_table = read_conllu_df(in_path)
        pred_table = read_conllu_df(
            os.path.join("predictions/cltk", f"{dataset}.conllu")
        )
        pred_table = fix_punctuation(pred_table)
        pred_table["FORM"] = gold_table["FORM"]
        # pred_table["ID"] = gold_table["ID"]
        write_conllu_df(
            pred_table,
            os.path.join(f"predictions/cltk/{dataset}_fixed.conllu"),
            separate_lines=False,
        )


if __name__ == "__main__":
    main()
