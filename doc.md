## data_raw

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
