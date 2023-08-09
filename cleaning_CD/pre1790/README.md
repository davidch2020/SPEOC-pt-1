# Cleaning Pre-1790 Debt Data 
The goal of this exercise was to clean the names of the individuals in the pre-1790 individual state debt files. There were many different kinds of issues we found with individuals' names. All of them can be found [here](https://docs.google.com/document/d/1pcSQfWNll6K9tl-_rB4lztN0TsZsclU9vOnbyQob-Zs/edit), along with comments and examples. In order to go about cleaning the individual debt files, ```@Snapwhiz914``` and ```@davidch2020``` decided to work on different parts of the cleaning process. 

## Setting up the Environment 
1. Clone this GitHub repository.
2. The latest version of Python is assumed to be installed. 
3. Enter your default terminal. 
4. Use Python's ```pip``` package or any other package installer to install the following libraries:
    - ```pip install pandas```
    - ```pip install numpy```
    - ```pip install selenium```
    - ```pip install phonetics```
    - ```pip install fuzzywuzzy```
5. Open ```clean_names_david.ipynb```

## Running the Program
Run code cells from top-to-bottom. Here are the different sections of my code. Detailed steps are in the section headers of ```clean_names_david.ipynb```. 

### Before Cleaning
**Goal**: Import all libraries and files. <br>
**Input**: ```final_agg_debt.csv``` type: CSV file <br>
**Output**: ```agg_debt``` type: Pandas dataframe

### Documenting Changes
**Goal**: We need to document changes we make to agg_debt.csv in a separate dataframe: name_changes. This way, we can double-check whether those changes were appropriate. <br>
**Input**: No inputs. <br>
**Output**: ```name_changes``` type: Pandas dataframe

[Add columns here]

### Company Names
**Goal**: Some debt entries are actually company names or represent a group of people (example: ```James Vernon & Co.```).<br>

[Add examples of company debt entries here]

**Input**: ```agg_debt```, ```name_changes```<br>
**Output**: ```agg_debt```: Company names changed to people's names, ```name_changes``` + Company names

[Add example output here]

### Cleaning Entries with Two Names
<b>Goal: </b>There are debt entries that have two names in a single cell: ```NY_2422: Messes Williamson & Beckman```. The plan is to split the name across the first name and last name columns. <br>

[Add examples here]

**Input**: ```agg_debt```, ```name_changes``` <br>
**Output**: ```agg_debt```: Debt entries with two names reformatted, ```name_changes``` + Debt entries with two names

### Grouping Consecutive Names
<b>Goal: </b> By grouping consecutive names, standardizing names using Ancestry will go faster. <br>

[Add example here]

**Input**:```agg_debt``` (as ```og_df```) <br>
**Output**: ```agg_debt``` (as ```agg_df```): Consecutive names grouped together 

[Add expected output here] 

## Areas of Future Improvement and Research











