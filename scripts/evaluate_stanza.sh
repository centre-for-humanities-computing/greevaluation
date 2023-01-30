# get in stanza venv
source environments/stanza/bin/activate

# evaluation arguemnts
args=()

# evaluate each corpus
for CORPUS in "joint" "perseus" "proiel"
do
    mkdir -p "metrics/stanza/$CORPUS"
    python3 -m spacy benchmark accuracy "models/stanza-model"