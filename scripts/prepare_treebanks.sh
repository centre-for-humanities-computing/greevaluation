# ----Renaming perseus and proiel treebank files----

for CORPUS in "perseus" "proiel"
do
    mkdir -p corpus/$CORPUS
    for SET in "train" "dev" "test"
    do
        mv assets/treebanks/$CORPUS/grc_$CORPUS-ud-$SET.conllu assets/treebanks/$CORPUS/$SET.conllu
        mv assets/treebanks/$CORPUS/grc_$CORPUS-ud-$SET.txt assets/treebanks/$CORPUS/$SET.txt
    done
done

# ----Joining treebanks together----
python3 scripts/join_treebanks.py

# ----Moving texts to more consistent paths----
rm -rf corpus/text
mkdir -p corpus/text
for CORPUS in "joint" "perseus" "proiel"
do
    cp assets/treebanks/$CORPUS/test.txt corpus/text/$CORPUS.txt
done

# ----Copying conll files to corpus/----
rm -rf corpus/conllu
mkdir -p corpus/conllu
for CORPUS in "joint" "perseus" "proiel"
do
    cp assets/treebanks/$CORPUS/test.conllu corpus/conllu/$CORPUS.conllu
done

# ----Converting treebank data to spaCy binraries----
for CORPUS in "joint" "perseus" "proiel"
do
    mkdir -p corpus/$CORPUS
    for SET in "train" "dev" "test"
    do
        python3 -m spacy convert assets/treebanks/$CORPUS/$SET.conllu corpus/$CORPUS/ --converter conllu -n 10 
    done
done

# ----Moving spaCy binaries to more consistent paths----
rm -rf corpus/binary
mkdir -p corpus/binary
for CORPUS in "joint" "perseus" "proiel"
do
    mv corpus/$CORPUS/test.spacy corpus/binary/$CORPUS.spacy
    rm -rf corpus/$CORPUS
done
