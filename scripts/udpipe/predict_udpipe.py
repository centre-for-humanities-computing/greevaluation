"""
Generate predictions of the test sets
"""

import os
from spacy.tokens import DocBin
import spacy_udpipe


RAW_DIR = "corpus/text"
OUT_DIR = "predictions/udpipe"


def main():

    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    for model in ["grc-perseus", "grc-proiel"]:
        for dataset in ["proiel", "perseus", "joint"]:
            print(f" - Predicting: {dataset}")
            # load test fold
            test_data_path = os.path.join(RAW_DIR, f"{dataset}.txt")
            with open(test_data_path) as in_file:
                text = in_file.read()
            # predict
            nlp = spacy_udpipe.load(model)
            doc = nlp(text)
            # export predictions
            doc_bin = DocBin()
            doc_bin.add(doc)
            outpath = os.path.join(OUT_DIR, f"{model}_{dataset}.spacy")
            doc_bin.to_disk(outpath)
    
    return None


if __name__ == "__main__":
    main()