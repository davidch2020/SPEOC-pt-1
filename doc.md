# Transforming Post-1790 CD Debt Data

## Objective

Turn raw post-1790 continental debt (CD) security data into an organized table indexed by individuals, 

### Inputs

1. Raw Data

   1. [Post-1790 Continental Debt Files](data_raw/pre1790): csv files with suffix CD
   2. Examples
      1. Connecticut: [CT_post1790_CD_ledger.xlsx](data_raw/post1790/CT_post1790_CD_ledger.xlsx) 
      2. Georgia: [T694_GA_Loan_Office_CD.xlsx](data_raw/post1790/GA/T694_GA_Loan_Office_CD.xlsx)

2. Various cleaning files

   
   
   1. 

   2. 
   3. [name_agg.csv](cleaning_CD/clean_tools/name_agg.csv): database of names spelled differently that correspond to the same identity
   4. [group_name_state.csv](cleaning_CD/clean_tools/group_name_state.csv): database of names with locations in multiple states that correspond to the same identity
   5. [occ_correction.csv](cleaning_CD/clean_tools/occ_correction.csv): database of occupation name changes for data cleaning purposes

### Ouputs 

1. Preliminary Data Checkpoints
   1. 
   2. [aggregated_CD_post1790_names.csv](cleaning_CD/data_clean/aggregated_CD_post1790_names.csv): [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv) with cleaned names
   3. [name_list.csv](cleaning_CD/clean_tools/name_list.csv): List of all identities in our raw debt data with cleaned names and geographies
      1. Identities have not been aggregated (two slightly mispelled names representing the same identity are denoted as separate identities)
   4. Scraping
      1. [scrape_ids_prelims.csv](cleaning_CD/scrape_tools/scrape_ids_prelim.csv): preliminary dataset of matched identities from Ancestry.com census scraper 
      2. [scrape_results_prelim.csv](cleaning_CD/clean_tools/scrape_results_prelim.csv): preliminary dataset of data for matched identities from Ancestry.com census scraper 
      3. [scrape_ids.csv](cleaning_CD/scrape_tools/scrape_ids.csv): cleaned preliminary dataset of matched identities from Ancestry.com census scraper 
      4. [scrape_results.csv](cleaning_CD/clean_tools/scrape_results.csv): cleaned preliminary dataset of data for matched identities from Ancestry.com census scraper 
2. Final Data
   1. [final_data_CD.csv](cleaning_CD/data_clean/final_data_CD.csv): final table, indexed by individual, of aggregate CD debt holdings
   2. [match_data_CD.csv](cleaning_CD/data_clean/match_data.csv): database of ancestry.com data for final_data_CD
3. Cleaning Logs
   1. [final_cw_all.csv](cleaning_CD/data_clean/check/geography_cw.csv): crosswalk mapping raw data geography to cleaned geography
   2. [change_df_CD](cleaning_CD/data_clean/check/town_occ_agg_check.csv): crosswalk mapping aggregation of multiple towns/occupations (raw data) to one town/occupation ([aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv))
4. For the Future
   1. 


## Process

### 1. Adding Each Individual's Geography 

**Code**: 

- [clean_1_geo.ipynb](cleaning_CD/clean_tools/clean_1_geo.ipynb) combines the raw CD debt data from all states into one dataset and processes the given geography colum

**Inputs**:

- Raw Data

  1. [Post-1790 Continental Debt Files](data_raw/pre1790): csv files with suffix CD
  2. Examples
     1. Connecticut: [CT_post1790_CD_ledger.xlsx](data_raw/post1790/CT_post1790_CD_ledger.xlsx) 
     2. Georgia: [T694_GA_Loan_Office_CD.xlsx](data_raw/post1790/GA/T694_GA_Loan_Office_CD.xlsx)
-  [cd_raw.csv](cleaning_CD/clean_tools/cd_raw.csv): arguments for importing state CD files
- [zip_code_database.xls](data_raw/census_data/zip_code_database.xls): geograhical database matching towns to counties
  - Downloaded from https://www.unitedstateszipcodes.org/zip_code_database.xls?download_auth=7b5b7133a55eef6807fc6da56f62bf27 
