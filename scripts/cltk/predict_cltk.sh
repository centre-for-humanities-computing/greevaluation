mkdir -p predictions/cltk
source environments/cltk/bin/activate
python3 scripts/conllu/remove_misc.py --no-lines
deactivate

for CORPUS in "joint" "perseus" "proiel"
do
    python3 -m spacy convert corpus/conllu/${CORPUS}_norm.conllu corpus/binary/ --converter conllu -n 10 
done

source environments/cltk/bin/activate
python3 -m scripts.cltk.predict_cltk
python3 -m scripts.cltk.fix_cltk
deactivate

for CORPUS in "joint" "perseus" "proiel"
do
    python3 -m spacy convert predictions/cltk/${CORPUS}_fixed.conllu predictions/cltk/ --converter conllu -n 10 
done