from typing import Dict, Optional

import pandas as pd
from cltk.core.data_types import Doc, Word
from typing_extensions import TypedDict

from utils.features import FEATURES

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


def features_to_str(features: Optional[Dict[str, str]]) -> str:
    """Converts CLTK feature dictionary to CONLLU feature string."""
    if features is None:
        return "_"
    feature_assignments = []
    for feature_name, values in features.items():
        feature_name = str(feature_name)
        value_name = str(values[0])
        feature = FEATURES[feature_name]
        feature_name = feature["name"]
        value = feature["values"][value_name]
        assignment = f"{feature_name}={value}"
        feature_assignments.append(assignment)
    if not feature_assignments:
        return "_"
    return "|".join(feature_assignments)


def comply_value(value) -> str:
    """Makes values CONLL-U compliant."""
    if value is None:
        return "_"
    return str(value)


def word_to_entry(word: Word) -> ConlluEntry:
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


def to_conllu(doc: Doc) -> pd.DataFrame:
    """Turns CLTK document to CONLL-U compliant dataframe."""
    entries = [word_to_entry(word) for word in doc.words]
    result = pd.DataFrame.from_records(entries, columns=CONLLU_FIELDS)
    return result


def save_conllu(doc: Doc, path: str) -> None:
    """Saves CLTK document as a conllu file to a given path."""
    table = to_conllu(doc)
    table.to_csv(path, sep="\t", na_rep="_", header=False, index=False)
