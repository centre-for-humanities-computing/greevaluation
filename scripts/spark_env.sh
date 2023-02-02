sudo apt update -y
sudo apt upgrade -y

# install java
sudo apt install default-jre -y

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