- [town_fix.csv](cleaning_CD/clean_tools/town_fix.csv): database of changes to the gegographical classification

**Outputs (for future use)**: 

- [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv): continental debt files with final geographical classification

**Outputs (to check validity of cleaning process)**: 

- [change_df_CD](cleaning_CD/data_clean/check/town_occ_agg_check.csv): crosswalk mapping aggregation of multiple towns/occupations (raw data) to one town/occupation ([aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv))

**Steps**:  

1. Using the arguments in [cd_raw.csv](cleaning_CD/clean_tools/cd_raw.csv), the raw CD data for each state is imported and aggregated into one table
2. Our raw data (except for NY) contains a town and state column denoting the place of residence for each debtholder
   1. When an entry for the state column is missing, we impute the state loan office that the debtholder redeemed debt from
   2. When there are multiple town or occupation values for one debtholder entry, I select the value with longest string length (since it likely contains the most information). The results of this selection are in [change_df_CD](cleaning_CD/data_clean/check/town_occ_agg_check.csv). 
   3. When one debtholder entry has multiple names, I group them and note that the entry has multiple names. CT_10 has the value `Joseph Woodruff | Joseph Woodruffe` 
3. The town column in our raw data is extremely messy. Here are some of its problems
   1. The same location can be spelled multiple ways
      1. GA_24 and GA_33 have the values `Charleston South Carolina` and `Charleston` in their respective town column values
   2. The listed "town" might be a town, state or column
      1. PA_115 and PA_655 have the values `Cumberland` and `Cumb County Pennsylvania` in their respective town column values
4. Using fuzzy string matching with [zip_code_database.xls](data_raw/census_data/zip_code_database.xls), I identify whether a "town" value is a town, county or state, and reformat it
   1. For towns, I also find the corresponding county name
5. There are cases where we cannot use fuzzy string matching to clean our geographies (or less commonly, [zip_code_database.xls](data_raw/census_data/zip_code_database.xls) makes a mistake). In this case, I use [town_fix.csv](cleaning_CD/clean_tools/town_fix.csv) to make the required changes
6. Our final results are in [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv) 

`town`, `occupation` and `state`  are given columns from the raw data but post step 2

`new_town`, `new_county`, `new_state`, `country`, `name_type ` are columns created post-cleaning and represent the location of an individual

|      | town                      | state | occupation | new_town      | county          | new_state | country | name_type |
| ---: | :------------------------ | :---- | :--------- | :------------ | :-------------- | :-------- | :------ | :-------- |
|    0 | Hartford                  | CT    | Merchant   | Hartford      | Hartford County | CT        | US      | town      |
|    2 | Rhode Island              | RI    | Farmer     | nan           | nan             | RI        | US      | state     |
|  390 | City of New York          | NY    | Merchant   | New York City | New York County | NY        | US      | town      |
| 2001 | Bucks County Pennsylvania | PA    | nan        | nan           | Bucks County    | PA        | US      | county    |

```python
# generate above - run at end of notebook
print(CD_all[['town', 'state', 'occupation', 'new_town', 'county', 'new_state', 'country', 'name_type']].loc[[0,2,390, 2001]].to_markdown())
```

### 2. Cleaning Names 

**Code**: 

- [clean_2_names.ipynb](cleaning_CD/clean_tools/clean_2_names.ipynb) cleans all the names in the CD debt file

**Inputs**:

- [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv): continental debt files with final geographical classification
- [company_names_fix.csv](cleaning_CD/clean_tools/company_names_fix.csv): database of name changes for data cleaning purposes

**Outputs (for future use)**: 

- [aggregated_CD_post1790_names.csv](cleaning_CD/data_clean/aggregated_CD_post1790_names.csv): [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv) with cleaned names
- [name_list.csv](cleaning_CD/clean_tools/name_list.csv): List of all identities in our raw debt data with cleaned names and geographies
  1. Identities have not been aggregated (two slightly mispelled names representing the same identity are denoted as separate identities)

**Outputs (for future research)**

- [company_research.csv](cleaning_CD/data_clean/check/company_research.csv): list of companies we want to map to owners/identities 

**Steps**:  

