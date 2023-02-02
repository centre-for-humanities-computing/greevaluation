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


def comply_value(value) -> str:
    """Makes values CONLL-U compliant."""
    if value is None:
        return "_"
    return str(value)


def word_to_entry(word) -> ConlluEntry:
    """Turns CLTK word object to an entry in a CONLL-U table."""
    entry: ConlluEntry = {
        "ID": str(word.index_token + 1),
        "FORM": word.string,
        "LEMMA": word.lemma,
        "UPOS": word.upos,  # type: ignore
        "XPOS": word.xpos,
        "FEATS": features_to_str(word.features),  # type: ignore
        "HEAD": str(word.governor + 1),
        "DEPREL": word.dependency_relation,
        "DEPS": "_",
        "MISC": "_",
    }
    for key, value in entry.items():
        entry[key] = comply_value(value)
    return entry


