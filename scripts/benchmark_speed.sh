# Speed stuff
echo "Installing VENV: speed benchmark"
python3 -m venv environments/speed

source environments/homercy/bin/activate
# odyCy
pip install -r "requirements_homercy.txt"
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
# UDPipe
pip install -r "requirements_udpipe.txt"
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
# Stanza
pip install -r "requirements_stanza.txt"
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
# greCy
pip install https://huggingface.co/Jacobo/grc_ud_proiel_trf/resolve/main/grc_ud_proiel_trf-any-py3-none-any.whl
pip install https://huggingface.co/Jacobo/grc_ud_perseus_trf/resolve/main/grc_ud_perseus_trf-any-py3-none-any.whl

echo "Initiating Benchmark"
python3 scripts/benchmark_speed.py
deactivate

