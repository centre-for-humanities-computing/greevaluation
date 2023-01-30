# Cleaning previous environments
rm -rf environments/
# Making folder for environments
mkdir -p environments

# Creating virtual environments
echo "Installing VENV: cltk"
python3 -m venv environments/cltk

# Installing requirements
source environments/cltk/bin/activate
pip install -r "requirements_cltk.txt"
deactivate
