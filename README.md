# SPEOC-pt-1
Code repository for a Summer Project on the Economic Origins of the Constitution. Contact me at chrisliao (at) uchicago (dot) edu. The project has two components - delegate matching and pre-post debt matching. The README is separated into two parts, one for each component.

## Overview of delegate matching
The purpose of this part of the project was to match constitutional and state convention delegates to their pre-1790 debt asset totals to identify how much each delegate owned and ananlyze if this influenced their vote. 

The name matching was executed in three steps: cleaning, fuzzy-matching, and merging. We have structured the Dropbox subdirectory to make the code runnable as-is. In more detail, the folder consists of:

1. `Data`: This folder contains all of the raw data and cleaned data. Within the Delegates, Post1790, and Pre1790 subfolders are the corresponding raw Excel sheets (copied from the dropbox) and cleaned csv files. This folder also contains `final_matching.csv` and `final_matching_post1790.csv` which list the results of our fuzzy matching.
2. `Producables`:The requested final tables are in this folder, along with a folder called ‘Separate’ containing csv files with individual tables for each type of certificate 
    1.`Delegate_Pre1790_Assets.csv` contains the assets in Pre-1790 certificates for all delegates
    2.`Delegate_Post1790_Assets.csv` contains the assets in Post-1790 certificates for all delegates
3. `clean_debt_files.ipynb`: This Jupyter notebook contains the code used to produce the cleaned csv files in the Data/Pre1790/Cleaned folder. Note: the post-1790 data was not cleaned.
4. `fuzzy_matching.ipynb`: This Jupyter notebook contains the code that created the`final_matching.csv`file in the Data folder that we used to identify pre-1790 debt certificates held by delegates
5. `fuzzy_matching_post1790.ipynb`: This Jupyter notebook contains the code that created the`final_matching_post1790_._csv`file in the Data folder that we used to identify post-1790 debt certificates held by delegates
6. `debt_aggregation.ipynb`: This Jupyter notebook contains the code which merges the cleaned delegate names and debt certificate/stock data using the`final_matching.csv`files. It then merges those results to produce`Delegate_Pre1790_Assets`in the`Producables`folder.
7. `debt_aggregation_post1790.ipynb`: This Jupyter notebook contains the code which merges the cleaned delegate names and debt certificate/stock data using the`final_matching_post1790.csv`files. It then merges those results to produce`Delegate_Post1790_Assets.csv`in the`Producables`folder.
8. `Results.ipynb`: This jupyter notebook contains the code which we used to generate results described in the technical report and located in the Results section.


### Detailed Description of Jupyter notebooks **
#### `clean_debt_files.ipynb`

Its overall purpose is to clean raw data imported into DataFrames from Excel sheets. Special cases are names that had to be manually replaced because they didn't follow some sort of set rule. Here are what the notebook does to different data files. 
* Delegates - strips names and separates alternate last names (in parentheses in the raw data) into two full names
    * Special case - row 44 of constitutional_convention_1787 was ‘Fitzsimons (FitzSimons; Fitzsimmons)’ and got modified to Fitzsimons (Fitzsimmons)
    * Note: John Nesbitt (Nisbet) was missed in cleaning and might not have matched properly
