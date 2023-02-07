
source environments/trankit/bin/activate

VERSION="1.1.1"

# run evaluation on two variants of the model
# using two variants of foundational model for embeddings
for MODEL in "ancient-greek" "ancient-greek-perseus" 
do 
    for EMBEDDING in "xlm-roberta-base" "xlm-roberta-large"
    do
        python3 scripts/trankit/predict_trankit.py --model "$MODEL" --embedding "$EMBEDDING"
        for CORPUS in "joint" "perseus" "proiel"
        do
            python3 -m spacy convert predictions/trankit/${CORPUS}_${MODEL}_${EMBEDDING}.conllu predictions/trankit/ --converter conllu -n 10 
            python3 scripts/evaluate_docbin.py predictions/trankit/${CORPUS}_${MODEL}_${EMBEDDING}.spacy corpus/binary/${CORPUS}.spacy metrics/trankit_${MODEL}_${EMBEDDING}/${VERSION}/${CORPUS}.json
        done
    done
done