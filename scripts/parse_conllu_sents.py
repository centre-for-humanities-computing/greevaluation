"""Load CONLL-U files from corpus/ - extract raw sentences - save as txt
"""
import os
from conllu import parse


CONLLU_DIR = 'corpus/conllu'
OUT_DIR = 'corpus/text_sents'


if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)


for corpus in ['joint', 'perseus', 'proiel']:

    # load conllu
    path = os.path.join(CONLLU_DIR, f"{corpus}.conllu")
    with open(path) as fin:
        raw_data = fin.read()

    # parse & extract segmented sentences
    treebank = parse(raw_data)
    sentences = [sent.metadata['text'] for sent in treebank]

    # export to txt
    outpath = os.path.join(OUT_DIR, f"{corpus}.txt")
    with open(outpath, 'w') as fin:
        for sent in sentences:
            fin.write(f"{sent}\n")