* Loan office certificates - removes empty rows and entries missing first or last names, splits full name entries with ‘&’ or ‘and’ into multiple names, handles cases of executors, heirs, ‘and co’, and treasurers
    * Creates`state_companies.csv`with entries that have ‘&’ or ‘and’ but with incomplete names (i.e. only last name)
    * Note: uses an entity classifier to detect organizations and remove them; results were manually checked for accuracy
        * See [https://spacy.io/models](https://spacy.io/models) for more detail about the entity classifier
    * Special cases - see`export_weird_names.csv`file in the Data folder; see chart below for cases changed manually
        * Entries marked with ** have an executor whose first name got accidentally dropped
        * Notes column contains other changes, errors, etc.
        * See `Documentation/LOC_special_cases.md`
* Marine office certificates - removes entries with ‘deceased’ and ‘estate’, adding notes to a cleaning notes column
    * Special cases: see chart, Hoov and Harrison were split into two last name columns
    * See `Documentation/marine_special_cases.md`
* Pierce certificates - strips entries and removes entries with no last name, added a second set of name columns
    * Special cases - see chart; some split into two names
    * See `Documentation/pierce_special_cases.md`
* State liquidated debt - removes empty rows; splits entries with ‘&’ or ‘and’ into two names; removes phrases like ‘and co’, ‘& son’ , ‘& others’ and adds them to a Cleaning notes column; removes ‘estates’, ‘heir of’, and ‘deceased’, adding those to the notes 
    * Special cases - see chart; some entries in PA had ‘esastate’ and those were treated the same as ‘estate’
        * See `Documentation/sld_special_cases.md`



#### fuzzy_matching.ipynb
Its overall purpose is to run the cleaned delegate and debt certificate files through a fuzzy matching algorithm, yielding `final_matching.csv_
* First, uses process.extract with a threshold of 85 to form a list of possible matches
    * Note: process.extract uses a weighted ratio of all four fuzz ratios
* Next, let m = min(# of words in name 1, # of words in name 2). This is the minimum threshold of word-pairs between the two names that must have a threshold score of 90 (a word pair is a pair of words consisting of one word from each of the two names that were considered to be a match)
* If the match passes both steps, it is added to the csv file
* In addition, if one name from the debt certificate files is matched to multiple delegates, we eliminate all but the matchign with the highest score. 
* See the Methods section of the report for a better explanation of step 2

#### fuzzy_matching_post1790.ipynb
It uses the same algorithm as`fuzzy_matching.ipynb` to generate`final_matching_post1790.csv`

#### debt_aggregation.ipynb
It merges state and constitutional convention delegates’ on the matched names from`final_matching.csv`, then uses full names to merge with the cleaned pre-1790 loan certificate data to compile the total sum value and certificate count of each certificate type for each delegate. It also produces`Delegate_Pre1790_Assets.csv`

#### debt_aggregation_post1790.ipynb 
It uses the same process to merge matched names with the post-1790 stocks and compile the total sum value and count of each type of stock for each delegate. It produces`Delegates_Post1790_Assets.csv`

### Results.ipynb
This is the code which utilizes fuzzy matching and aggregated debt csv files to generate the tables and charts found in the Results section of our technical report

### Detailed description of csv files
#### Raw data
* Delegates
    * `Data/Delegates/constitutional_convention_1787.xlsx`
    * `Data/Delegates/State Delegates.xlsx`
* Pre1790 Debt Files
    * `Data/Pre1790/` contains the raw Pre-1790 debt certificates that were copied over dropbox
* Post1790 Debt Files
    * `Data/Post1790/` contains the raw Post-1790 debt certificates that were copied over dropbox, organized by state in the folders

#### Cleaned Data
These are products of`clean_debt_files.ipynb`
* Delegates - located in`Data/Delegates/cleaned`
    * `State_Delegates_cleaned.csv`
    * `constitutional_convention_delegates_cleaned.csv`
* Pre-1790 Debt Files - located in`Data/Pre1790/cleaned`
    * `Marine_Liquidated_Debt_Certificates_cleaned.csv`
    * `Pierce_Certs_cleaned_2021.csv`
    * `liquidated_debt_certificates_CT_cleaned.csv`
    * `liquidated_debt_certificates_DE_cleaned.csv`
    * `liquidated_debt_certificates_MA_cleaned.csv`
    * `liquidated_debt_certificates_NH_cleaned.csv`
    * `liquidated_debt_certificates_NJ_cleaned.csv`
    * `liquidated_debt_certificates_NY_cleaned.csv`
    * `liquidated_debt_certificates_PA_stelle_cleaned.csv`
    * `liquidated_debt_certificates_PA_story_cleaned.csv`
    * `liquidated_debt_certificates_RI_cleaned.csv`
    * `Loan_office_certificates_9_states_cleaned.csv`

#### Intermediary Data 
* `final_matching.csv` - Lists all the fuzzy matches matches generated by `fuzzy_matching.ipynb`, with the initial process.extract score in the Scores column
    * Used in `debt_aggregation.ipynb`to generate totals of delegate assets
* `final_matching_post1790.csv` - Lists all the fuzzy matches matches generated by `fuzzy_matching_post1790.ipynb`, with the initial process.extract score in the Scores column
    * Used in `debt_aggregation_post1790.ipynb` to generate totals of delegate assets
* `state_companies.csv` - Lists all the entries from `Loan_office_certificates_9_states.xlsx` which contained ‘&’ or ‘and’ with two last names
    * Ex. Clark & Nightingale

#### Final Data
* `Delegates_Pre1790_Assets.csv` - final compiled table of pre-1790 assets of delegates, formatted as requested
    * Product of`debt_aggregation.ipynb`
* `Delegates_Post1790_Assets.csv`- final compiled table of post-1790 assets of delegates, formatted requested
    * Product of`debt_aggregation_post1790.ipynb`
* Separate - aggregated debt for each type of asset
    * `ASD_debt_Matched.csv`
    * `CD_debt_Matched.csv`
    * `Loan_Office_Certificates_Matched.csv`
    * `Marine_Certificates_Matched.csv`
    * `Pierce_Certificates_Matched.csv`
    * `State_Certificates_Matched.csv`

#### Something I wish we did:
* Identify company owners - see our incomplete list at`state_companies.csv`
    * This would give us a more complete way to calculate a person’s holdings
* Change abbreviated names (Thm - Thomas, J/Jn to John/Jonathan)

## Overview of pre-post debt matching
In this step, I matched individuals who owned continental debt post-1790 to their pre-1790 debt assets. `post1790_data_prep.ipynb` generates the dataset of matches and asset totals, and `post1790_data_analysis.ipynb` generates results relating to this question. 
