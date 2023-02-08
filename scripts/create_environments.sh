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
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
deactivate

# udpipe stuff
echo "Installing VENV: udpipe"
python3 -m venv environments/udpipe
source environments/udpipe/bin/activate
pip install -r "requirements_udpipe.txt"
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
deactivate

# our stuff
echo "Installing VENV: homercy"
python3 -m venv environments/homercy
source environments/homercy/bin/activate
pip install -r "requirements_homercy.txt"
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
pip install https://huggingface.co/janko/grc_dep_treebanks_sm/resolve/main/grc_dep_treebanks_sm-any-py3-none-any.whl
deactivate

# spark stuff
# install java
sudo apt install default-jre

# export java home
JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export JAVA_HOME

# create spark env
python3 -m venv environments/spark
source environments/spark/bin/activate

# install requirements
pip install -r requirements_spark.txt
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl

# export spark home
SPARK_HOME=environments/spark/lib/python3.9/site-packages/pyspark
export SPARK_HOME

# trankit stuff
echo "Installing VENV: trankit"
python3 -m venv environments/trankit
source environments/homercy/bin/activate
pip install -r "requirements_trankit.txt"
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
pip install https://huggingface.co/janko/grc_dep_treebanks_sm/resolve/main/grc_dep_treebanks_sm-any-py3-none-any.whl
deactivate