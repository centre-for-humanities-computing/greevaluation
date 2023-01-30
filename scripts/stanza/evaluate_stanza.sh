# HACK: hardcoded following https://stanfordnlp.github.io/stanza/available_models.html
VERSION="1.0.0" 

# get in stanza venv
source environments/stanza/bin/activate

# evaluate each model
for STANZA_MODEL in "stanza-perseus" "stanza-proiel"
do
    # evaluate test fold in each corpus
    for CORPUS in "joint" "perseus" "proiel"
    do
        mkdir -p "metrics/$STANZA_MODEL_NAME/$VERSION/$CORPUS"
        python3 -m spacy benchmark accuracy \
            "models/stanza-model" \
            "corpus/binary/$CORPUS.spacy" \
            --output "metrics/$STANZA_MODEL_NAME/$VERSION/$CORPUS.json"
    done
done