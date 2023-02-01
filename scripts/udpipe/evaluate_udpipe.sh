# HACK: hardcoded following https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3131
VERSION="2.5.0" 

# get in stanza venv
source environments/udpipe/bin/activate

# fetch stanza models
python3 scripts/udpipe/fetch_udpipe_grc.py

# evaluate each model
for UDPIPE_MODEL in "udpipe-perseus" "udpipe-proiel"
do
    # evaluate test fold in each corpus
    for CORPUS in "joint" "perseus" "proiel"
    do
        mkdir -p "metrics/$UDPIPE_MODEL/$VERSION"
        python3 -m spacy benchmark accuracy \
            "models/$UDPIPE_MODEL" \
            "corpus/binary/$CORPUS.spacy" \
            --output "metrics/$UDPIPE_MODEL/$VERSION/$CORPUS.json"
    done
done