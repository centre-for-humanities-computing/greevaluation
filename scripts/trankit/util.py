"""
"""
from typing import Dict, Optional, List
from typing_extensions import TypedDict

import pandas as pd
from scripts.conllu.file import ConlluEntry, CONLLU_FIELDS


def comply_value(value) -> str:
    """Makes values CONLL-U compliant."""
    if value is None:
        return "_"
    return str(value)


def word_to_entry(token: Dict) -> ConlluEntry:
    """Turns TranKit token object to an entry in a CONLL-U table."""
    entry: ConlluEntry = {
        "ID": token["id"],
        "FORM": token["text"],
        "LEMMA": token["lemma"],
        "UPOS": token["upos"],  # type: ignore
        "XPOS": token["xpos"],
        "FEATS": token.get("feats", "_"),  # type: ignore
        "HEAD": token["head"],
        "DEPREL": token["deprel"],
        "DEPS": "_",
        "MISC": "_",
    }
    for key, value in entry.items():
        entry[key] = comply_value(value)
    return entry


def to_conllu_df(tokens: List[Dict]) -> pd.DataFrame:
    """Turns Trankit document to CONLL-U compliant dataframe."""
    entries = [word_to_entry(word) for word in tokens]
    result = pd.DataFrame.from_records(entries, columns=CONLLU_FIELDS)
    return result
