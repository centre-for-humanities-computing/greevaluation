# Cleaning previous environments
rm -rf environments/
# Making folder for environments
mkdir -p environments

# cltk stuff
echo "Installing VENV: cltk"
python3 -m venv environments/cltk
source environments/cltk/bin/activate
pip install -r "requirements_cltk.txt"
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
deactivate

# stanza stuff
echo "Installing VENV: stanza"
python3 -m venv environments/stanza
source environments/stanza/bin/activate
pip install -r "requirements_stanza.txt"
deactivate

# udpipe stuff
echo "Installing VENV: udpipe"
python3 -m venv environments/udpipe
source environments/udpipe/bin/activate
pip install -r "requirements_udpipe.txt"
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
deactivate

# spark stuff
echo "Installing VENV: spark"
bash scripts/spark_env.sh