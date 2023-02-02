from typing import Dict
from typing_extensions import TypedDict


class Feature(TypedDict):
    name: str
    values: Dict[str, str]


FEATURES: Dict[str, Feature] = {
    "Aspect": {
        "name": "Aspect",
        "values": {
            "imperfective": "Imp",
            "perfective": "Perf",
        },
    },
    "Case": {
        "name": "Case",
        "values": {
            "accusative": "Acc",
            "dative": "Dat",
            "genitive": "Gen",
            "locative": "Loc",
            "nominative": "Nom",
            "vocative": "Voc",
        },
    },
    "Definiteness": {
        "name": "Definite",
        "values": {
            "definite": "Def",
        },
    },
    "Degree": {
        "name": "Degree",
        "values": {
            "comparative": "Cmp",
            "positive": "Pos",
            "superlative": "Sup",
        },
    },
    "Gender": {
        "name": "Gender",
        "values": {
            "feminine": "Fem",
            "masculine": "Masc",
            "neuter": "Neut",
        },
    },
    "Mood": {
        "name": "Mood",
        "values": {
            "imperative": "Imp",
            "indicative": "Ind",
            "optative": "Opt",
            "subjunctive": "Sub",
        },
    },
    "Number": {
        "name": "Number",
        "values": {
            "dual": "Dual",
            "plural": "Plur",
            "singular": "Sing",
        },
    },
    "Person": {
        "name": "Person",
        "values": {
            "first": "1",
            "second": "2",
            "third": "3",
        },
    },
    "Polarity": {
        "name": "Polarity",
        "values": {
            "neg": "Neg",
        },
    },
    "Possessive": {
        "name": "Poss",
        "values": {
            "pos": "Yes",
        },
    },
    "PrononimalType": {
        "name": "PronType",
        "values": {
            "demonstrative": "Dem",
            "interrogative": "Int",
            "personal": "Prs",
            "reciprocal": "Rcp",
            "relative": "Rel",
        },
    },
    "Reflexive": {
        "name": "Reflex",
        "values": {
            "pos": "Yes",
        },
    },
    "Tense": {
        "name": "Tense",
        "values": {
            "future": "Fut",
            "past": "Past",
            "pluperfect": "Pqp",
            "present": "Pres",
        },
    },
    "VerbForm": {
        "name": "VerbForm",
        "values": {
            "finite": "Fin",
            "gerundive": "Gdv",
            "infinitive": "Inf",
            "participle": "Part",
        },
    },
    "Voice": {
        "name": "Voice",
        "values": {
            "active": "Act",
            "middle": "Mid",
            "passive": "Pass",
        },
    },
}
