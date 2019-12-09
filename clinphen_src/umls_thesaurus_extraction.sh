umlsDir=$1
targetDir=$2
prepperPath=$3

mkdir $targetDir/umls

for file in $umlsDir/*.nlm; do  unzip -o -d $targetDir/umls $file; done

gunzip -c $targetDir/umls/*/META/MRCONSO* | awk '{FS = "|";} $2 == "ENG"' > $targetDir/umls/id_everything_map.txt

python $prepperPath > $targetDir/hpo_umls_thesaurus.txt

rm -rf $targetDir/umls
