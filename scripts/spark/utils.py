from typing import Dict, Optional, List
from io import StringIO

import pandas as pd
from typing_extensions import TypedDict

# Entry order in CONLL-U files
CONLLU_FIELDS = [
    "ID",
    "FORM",
    "LEMMA",
    "UPOS",
    "XPOS",
    "FEATS",
    "HEAD",
    "DEPREL",
    "DEPS",
    "MISC",
]
GREEK_PUNCT = [",", ".", "·", ";", "(", ")", ".̓"]


class ConlluEntry(TypedDict):
    """Entry in CONLL-U files"""

    ID: str
    FORM: str
    LEMMA: str
    UPOS: str
    XPOS: str
    FEATS: str
    HEAD: str
    DEPREL: str
    DEPS: str
    MISC: str


def remove_punctuation(text: str) -> str:
    """Removes punctuation from greek text."""
    punct = "".join(GREEK_PUNCT)
    trans = str.maketrans({mark: "" for mark in punct})
    return text.translate(trans)


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
    df = pd.read_csv(text_stream, sep="\t", names=CONLLU_FIELDS)
    return df


def create_punct_token(text: str, index: int) -> ConlluEntry:
    token = {key: "_" for key in CONLLU_FIELDS}
    token["FORM"] = text
    token["LEMMA"] = text
    token["XPOS"] = "u--------"
    token["UPOS"] = "PUNCT"
    token["DEPREL"] = "punct"
    token["HEAD"] = "0"
    token["ID"] = str(index)
    return ConlluEntry(**token)


def get_punct_tokens(token: ConlluEntry) -> List[ConlluEntry]:
    punct_tokens = []
    current_index = int(token["ID"])
    punct_chars = "".join(
        [char for char in token["FORM"] if char in GREEK_PUNCT]
    )
    while punct_chars:
        if punct_chars.startswith("..."):
            punct_chars = punct_chars.removeprefix("...")
            new_token = "..."
        else:
            new_token = punct_chars[0]
            punct_chars = punct_chars[1:]
        punct_tokens.append(
            create_punct_token(
                new_token, index=current_index + len(punct_tokens) + 1
            )
        )
    return punct_tokens


def is_end_of_sentence(doc_df: pd.DataFrame, i_token: int) -> bool:
    n_rows = len(doc_df.index)
    return (i_token < n_rows - 1) and (
        int(doc_df.iloc[i_token]["ID"]) > int(doc_df.iloc[i_token + 1]["ID"])
    )


def is_punct(token: ConlluEntry) -> bool:
    """Determines if a token is only made up of punctuation marks."""
    return not remove_punctuation(token["FORM"])


def fix_punctuation(doc_df: pd.DataFrame) -> pd.DataFrame:
    """Fixes CLTK's stupid punctuation errors."""
    records: List[ConlluEntry] = []
    n_punct = 0
    n_rows = len(doc_df.index)
    for i_token in range(n_rows):
        current_token = ConlluEntry(**doc_df.iloc[i_token].to_dict())  # type: ignore
        if is_punct(current_token):
            current_token["ID"] = str(int(current_token["ID"]) + n_punct - 1)
            punct_tokens = get_punct_tokens(current_token)
            records.extend(punct_tokens)
        else:
            current_token["ID"] = str(int(current_token["ID"]) + n_punct)
            punct_tokens = get_punct_tokens(current_token)
            current_token["FORM"] = remove_punctuation(current_token["FORM"])
            records.extend([current_token, *punct_tokens])
            n_punct += len(punct_tokens)
        if is_end_of_sentence(doc_df, i_token):
            n_punct = 0
    return pd.DataFrame.from_records(records, columns=CONLLU_FIELDS)
