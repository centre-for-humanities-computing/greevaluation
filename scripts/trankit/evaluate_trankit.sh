
source environments/trankit/bin/activate

# run evaluation on two variants of the model
# using two variants of foundational model for embeddings
for MODEL in "ancient-greek" "ancient-greek-perseus" 
do 
    for EMBEDDING in "xlm-roberta-base" "xlm-roberta-large"
    do
        python3 scripts/trankit/predict_trankit.py --model "$MODEL" --embedding "$EMBEDDING"
    done
done