"""Script for making CLTK predictions for all test sets."""
import os

from cltk import NLP
from scripts.cltk.utils import to_conllu
from scripts.conllu.file import write_conllu_df

RAW_DIR = "corpus/text"
OUT_DIR = "predictions/cltk"


def main() -> None:
    nlp = NLP(language="grc")
    for dataset in ["proiel", "perseus", "joint"]:
        print(f" - Predicting: {dataset}")
        path = os.path.join(RAW_DIR, f"{dataset}.txt")
        with open(path) as in_file:
            text = in_file.read()
        doc = nlp.analyze(text)
        doc_df = to_conllu(doc)
        print(" - Saving")
        write_conllu_df(
            doc_df, path=os.path.join(OUT_DIR, f"{dataset}.conllu")
        )
    print("DONE")


if __name__ == "__main__":
    main()
