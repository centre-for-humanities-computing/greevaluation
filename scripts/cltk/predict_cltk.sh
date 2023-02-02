mkdir -p predictions/cltk
source environments/cltk/bin/activate
python3 scripts/cltk/predict_cltk.py
python3 scripts/cltk/wrangle_cltk.py
deactivate

for CORPUS in "joint" "perseus" "proiel"
do
    python3 -m spacy convert predictions/cltk/${CORPUS}_fixed.conllu predictions/cltk/ --converter conllu -n 10 
done

for CORPUS in "joint" "perseus" "proiel"
do
    python3 -m spacy convert corpus/conllu/${CORPUS}_norm.conllu corpus/binary/ --converter conllu -n 10 
done