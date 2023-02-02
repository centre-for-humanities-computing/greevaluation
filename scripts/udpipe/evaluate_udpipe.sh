source environments/udpipe/bin/activate
python3 scripts/udpipe/fetch_udpipe_grc.py
python3 scripts/udpipe/predict_udpipe.py
python3 scripts/udpipe/evaluate_udpipe.py
deactivate