"""Set of utilities for writing and reading conll-u files."""
import os
from typing import Sequence, List, Dict, Any
from typing_extensions import TypedDict
from io import StringIO
from pathlib import Path
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


def read_conllu_df(path: str) -> pd.DataFrame:
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


def is_sentence_end(i_entry: int, entries: Sequence[ConlluEntry]) -> bool:
    """Determines whether the given entry is the end of a sentence."""
    n_entries = len(entries)
    return (i_entry < (n_entries - 1)) and (
        int(entries[i_entry]["ID"]) > int(entries[i_entry + 1]["ID"])
    )


def to_conllu_text(entries: Sequence[ConlluEntry]) -> str:
    """Turns a sequence of entries to a CONLL-U compliant string."""
    n_entries = len(entries)
    lines: List[str] = []
    for i_entry in range(n_entries):
        current = entries[i_entry]
        # Joining fields together with a tab
        line = "\t".join(str(current[field]) for field in CONLLU_FIELDS)
        lines.append(line)
        # Adding empty line if sentence ends
        if is_sentence_end(i_entry, entries=entries):
            lines.append("")
    # Joining lines together with line break
    text = "\n".join(lines)
    return text


def df_to_entries(df: pd.DataFrame) -> List[ConlluEntry]:
    """Turns data frame to a list of conllu entries."""
    # Selecting important rows in the proper order
    df = df[CONLLU_FIELDS]
    entries: List[ConlluEntry] = []
    for index, row in df.iterrows():
        entry: ConlluEntry = row.to_dict()  # type:ignore
        entries.append(entry)
    return entries


def write_conllu(entries: Sequence[ConlluEntry], path: str) -> None:
    """Writes entries to a conllu file."""
    if not path.endswith(".conllu"):
        raise ValueError(
            f"Path: {path}, is not the right format, file extension has to be conllu"
        )
    # Making sure directory exists
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    text = to_conllu_text(entries)
    with open(path, "w") as out_file:
        out_file.write(text)


def write_conllu_df(df: pd.DataFrame, path: str) -> None:
    """Writes dataframe with entries to a conllu file."""
    entries = df_to_entries(df)
    write_conllu(entries, path)
