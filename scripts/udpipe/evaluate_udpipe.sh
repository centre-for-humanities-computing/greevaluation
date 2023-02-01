source environments/udpipe/bin/activate
python3 scripts/fetch_udpipe_grc.py
python3 scripts/predict_udpipe.py
python3 scripts/evaluate_udpipe.py
deactivate