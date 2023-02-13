source environments/homercy/bin/activate

VERSION="0.5.0"
for MODEL in "grc_dep_treebanks_trf" "grc_dep_treebanks_sm" "grc_dep_treebanks_xlm"
do
    mkdir -p metrics/$MODEL/$VERSION/
    for CORPUS in "perseus" "proiel" "joint" 
    do
        echo "Evaluating $MODEL on $CORPUS"
        python3 -m spacy benchmark accuracy $MODEL corpus/binary/$CORPUS.spacy --output metrics/$MODEL/$VERSION/$CORPUS.json
    done
done

deactivate