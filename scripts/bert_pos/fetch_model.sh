# Creating folder for the model and cleaning everything that was previously there
rm -rf models/bert_pos/
mkdir -p models/bert_pos/
# Cloning from GitHub
cd models/bert_pos/
git clone https://github.com/pranaydeeps/Ancient-Greek-BERT.git
cd Ancient-Greek-BERT
git lfs install
git lfs pull --include "final-model.pt"
mkdir ../LM
git clone https://huggingface.co/pranaydeeps/Ancient-Greek-BERT ../LM/SuperPeitho-v1