"""
"""
from typing import Dict, Optional, List
from typing_extensions import TypedDict

import pandas as pd


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


def word_to_entry(token: Dict) -> ConlluEntry:
    """Turns TranKit token object to an entry in a CONLL-U table."""
    if 'feats' in token:
        entry: ConlluEntry = {
            "ID": token['id'],
            "FORM": token['text'],
            "LEMMA": token['lemma'],
            "UPOS": token['upos'],  # type: ignore
            "XPOS": token['xpos'],
            "FEATS": token['feats'],  # type: ignore
            "HEAD": token['head'],
            "DEPREL": token['deprel'],
            "DEPS": "_",
            "MISC": "_",
        }
    else:
        entry: ConlluEntry = {
            "ID": token['id'],
            "FORM": token['text'],
            "LEMMA": token['lemma'],
            "UPOS": token['upos'],  # type: ignore
            "XPOS": token['xpos'],
            "FEATS": "_",  # type: ignore
            "HEAD": token['head'],
            "DEPREL": token['deprel'],
            "DEPS": "_",
            "MISC": "_",
        }
    for key, value in entry.items():
        entry[key] = comply_value(value)
    return entry


def to_conllu(tokens: List[Dict]) -> pd.DataFrame:
    """Turns Trankit document to CONLL-U compliant dataframe."""
    entries = [word_to_entry(word) for word in tokens]
    result = pd.DataFrame.from_records(entries, columns=CONLLU_FIELDS)
    return result


def save_conllu(doc: List[Dict], path: str) -> None:
    """Saves CLTK document as a conllu file to a given path."""
    table = to_conllu(doc)
    table.to_csv(path, sep="\t", na_rep="_", header=False, index=False)
