# ----Renaming perseus and proiel treebank files----

# Perseus
mv assets/treebanks/perseus/grc_perseus-ud-dev.conllu assets/treebanks/perseus/dev.conllu
mv assets/treebanks/perseus/grc_perseus-ud-train.conllu assets/treebanks/perseus/train.conllu
mv assets/treebanks/perseus/grc_perseus-ud-test.conllu assets/treebanks/perseus/test.conllu
# Proiel
mv assets/treebanks/proiel/grc_proiel-ud-dev.conllu assets/treebanks/proiel/dev.conllu
mv assets/treebanks/proiel/grc_proiel-ud-train.conllu assets/treebanks/proiel/train.conllu
mv assets/treebanks/proiel/grc_proiel-ud-test.conllu assets/treebanks/proiel/test.conllu

# ----Joining treebanks together----
python3 scripts/join_treebanks.py

# ----Copying conll files to corpus/----
rm -rf corpus/conllu
mkdir -p corpus/conllu
cp assets/treebanks/perseus/test.conllu corpus/conllu/perseus.conllu
cp assets/treebanks/proiel/test.conllu corpus/conllu/proiel.conllu
cp assets/treebanks/joint/test.conllu corpus/conllu/joint.conllu

# ----Converting treebank data to spaCy binraries----
for CORPUS in "joint" "perseus" "proiel"
do
    mkdir -p corpus/$CORPUS
    for SET in "train" "dev" "test"
    do
        python3 -m spacy convert assets/treebanks/$CORPUS/$SET.conllu corpus/$CORPUS/ --converter conllu -n 10 
    done
done

# ----Moving spaCy binaries to more consistent paths
mkdir -p corpus/binary
for CORPUS in "joint" "perseus" "proiel"
do
    mv corpus/$CORPUS/test.spacy corpus/binary/$CORPUS.spacy
    rm -rf corpus/$CORPUS
done