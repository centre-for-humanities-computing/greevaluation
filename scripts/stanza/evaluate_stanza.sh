# HACK: hardcoded following https://stanfordnlp.github.io/stanza/available_models.html
VERSION="1.0.0" 

# get in stanza venv
source environments/stanza/bin/activate

# fetch stanza models
python3 scripts/stanza/fetch_stanza_grc.py

# evaluate each model
for STANZA_MODEL in "stanza-perseus" "stanza-proiel"
do
    # evaluate test fold in each corpus
    for CORPUS in "joint" "perseus" "proiel"
    do
        mkdir -p "metrics/$STANZA_MODEL/$VERSION"
        python3 -m spacy benchmark accuracy \
            "models/$STANZA_MODEL" \
            "corpus/binary/$CORPUS.spacy" \
            --output "metrics/$STANZA_MODEL/$VERSION/$CORPUS.json"
    done
done