SPARK_VERSION="4.2.8"
source environments/spark/bin/activate
python3 scripts/spark/predict_spark.py

for CORPUS in "joint" "perseus" "proiel"
do
    python3 -m spacy convert predictions/spark/${CORPUS}.conllu predictions/spark/ --converter conllu -n 10 
    python3 scripts/evaluate_docbin.py predictions/spark/${CORPUS}.spacy corpus/binary/${CORPUS}.spacy metrics/spark/${SPARK_VERSION}/${CORPUS}.json
done
deactivate