1. First, I import [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv) 
2. The names in [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv) can be quite messy for various reasons
   1. One "name" value can be multiple names: CT_19 has the value `John and James Davenport` 
   2. One "name" value can have extraneous information: RI_318 has the value `John Parker as Gaurdian`
   3. One "name" value can be an institution, not a name: RI_597 has the value `Clark and Nightingale Transferred from Register | Clark and Nightingale transferred` . `Clark and Nightingale` is a company owned by Joseph Innes Clark and Joseph Nightingale. In this case, we can match a company to the owner but we may not always be able to do this
      1. [company_research.csv](cleaning_CD/data_clean/check/company_research.csv) contains the list of companies we want to find identities for
   4. One debtholder entry can contain multiple names: CT_10 has the value `Joseph Woodruff | Joseph Woodruffe` . Different names are separated by ` | `
3. In section **Known Cleaning Process**, I clean names where we know how to fix the structure
4. In section **Import Name Fixes**, I clean names that have to be manually fixed (looked at each messed up entry one by one, then added the fixed name to the spreadsheet) using [company_names_fix.csv](cleaning_CD/clean_tools/company_names_fix.csv)
   1. This process was tedious, even with GitHub copilot. I hope that this summer we can automate at least parts of this process 
5. In section **Manual Name Fixes**, I make some final name changes
6. Finally, I create a dataset of all unique identities (name + geography combinations) to feed to our scraper, outputted as [name_list.csv](cleaning_CD/clean_tools/name_list.csv)
   1. Name values that are not actually names (and for who we cannot match to a set of actual names) are excludede from this dataset
   2. NH_22's name is `The Trustees of Phillips Academy` 
   3. GA_64's name is `Jackson and Nightingale` 
7. I also create [aggregated_CD_post1790_names.csv](cleaning_CD/data_clean/aggregated_CD_post1790_names.csv), which contains debt data, the original name and the new (cleaned) name

Here are some examples of the original name and the cleaned name

|      | original                                                     | new                                                          |
| ---: | :----------------------------------------------------------- | :----------------------------------------------------------- |
|    0 | Clark and Nightingale                                        | Joseph Innes Clark \| Joseph Nightingale                     |
|    1 | Jon and Jacob Starr \| Jonathan and Jared Starr              | Jacob Starr \| Jonathan Starr \| Jared Starr                 |
|   38 | Nicholas And Hannah Cooke \| Nicholas And Hannah Coske \| Robert Crooke | Hannah Cooke \| Hannah Coske \| Nicholas Cooke \| Nicholas Coske \| Robert Crooke |

```python
# generate code
print(df_comp.loc[[0,1,38]].to_markdown())
```

### 3. Scraping Census Data	

**Code**: 

- [clean_3_scrape.ipynb](cleaning_CD/clean_tools/clean_3_scrape.ipynb) cleans all the names in the CD debt file

**Inputs**:

- [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv): continental debt files with final geographical classification
- [company_names_fix.csv](cleaning_CD/clean_tools/company_names_fix.csv): database of name changes for data cleaning purposes

**Outputs (for future use)**: 

- [aggregated_CD_post1790_names.csv](cleaning_CD/data_clean/aggregated_CD_post1790_names.csv): [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv) with cleaned names
- [name_list.csv](cleaning_CD/clean_tools/name_list.csv): List of all identities in our raw debt data with cleaned names and geographies
  1. Identities have not been aggregated (two slightly mispelled names representing the same identity are denoted as separate identities)

**Outputs (for future research)**

- [company_research.csv](cleaning_CD/data_clean/check/company_research.csv): list of companies we want to map to owners/identities 

**Steps**:  

1. First, I import [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv) 
2. The names in [aggregated_CD_post1790.csv](cleaning_CD/data_clean/aggregated_CD_post1790.csv) can be quite messy for various reasons
   1. One "name" value can be multiple names: CT_19 has the value `John and James Davenport` 
   2. One "name" value can have extraneous information: RI_318 has the value `John Parker as Gaurdian`
   3. One "name" value can be an institution, not a name: RI_597 has the value `Clark and Nightingale Transferred from Register | Clark and Nightingale transferred` . `Clark and Nightingale` is a company owned by Joseph Innes Clark and Joseph Nightingale. In this case, we can match a company to the owner but we may not always be able to do this
      1. [company_research.csv](cleaning_CD/data_clean/check/company_research.csv) contains the list of companies we want to find identities for
   4. One debtholder entry can contain multiple names: CT_10 has the value `Joseph Woodruff | Joseph Woodruffe` . Different names are separated by ` | `
