This file describes the scripts that are located in `Delebate_Debt_Holdings`.
The files should be run in the following order (see `delegate_debt.sh`):
1. `clean_debt_files.ipynb`: this file cleans problematically formatted names in the loan office, pierce and marine certificates.
   1. The cleaning process is messy and can likely be improved
   2. However, I'm not sure how many more delegate certificates we'll match through that process (likely not very many)
   3. Only ~ 4000 odd cases out of ~ 80000 (5%) of names are cleaned
2. `clean_states_liquidated_debt.ipynb`: this file cleans names that are formatted in an unmatchable name in the liquidated debt certifiactes
   1. Cleaning process affects very few names
   2. Might be a better way to automate, but will likely affect matching process little
3. `fuzzy_matching.ipyng`: this file matches state/constitutional convention delegates with pre-1790 debt certificates
   1. Might be better to focus on constitutional convention delegates for now
      1. Should impose strict rules for state delegate matching (same state = must, etc)
   2. Can improve "name-matching" process as well as overall match process
