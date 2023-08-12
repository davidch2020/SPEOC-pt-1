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

| title_org   | title_new   | first_name_org   | last_name_org   | first_name_new   | last_name_new   | cleaning case   | file_loc   | org_index   |
|-------------|-------------|------------------|-----------------|------------------|-----------------|-----------------|------------|-------------|

Source: ```name_changes```

```python 
print(name_changes.to_markdown()) 
```

### Company Names
**Goal**: Some debt entries are actually company names or represent a group of people (example: ```James Vernon & Co.```).

|      | to whom due - first name   |
|-----:|:---------------------------|
| 5776 | Henry Wisner & Co          |
| 8879 | James Mc Farlane & others  |

Source: ```agg_debt```

```python
print(agg_debt['to whom due | first name'].loc[[5776, 8879]].to_markdown())
```

**Input**: ```agg_debt```, ```name_changes```<br>
**Output**: ```agg_debt```: Company names changed to people's names, ```name_changes``` + Company names

|    | first_name_org    |   last_name_org | first_name_new   | last_name_new   |
|---:|:------------------|----------------:|:-----------------|:----------------|
|  0 | Henry Wisner & Co |             nan | Henry            | Wisner          |

Source: ```name_changes```

### Cleaning Entries with Two Names
<b>Goal: </b>There are debt entries that have two names in a single cell: ```NY_2422: Messes Williamson & Beckman```. The plan is to split the name across the first name and last name columns. <br>

|        | to whom due - first name            |
|-------:|:------------------------------------|
|    182 | Furman & Hunt                       |
| 178682 | William Rigden and Edward Middleton |

Source: ```agg_debt```

**Input**: ```agg_debt```, ```name_changes``` <br>
**Output**: ```agg_debt```: Debt entries with two names reformatted, ```name_changes``` + Debt entries with two names

|      | first_name_org   |   last_name_org | first_name_new   | last_name_new      |
|-----:|:-----------------|----------------:|:-----------------|:-------------------|
| 1119 | Furman and Hunt  |             nan |                  | ['Furman', 'Hunt'] |

Source: ```name_changes```

### Handle Abbreviations of Names
<b>Goal: </b>There are individuals who have a handwritten abbreviation of a name in their debt entry. Thanks to Chris, he found a website with all these [abbreviations](https://hull-awe.org.uk/index.php/Conventional_abbreviations_for_forenames). 

|        | to whom due - first name   | to whom due - last name   |
|-------:|:---------------------------|:--------------------------|
| 102117 | And                        | Wardleberger              |

Source: ```agg_debt```

**Input**: ```agg_debt```, ```name_changes```, ```abbreviations``` dictionary <br>
**Output**: ```agg_debt```: Renamed abbreviations, ```name_changes``` + Abbreviations

|      | first_name_org   | last_name_org   | first_name_new   | last_name_new   |
|-----:|:-----------------|:----------------|:-----------------|:----------------|
| 3683 | And              | Wardleberger    | Andrew           | Wardleberger    |

Source: ```name_changes```

### Grouping Consecutive Names
<b>Goal: </b> By grouping consecutive names, standardizing names using Ancestry will go faster. <br>

[Add example here]

**Input**:```agg_debt``` (as ```og_df```) <br>
**Output**: ```agg_debt``` (as ```agg_df```): Consecutive names grouped together 

[Add expected output here] 

### Ancestry Search : ```ancestry_search_david.ipynb```
<b>Goal: </b>Multiple different spellings of a name can be referring to the same identity. We will use a phonetics library and Ancestry to fix this. An example: ```David Schaffer``` and ```David Schafer``` from `MA`. 

**Input**: ```agg_debt```, ```name_changes```
**Output**: ```ancestry_name_changes```, ```agg_debt``` : Ancestry name fixes, ```name_changes``` + Ancestry name fixes 

## Areas of Future Improvement and Research