3. In section **Known Cleaning Process**, I clean names where we know how to fix the structure
4. In section **Import Name Fixes**, I clean names that have to be manually fixed (looked at each messed up entry one by one, then added the fixed name to the spreadsheet) using [company_names_fix.csv](cleaning_CD/clean_tools/company_names_fix.csv)
   1. This process was tedious, even with GitHub copilot. I hope that this summer we can automate at least parts of this process 
5. In section **Manual Name Fixes**, I make some final name changes
6. Finally, I create a dataset of all unique identities (name + geography combinations) to feed to our scraper, outputted as [name_list.csv](cleaning_CD/clean_tools/name_list.csv)
   1. Name values that are not actually names (and for who we cannot match to a set of actual names) are excludede from this dataset
   2. NH_22's name is `The Trustees of Phillips Academy` 
   3. GA_64's name is `Jackson and Nightingale` 
7. I also create [aggregated_CD_post1790_names.csv](cleaning_CD/data_clean/aggregated_CD_post1790_names.csv), which contains debt data, the original name and the new (cleaned) name

Here are some examples of the original name and the cleaned name

|      | original                                                     | new                                                          |
| ---: | :----------------------------------------------------------- | :----------------------------------------------------------- |
|    0 | Clark and Nightingale                                        | Joseph Innes Clark \| Joseph Nightingale                     |
|    1 | Jon and Jacob Starr \| Jonathan and Jared Starr              | Jacob Starr \| Jonathan Starr \| Jared Starr                 |
|   38 | Nicholas And Hannah Cooke \| Nicholas And Hannah Coske \| Robert Crooke | Hannah Cooke \| Hannah Coske \| Nicholas Cooke \| Nicholas Coske \| Robert Crooke |

```python
# generate code
print(df_comp.loc[[0,1,38]].to_markdown())
```







### Census Data

[statepop.csv](data_raw/census_data/statepop.csv): https://web.viu.ca/davies/H320/population.colonies.htm

[countyPopulation.csv](data_raw/census_data/countyPopulation.csv): https://www.socialexplorer.com/tables/Census1790/R13347861

[zip_code_database.xls](data_raw/census_data/zip_code_database.xls): https://www.unitedstateszipcodes.org/zip_code_database.xls?download_auth=7b5b7133a55eef6807fc6da56f62bf27

### Delegates Data

Both files from DB

### Post-1790 Debt Redemption Coupons

All files from DB

### Pre-1790 Debt Redemption Coupons

All files from DB

### shapefiles

[historicalcounties](data_raw/shapefiles/historicalcounties): IPUMS NHGIS, 1790 census data, 1790 County 2000 Tiger/Line GIS

[historicalstates](data_raw/shapefiles/historicalstates): https://digital.newberry.org/ahcb/downloads/gis/US_AtlasHCB_StateTerr_Gen001.zip 



## cleaning

1. `clean_raw.ipynb`  - aggregates towns + occupations, then assigns counties to towns and organizes geography
   1. **things to do**
      1. Add comments
      2. Find a way to make changing/cleaning final_cw_all more clean (right now it's a mess)
      3. Check that `geography_cw.csv` and `town_occ_agg.csv` are correct
      4. Convert notebook into script

**next steps**

1. clean occupations (AvgDeptPerOccupation.ipynb)
2. clean names 







data_cleaning_cl.ipynb

helper function section, raw data import section, cleaning data section

cleaning steps

1. combine multiple different town, occupation, state columns into 1 town, occupation and state column each
2. unify locations (when possible)

To do's

1. Comment code
2. check the change_df, see if there's anything that we should flag (example VA_ASD 195)
3. check town name matching - missing vs. wrong (final_cw_all)
4. make process where I modify final_cw_all more clean (perhaps import dataframe of changes or write a function)



scraping - check city, without checking county
