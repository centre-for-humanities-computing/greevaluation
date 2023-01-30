# %%
import os

os.chdir("/home/au689890/Documents/Github/greevaluation")

# %%
from IPython import get_ipython  # type: ignore

ipython = get_ipython()  # type: ignore

ipython.magic("load_ext autoreload")  # type: ignore
ipython.magic("autoreload 2")  # type: ignore
# %%
from io import StringIO
import pandas as pd

# %%
# Columns in a CONLL-U file
CONLL_COLUMNS = [
    "word_id",
    "form",
    "lemma",
    "upos",
    "xpos",
    "feats",
    "head",
    "deprel",
    "deps",
    "misc",
]


def load_conllu(path: str) -> pd.DataFrame:
    """Reads a CONLL-U file into a Dataframe"""
    with open(path) as conllu_file:
        lines = []
        # I only append lines from the file that are not comments.
        for line in conllu_file:
            if not line.startswith("#"):
                lines.append(line)
    # Joining the lines
    conllu_text = "".join(lines)
    # Turning it into a stream so that pandas can read it as a file.
    text_stream = StringIO(conllu_text)
    # Reading conllu files to a dataframe
    df = pd.read_csv(text_stream, sep="\t", names=CONLL_COLUMNS)
    return df


# %%
gold = load_conllu("corpus/conllu/proiel.conllu")
pred = load_conllu("predictions/cltk/proiel.conllu")
# %%
