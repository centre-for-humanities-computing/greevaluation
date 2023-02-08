"""Script that removes the MISC column from the corpus CONLL-U files and saves them as _norm.
"""
import argparse
import os

from file import read_conllu_df, write_conllu_df

CONLLU_PATH = "corpus/conllu"


def main(separate_lines: bool) -> None:
    for dataset in ["proiel", "perseus", "joint"]:
        in_path = os.path.join(CONLLU_PATH, f"{dataset}.conllu")
        gold_table = read_conllu_df(in_path)
        gold_table["MISC"] = "_"
        out_path = os.path.join(CONLLU_PATH, f"{dataset}_norm.conllu")
        write_conllu_df(
            gold_table, path=out_path, separate_lines=separate_lines
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lines", action="store_true")
    parser.add_argument("--no-lines", dest="lines", action="store_false")
    parser.set_defaults(lines=True)
    args = parser.parse_args()
    main(separate_lines=args.lines)
