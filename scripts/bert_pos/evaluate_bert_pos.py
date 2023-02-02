import os

from flair.models import SequenceTagger


def load_model() -> SequenceTagger:
    working_dir = os.getcwd()
    os.chdir("models/Ancient-Greek-BERT")
    tagger = SequenceTagger.load("SuperPeitho-FLAIR-v2/final-model.pt")
    os.chdir(working_dir)
    return tagger


def main() -> None:
    tagger = load_model()
