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
import numpy as np

from utils.cltk import load_conllu

# %%
gold = load_conllu("corpus/conllu/joint.conllu")
pred = load_conllu("predictions/cltk/joint_fixed.conllu")
# %%
gold

# %%
pred
# %%
matches = gold["FORM"] == pred["FORM"]
doesnt_match = matches.index[~matches]
# %%
gold_nomatch = gold.loc[doesnt_match]

# %%
pred_nomatch = pred.loc[doesnt_match]

# %%
nomatch = pd.DataFrame(
    dict(
        gold=gold.loc[doesnt_match]["FORM"],
        pred=pred.loc[doesnt_match]["FORM"],
    )
)
# %%
import os

os.chdir("/home/au689890/Documents/Github/greevaluation")

# %%
import spacy
from spacy.scorer import Scorer
from spacy.training import Example
from spacy.vocab import Vocab
from spacy.tokens import DocBin

import pandas as pd

PRED_DIR = "predictions/cltk/"
GOLD_DIR = "corpus/binary"

pred_path = os.path.join(PRED_DIR, f"joint_fixed.spacy")
gold_path = os.path.join(GOLD_DIR, f"joint.spacy")
pred_db = DocBin().from_disk(pred_path)
gold_db = DocBin().from_disk(gold_path)
pred_docs = pred_db.get_docs(Vocab())
gold_docs = gold_db.get_docs(Vocab())

gold_tokens = [token.orth_ for doc in gold_docs for token in doc]
pred_tokens = [token.orth_ for doc in pred_docs for token in doc]

# %%
tokens = pd.DataFrame(dict(gold=gold_tokens, pred=pred_tokens))
tokens

# %%
tokens[tokens.pred != tokens.gold]

# %%
(pred_tokens == gold_tokens)

# %%
