"""
"""
import os
import argparse
from trankit import Pipeline
from util import save_conllu


RAW_DIR = "corpus/text"
OUT_DIR = "predictions/trankit"


if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)


def main(pipeline, embedding) -> None:

    nlp = Pipeline(pipeline, embedding=embedding)

    for dataset in ["proiel", "perseus", "joint"]:
        print(f" - Predicting: {dataset}")
        path = os.path.join(RAW_DIR, f"{dataset}.txt")
        with open(path) as in_file:
            text = in_file.read()
        doc = nlp(text)
        tokens = doc['sentences'][0]['tokens']
        print(" - Saving")
        save_conllu(tokens, path=os.path.join(OUT_DIR, f"{dataset}_{pipeline}_{embedding}.conllu"))

    print("DONE")


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument('--model')
    ap.add_argument('--embedding')
    args = ap.parse_args()

    main(
        pipeline=args.model,
        embedding=args.embedding
    )


# #  --- test ---
# RAW_DIR = "corpus/text"
# OUT_DIR = "predictions/trankit"
# dataset = 'joint'

# nlp_perseus = Pipeline('ancient-greek-perseus')

# path = os.path.join(RAW_DIR, f"{dataset}.txt")
# with open(path) as in_file:
#     text = in_file.read()

# doc = nlp_perseus(text)
# tokens = doc['sentences'][0]['tokens']
# save_conllu(tokens, 'test.csv')