mkdir -p predictions/cltk
source environments/cltk/bin/activate
python3 scripts/predict_cltk.py
deactivate

for CORPUS in "joint" "perseus" "proiel"
do
    python3 -m spacy convert predictions/cltk/$CORPUS.conllu predictions/cltk/ --converter conllu -n 10 
done