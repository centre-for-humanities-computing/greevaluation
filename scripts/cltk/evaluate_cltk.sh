# bash scripts/cltk/predict_cltk.sh

VERSION=1.1.6
source environments/cltk/bin/activate
for CORPUS in "proiel" "perseus" "joint"
do
    python3 scripts/evaluate_docbin.py predictions/cltk/${CORPUS}_fixed.spacy corpus/binary/${CORPUS}_norm.spacy metrics/cltk/${VERSION}/${CORPUS}.json
done
deactivate