#ClinPhen is a tool that automatically extracts phenotypes from clinical notes.
#ClinPhen is freely available for academic, nonprofit, and personal use. Please e-mail us with any licensing inquiries.

#PIP VERSION INSTRUCTIONS
##To extract phenotypes:
clinphen <path_to_clinincal_note_file>

##To see how to use other features:
clinphen -h

##We also have a version that parses phenotypes from a large table of notes. You can run it with:
clinphen_bulk <path_to_table_file> <path_to_output_file>

##The input file for clinphen_bulk, by default, is a 2-column table delimited by a "|" character. The first column is the patient identifier, the second is the note. It should have the following header:
"MRN"|"NOTE"

##To learn more, run:
clinphen_bulk -h

#STANDARD (NON-PIP) VERSION INSTRUCTIONS
#Running the ClinPhen GUI on a mac:

#Running the ClinPhen GUI on a non-mac:

#Running the ClinPhen GUI on the command line:
##Open the terminal
##cd to the ClinPhen directory
##Run the following command:
./ClinPhenApp

#Running ClinPhen directly on the command line:
##Open the terminal
##cd to the ClinPhen directory
##Run the following command:
./clinphen input.txt
##Replace "input.txt" with the path to the free-text clinical note file that you want to parse.
##You can also run the command line with a custom thesaurus:
./clinphen input.txt thesaurus.txt
##Replace "thesaurus.txt" with the path to your custom thesaurus, which should be in the format: HPO_ID<tab>Synonym
