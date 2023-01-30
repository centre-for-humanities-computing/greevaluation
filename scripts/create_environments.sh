# Cleaning previous environments
rm -rf environments/
# Making folder for environments
mkdir -p environments

# cltk stuff
echo "Installing VENV: cltk"
python3 -m venv environments/cltk

# Installing requirements
source environments/cltk/bin/activate
pip install -r "requirements_cltk.txt"
deactivate

# stanza stuff
echo "Installing VENV: stanza"
python3 -m venv environments/stanza

source environments/stanza/bin/activate
pip install -r "requirements_stanza.txt"
deactivate