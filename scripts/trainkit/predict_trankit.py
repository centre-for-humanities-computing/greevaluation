"""
"""
import os
from trankit import Pipeline

# can't be loaded/used at the same time
# otehrwise rases a KeyError
nlp_proiel = Pipeline('ancient-greek')
nlp_perseus = Pipeline('ancient-greek-perseus')


RAW_DIR = "corpus/text"
OUT_DIR = "predictions/trankit"


if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)


def main() -> None:
    nlp_proiel = Pipeline('ancient-greek')

    for dataset in ["proiel", "perseus", "joint"]:
        print(f" - Predicting: {dataset}")
        path = os.path.join(RAW_DIR, f"{dataset}.txt")
        with open(path) as in_file:
            text = in_file.read()

        doc = nlp_proiel(text)
        doc = nlp.analyze(text)
        print(" - Saving")
        save_conllu(doc, path=os.path.join(OUT_DIR, f"{dataset}.conllu"))
    print("DONE")