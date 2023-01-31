bash scripts/predict_cltk.sh

source environments/cltk/bin/activate
python3 scripts/evaluate_cltk.py
deactivate