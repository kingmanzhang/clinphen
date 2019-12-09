DIR=$1

#if [ -d "$DIR/data" ]; then
#  rm -r $DIR/data
#fi
#mkdir $DIR/data
#
#curl https://files.pythonhosted.org/packages/6f/ed/9c755d357d33bc1931e157f537721efb5b88d2c583fe593cc09603076cc3/nltk-3.4.zip > $DIR/data/nltk-3.4.zip
#unzip $DIR/data/nltk-3.4.zip -d $DIR/data/
#if [ -d "$DIR/nltk" ]; then
#  rm -r $DIR/nltk
#fi
#mv $DIR/data/nltk-3.4/nltk/ $DIR/
#rm -r $DIR/data/nltk-3.4/
#rm $DIR/data/nltk-3.4.zip
#
#if [ -d "$DIR/nltk_data" ]; then
#  rm -r $DIR/nltk_data
#fi
#mkdir $DIR/nltk_data
#mkdir $DIR/nltk_data/corpora
#curl https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip > $DIR/nltk_data/corpora/wordnet.zip
#unzip $DIR/nltk_data/corpora/wordnet.zip -d $DIR/nltk_data/corpora/
#rm $DIR/nltk_data/corpora/wordnet.zip
#cat $DIR/nltk/data.py | awk 'BEGIN {FS = "\t"} {if($1 == "path = []"){print $1 "\npath.append(\"'$DIR/nltk_data'\")"} else{print}}' > $DIR/tmp
#mv $DIR/tmp $DIR/nltk/data.py

curl https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo > $DIR/data/hp.obo
python $DIR/hpo_syns.py $DIR/data/hp.obo > $DIR/data/tmp
python $DIR/standardize_syn_map.py $DIR/data/tmp > $DIR/data/hpo_synonyms.txt
rm $DIR/data/tmp
python $DIR/hpo_names.py $DIR/data/hp.obo > $DIR/data/hpo_term_names.txt 

