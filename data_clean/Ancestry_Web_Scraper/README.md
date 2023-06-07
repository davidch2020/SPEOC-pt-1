# Ancestry Web Scraping

The purpose of this application is to find the populations of all towns in ```final_data_CD.csv```. This way, the percentage of people in each town that held debt can be found. Next, the populations of **all** towns in Ancestry's database were found. This way, the program wouldn't have to be run again when assumed state debt was added. 

## What Libraries Did I Use?
In order to create this application, the two most important Python libraries I used were Selenium and Pandas. Selenium is a Python library that can act as a web scraper. The Pandas library allowed me to convert the data I gathered from Ancestry's website into readable Dataframes and then into a CSV file. 

## Challenges 
Most issues I encountered came from using Selenium. Although Selenium gave me many different errors, I noticed that it oftentimes crashed while going through the list of towns. Although I am still not fully sure why, my best guess at this moment is that it could not handle opening so many tabs. This problem will need further testing, but as of right now, I simply added a try-catch statement. 

## Running the Program (Step-by-Step)

1. Pull this GitHub repository. 
2. The latest version of Python is assumed to be installed. 
3. Install Selenium, Pandas using ```pip install Selenium``` and ```pip install Pandas```, respectively. 
4. Open ```web_scraper.ipynb```.
5. Run all code cells going from the top, up to the section labeled "Part II". Details for each code cell can be found in the headers in ```web_scraper.ipynb```. 
6. By this point, hopefully you have a .csv file titled ```town_pops_clean.csv``` that has all the populations for every town in ```final_data_CD.csv```. 
7. Run all code in "Part II". This will return a .csv file: ```town_pops_2.csv```. This contains the populations of all the towns in Ancestry's databases. Further instructions and details can be found underneath the headers of each section as well as in the comments. 
8. If needed, you can run the error handling code (Fix Formatting - Rerunning the Program), again. Just make sure filenames have been changed from ```town_pops.csv``` to ```town_pops_2.csv```. This will return a new file, ```town_pops_clean_2.csv```
9. Note: I actually removed ```town_pops_clean.csv``` since it was no longer needed and renamed ```town_pops_clean_2.csv``` to ```town_pops_clean.csv```. 

## Credits
Thanks to ```@liaochris``` for all his help on this. 


