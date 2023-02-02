mkdir -p models/agile
cd models/agile
git clone https://github.com/agile-gronlp/agile
cd agile

source environments/agile/bin/activate
pip install requirements.txt
deactivate