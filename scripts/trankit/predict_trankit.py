"""Creates predictions with trankit.
"""
import os
import argparse
from trankit import Pipeline
from util import save_conllu


RAW_DIR = "corpus/text"
OUT_DIR = "predictions/trankit"


if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)


def main(pipeline_name: str, embedding_name: str) -> None:
    nlp = Pipeline(pipeline_name, embedding=embedding_name)

    for dataset in ["proiel", "perseus", "joint"]:
        print(f" - Predicting: {dataset}")
        path = os.path.join(RAW_DIR, f"{dataset}.txt")
        with open(path) as in_file:
            text = in_file.read()
        doc = nlp(text)
        predictions = [sentence["tokens"] for sentence in doc["sentences"]]
        predictions_flat = [
            token for sentence in predictions for token in sentence
        ]
        print(" - Saving")
        save_conllu(
            predictions_flat,
            path=os.path.join(
                OUT_DIR, f"{dataset}_{pipeline_name}_{embedding_name}.conllu"
            ),
        )

    print("DONE")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--embedding")
    args = ap.parse_args()

    main(pipeline_name=args.model, embedding_name=args.embedding)


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
