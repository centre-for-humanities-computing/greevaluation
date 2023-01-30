# Fetch assets
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-4923/ud-treebanks-v2.11.tgz
mkdir -p assets/treebanks
tar -xvzf ud-treebanks-v2.11.tgz -C assets/treebanks/
rm ud-treebanks-v2.11.tgz 

# Cleaning up paths
mkdir -p assets/treebanks/perseus/ 
mkdir -p assets/treebanks/proiel/ 
mkdir -p assets/treebanks/joint/ 
cp -rf assets/treebanks/ud-treebanks-v*/UD_Ancient_Greek-Perseus/* assets/treebanks/perseus
cp -rf assets/treebanks/ud-treebanks-v*/UD_Ancient_Greek-PROIEL/* assets/treebanks/proiel
rm -rf assets/treebanks/ud-treebanks-v*