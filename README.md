# SPEOC-pt-1
Code repository for a Summer Project on the Economic Origins of the Constitution. Contact me at chrisliao (at) uchicago (dot) edu.

**Overview**

The name matching was executed in three steps: cleaning, fuzzy-matching, and merging. We have structured the Dropbox subdirectory to make the code runnable as-is. In more detail, the folder consists of:



1. `Data`: This folder contains all of the raw data and cleaned data. Within the Delegates, Post1790, and Pre1790 subfolders are the corresponding raw Excel sheets (copied from the dropbox) and cleaned csv files. This folder also contains `final_matching.csv` and `final_matching_post1790.csv` which list the results of our fuzzy matching.
2. `Producables`:The requested final tables are in this folder, along with a folder called ‘Separate’ containing csv files with individual tables for each type of certificate 
    1.`Delegate_Pre1790_Assets.csv` contains the assets in Pre-1790 certificates for all delegates
    2.`Delegate_Post1790_Assets.csv` contains the assets in Post-1790 certificates for all delegates 2
3.`clean_debt_files.ipynb`: This Jupyter notebook contains the code used to produce the cleaned csv files in the Data/Pre1790/Cleaned folder. Note: the post-1790 data was not cleaned.
4.`fuzzy_matching.ipynb`: This Jupyter notebook contains the code that created the`final_matching.csv`file in the Data folder that we used to identify pre-1790 debt certificates held by delegates
5.`fuzzy_matching_post1790.ipynb`: This Jupyter notebook contains the code that created the`final_matching_post1790_._csv`file in the Data folder that we used to identify post-1790 debt certificates held by delegates
6.`debt_aggregation.ipynb`: This Jupyter notebook contains the code which merges the cleaned delegate names and debt certificate/stock data using the`final_matching.csv`files. It then merges those results to produce`Delegate_Pre1790_Assets`in the`Producables`folder.
7.`debt_aggregation_post1790.ipynb`: This Jupyter notebook contains the code which merges the cleaned delegate names and debt certificate/stock data using the`final_matching_post1790.csv`files. It then merges those results to produce`Delegate_Post1790_Assets.csv`in the`Producables`folder.
8.`Results.ipynb`: This jupyter notebook contains the code which we used to generate results described in the technical report and located in the Results section.

**READMEs and Notes**

_Jupyter Notebooks_

clean_debt_files.ipynb - Cleans raw data imported into DataFrames from Excel sheets



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

<table>
  <tr>
   <td>
Row number (in raw data)
   </td>
   <td>Original First name
   </td>
   <td>New First name (s)
   </td>
   <td>New Last name(s)
   </td>
   <td>Notes
   </td>
  </tr>
  <tr>
   <td>79985-79990
   </td>
   <td>Atkinsons Executors
   </td>
   <td>
   </td>
   <td>Atkinsons
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>49584 and 49671
   </td>
   <td>David Mackey and Debt Executor
   </td>
   <td>David (name 1)
   </td>
   <td>Mackey (name 1)
<p>
Mackey (name 2)
   </td>
   <td>Name 2 has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>57475-57477
   </td>
   <td>Jacob Fisher Philip Lentz Ex.
   </td>
   <td>Jacob (name 1)
   </td>
   <td>Fisher (name 1)
<p>
Lentz (name 2)**
   </td>
   <td>Lentz has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>57636-57637
   </td>
   <td>William Allison Ex. Of Mat Mease and Co.
   </td>
   <td>Mat (name 1)
   </td>
   <td>Mease (name 1)
<p>
Allison (name 2)**
   </td>
   <td>Allison has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>40032
   </td>
   <td>Robert Morris and John Simon executor to the estate of R Gerraty
   </td>
   <td>R (name 1)
<p>
John (name 3)
   </td>
   <td>Gerraty (name 1)
<p>
Morris (name 2)**
<p>
Simon (name 3)
   </td>
   <td>Morris and John Simon have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>39714-39715
   </td>
   <td>Robert Morris and John Simon executor to the estate of
   </td>
   <td>R (name 1)
<p>
John (name 3)
   </td>
   <td>Gerraty (name 1)
<p>
Morris (name 2)**
<p>
Simon (name 3)
   </td>
   <td>See above line
   </td>
  </tr>
  <tr>
   <td>40859
   </td>
   <td>Sarah Charman for the use of Gilbert Hammond and Cornelius Tommand
   </td>
   <td>Gilbert H a m m o n (name 1)
<p>
Cornelius (name 2)
<p>
Sarah (name 3)
   </td>
   <td>d (name 1)
<p>
Tommand (name 2)
<p>
Charman (name 3)
   </td>
   <td>Sarah Charman has the title ‘executor’, Gilbert Hammond is improperly populated
   </td>
  </tr>
  <tr>
   <td>42975, 43084, 43086, 43087
   </td>
   <td>John Cavott and Jacob Aivl for Moses Dichey and George Dukey
   </td>
   <td>Moses (name 1)
<p>
George (name 2)
   </td>
   <td>Dichey (name 2)
<p>
Dukey (name 2)
   </td>
   <td>John Cavott and Jacob Aivl not properly added as executors
   </td>
  </tr>
  <tr>
   <td>53732
   </td>
   <td>Jn Nixon I M Nerbitt and Alexander Forster
   </td>
   <td>Jn (name 1)
<p>
I M (name 2)
<p>
Alexander (name 3)
   </td>
   <td>Nixon (name 2)
<p>
Nerbit (name 2)
<p>
Forster (name 3)
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>62772
   </td>
   <td>Samuel Ely and Michael Gellington Esq and Co
   </td>
   <td>Samuel (name 1)
<p>
Michael Gellington (name 2)
   </td>
   <td>Esq (name 2)
   </td>
   <td>Michael Gellington Esq improperly populated, last name of name 1 not populated
   </td>
  </tr>
  <tr>
   <td>57682
   </td>
   <td>Peter Brown & Nic Jacobs Ex & …….
   </td>
   <td>Peter (name 1)
<p>
Nic (name 2)
   </td>
   <td>Brown (name 1)
<p>
Jacobs (name 2)
   </td>
   <td>Nic Jacobs has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>4002
   </td>
   <td>John Gray &Tho Dawes Fws.to Sarah Green
   </td>
   <td>Sarah (name 1)
<p>
John (name 2)
<p>
Tho (name 3)
   </td>
   <td>Green (name 1)
<p>
Gray (name 2)
<p>
Dawes (name 3)
   </td>
   <td>John Gray and Tho Dawes have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>5566-5569
   </td>
   <td>Jn Gray & Thomas Dawes Trustees to Sach Green
   </td>
   <td>Sarah (name 1)
<p>
Jn (name 2)
<p>
Thomas (name 3)
   </td>
   <td>Green (name 1)
<p>
Gray (name 2)
<p>
Dawes (name 3)
   </td>
   <td>Jn Gray and Thomas Dawes have the title ‘executor’
<p>
This entry may be the same names as the previous
   </td>
  </tr>
  <tr>
   <td>8457
   </td>
   <td>Nathaniel Appleton and other trustees of Judah Monis Legasy
   </td>
   <td>Judah (name 1)
<p>
Nathaniel (name 2)
   </td>
   <td>Monis (name 1)
<p>
Appleton (name 2)
   </td>
   <td>Nathaniel Appleton has the title ‘executor’, entry has the note ‘legacy’ because it is probably a misspelling in the original text
   </td>
  </tr>
  <tr>
   <td>13576, 13580, 13582
   </td>
   <td>John Barrett & Sons Trustees to Creditors of John Elsworth
   </td>
   <td>John (name 1)
<p>
John (name 2)
   </td>
   <td>Elsworth (name 1)
<p>
Barrett (name 2)
   </td>
   <td>John Barrett has the title ‘executor’, entry has the note ‘creditors’
   </td>
  </tr>
  <tr>
   <td>39702-39706
   </td>
   <td>Society for Relief of Poor Masters of ships widows and children
   </td>
   <td>Same as original
   </td>
   <td>
   </td>
   <td>‘organization’ added as title
   </td>
  </tr>
  <tr>
   <td>39831-39839
   </td>
   <td>Corporation for the Relief of Poor and Distressed Presbyterian Ministers
   </td>
   <td>Same as original
   </td>
   <td>
   </td>
   <td>‘organization’ added as title
   </td>
  </tr>
  <tr>
   <td>39846
   </td>
   <td>Corporation for relief of poor and distressed presbyterian ministers
   </td>
   <td>Same as original
   </td>
   <td>
   </td>
   <td>‘organization’ added as title
   </td>
  </tr>
  <tr>
   <td>57479
   </td>
   <td>The rector of christ and st. peters churches
   </td>
   <td>Same as original
   </td>
   <td>
   </td>
   <td>‘organization’ added as title
   </td>
  </tr>
  <tr>
   <td>40476-40479
   </td>
   <td>Jeremiah Halsey and Sarah Gaston for the Estate of Gaston Dec
   </td>
   <td>Gaston (name 1)
<p>
Jeremiah (name 2)
<p>
Sarah (name 3)
   </td>
   <td>Dec (name 1)
<p>
Halsey (name 2)
   </td>
   <td>Jeremiah Halsey and Sarah have the title ‘executors’, last name of name 3 not populated, entry has the note ‘estate’
   </td>
  </tr>
  <tr>
   <td>40520-40524
   </td>
   <td>Wm Allison & Sam Caldwell Ex to the est of David Caldwell for children
   </td>
   <td>David (name 1)
<p>
Sam (name 2)
<p>
Wm (name 3)
   </td>
   <td>Caldwell (name 1)
<p>
Caldwell (name 2)
<p>
Allison (name 3)
   </td>
   <td>Sam Caldwell and Wm Allison have the title ‘executor’, entry has the note ‘estate for children’
   </td>
  </tr>
  <tr>
   <td>40602
   </td>
   <td>Jacob Brush & Mary Wroop to the est of Jacob Carver Ded
   </td>
   <td>Jacob (name 1)
<p>
Jacob (name 2)
<p>
Mary (name 3)
   </td>
   <td>Carver (name 1)
<p>
Wroop (name 2)
<p>
Carver (name 3)
   </td>
   <td>Jacob Wroop and Mary Carver have the title ‘executor’, entry has the note ‘estate, deceased’
   </td>
  </tr>
  <tr>
   <td>42847
   </td>
   <td>Mathew Greer & Mathew Greer for the heirs of Thomas Jones Deceased
   </td>
   <td>Thomas (name 1)
<p>
Mathew (name 2)
   </td>
   <td>Jones (name 1)
<p>
Greer (name 2)
   </td>
   <td>Mathew Greer has the title ‘executor’, entry has the note ‘heirs, deceased’
   </td>
  </tr>
  <tr>
   <td>45757
   </td>
   <td>Joseph Jacket and Anthany Jacket Trustees of Presbyterian Congregation N town
   </td>
   <td>Presbyterian Congregation N town (name 1)
<p>
Joseph (name 2)
<p>
Anthany (name 3)
   </td>
   <td>Jacket (name 2)
<p>
Jacket (name 3)
   </td>
   <td>‘organization’ added as title for name 1
<p>
name 2 and name 3 have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>46926-46927
   </td>
   <td>Isaac Roush & Mary Bldney of Jacob Carver
   </td>
   <td>Jacob (name 1)
<p>
Mary (name 2)
<p>
Issac (name 3)
   </td>
   <td>Carver (name 1)
<p>
Bldney (name 2)
<p>
Roush (name 3)
   </td>
   <td>Mary Bldney and Isaac Roush have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>47554
   </td>
   <td>Samuel Johnston Inna Hanna and I Johnston in trust for the Hierrs of Phil Johnston
   </td>
   <td>Phil (name 1)
<p>
Samuel (name 2)
<p>
Inna Hanna (name 3)
   </td>
   <td>Johnston (name 1)
<p>
Johnston (name 2)
<p>
Johnston (name 3)
   </td>
   <td>Samuel Johnston and Inna Hanna Johnston have the title ‘executor’, entry has the note ‘heirs’
   </td>
  </tr>
  <tr>
   <td>47760
   </td>
   <td>Michele Shubart For Corporation of Michelle & Zion Churches
   </td>
   <td>Corporation of Michelle & Zion Churches (name 1)
<p>
Michele (name 2)
   </td>
   <td>Shubart (name 2)
   </td>
   <td>‘organization’ added as title for name 1
<p>
Name 2 has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>50299
   </td>
   <td>Ed Keasby & J Bilber by the Ers of J Dickinson
   </td>
   <td>J (name 1)
<p>
Ed (name 2)
<p>
J (name 3)
   </td>
   <td>Dickinson
<p>
Keasby
<p>
Bilber
   </td>
   <td>J Dickinson and Ed Keasby have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>51369
   </td>
   <td>Gen. Kelehner and Pr. Sheser Esq. to State of Conrad Scheele
   </td>
   <td>Conrad (name 1)
<p>
Gen. (name 2)
<p>
Pr. Sheser (name 3)
   </td>
   <td>Scheele (name 1)
<p>
Kelehner (name 2)
<p>
Esq. (name 3)
   </td>
   <td>Name 2 and name 3 have the title ‘executor’, 
<p>
Gen. might be the title general
<p>
Pr. Sheser Esq. improperly populated
   </td>
  </tr>
  <tr>
   <td>53040-53041
   </td>
   <td>Andrew Hagenbach and Catherine Brobst Guardians of John Brobst
   </td>
   <td>John (name 1)
<p>
Andrew (name 2)
<p>
Catherine (name 3)
   </td>
   <td>Brobst (name 1)
<p>
Hagenbach (name 2)
<p>
Brobst (name 3)
   </td>
   <td>Andrew Hagenbach and Catherine Brobst have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>53692-53693
   </td>
   <td>Robert Patterson Guardin for Sarah and Mary Stewart
   </td>
   <td>Sarah (name 1)
<p>
Mary (name 2)
<p>
Robert (name 3)
   </td>
   <td>Stewart (name 1)
<p>
Stewart (name 2)
<p>
Patterson (name 3)
   </td>
   <td>Robert Patterson has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>55523-55524
   </td>
   <td>Peter Knight & Sus Woodrow Ex to the Estate of H Woodrow
   </td>
   <td>H (name 1)
<p>
Peter (name 2)
<p>
Sus (name 3)
   </td>
   <td>Woodrow (name 1)
<p>
Knight (name 2)
<p>
Woodrow (name 3)
   </td>
   <td>Peter Knight and Sus Woodrow have the title ‘executors’, entry has the note ‘estate’
   </td>
  </tr>
  <tr>
   <td>55785
   </td>
   <td>James Camble NO 7015 is not on file & in supposed to the number not delivered
   </td>
   <td>Same as original
   </td>
   <td>
   </td>
   <td>Entry has ‘problem’ added as title; not cleaned
   </td>
  </tr>
  <tr>
   <td>57946
   </td>
   <td>Jere Kalbey & S Gaston to the Estate John Gaston de
   </td>
   <td>John (name 1)
<p>
Jere (name 2)
<p>
S (name 3)
   </td>
   <td>Gaston (name 1)
<p>
Kalbey (name 2)
<p>
Gaston (name 3)
   </td>
   <td>Jere Kalbey and S Gaston have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>57953
   </td>
   <td>Jer Hals by & I Gaston Ex for the Estate of Jn Gaster
   </td>
   <td>Jn (name 1)
<p>
Jer (name 2)
<p>
I (name 3)
   </td>
   <td>Gaster (name 1)
<p>
Hals (name 2)
<p>
Gaston (name 3)
   </td>
   <td>Jer Hals and I Gaston have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>59865
   </td>
   <td>John Smith and James McDonald Guardian of the Heirs of John Gibson
   </td>
   <td>John (name 1)
<p>
John (name 2)
<p>
James (name 3)
   </td>
   <td>Gibson (name 1)
<p>
Smith (name 2)
<p>
McDonald (name 3)
   </td>
   <td>John Smith and James McDonald have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>61972
   </td>
   <td>Ex of William Stadlerman and Pk Lickon Ex of William Stadlerman
   </td>
   <td>William (name 1)
<p>
Pk (name 2)
   </td>
   <td>Stadlerman (name 2)
<p>
Lickon (name 2)
   </td>
   <td>Pk Lickon has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>69329
   </td>
   <td>Michael Schubert for St Michael and Zeus Corporation
   </td>
   <td>St Michael and Zeus Corporation (name 1)
<p>
Michael (name 2)
   </td>
   <td>Schubert (name 2)
   </td>
   <td>Name 1 has the title of ‘organization’, Michael Schubert has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>70248-700249
   </td>
   <td>John Steinmetz for Corperetion of F Mich & Lions Cer
   </td>
   <td>Corperetion of F Mich & Lions Cer (name 1)
<p>
John (name 2)
   </td>
   <td>Steinmetz (name 2)
   </td>
   <td>Name 1 has the title of ‘organization’, John Steinmetz has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>72127
   </td>
   <td>Jon Steinmetz for St Michaels and Zions Cerpreatere
   </td>
   <td>St Michaels and Zions Cerpreatere (name 1)
<p>
Jon (name 2)
   </td>
   <td>Steinmetz (name 2)
   </td>
   <td>Name 1 has the title of ‘organization’, Jon Steinmetz has the title ‘executor’
<p>
Similarity to above two entries?
   </td>
  </tr>
  <tr>
   <td>71034-71037
   </td>
   <td>A and J J Caldwell for EvMitchell
   </td>
   <td>Ev (name 1)
<p>
A (name 2)
<p>
J J (name 3)
   </td>
   <td>Mitchell (name 1)
<p>
Caldwell (name 2)
<p>
Caldwell (name 3)
   </td>
   <td>A Caldwell and J J Caldwell have the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>73788, 73790-73791
   </td>
   <td>Capt Samuel Wilman and Co.
   </td>
   <td>Sam
   </td>
   <td>Wilman
   </td>
   <td>Sam Wilman has the title ‘Capt’
   </td>
  </tr>
  <tr>
   <td>59392-59393
   </td>
   <td>Paris Brothers and co.
   </td>
   <td>
   </td>
   <td>Paris
   </td>
   <td>Entry has the note ‘brothers’
   </td>
  </tr>
  <tr>
   <td>59558, 59560
   </td>
   <td>GS.Dewint & Co
   </td>
   <td>GS
   </td>
   <td>Dewint
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>40274
   </td>
   <td>Margarett Grant herself and heirs
   </td>
   <td>Margaret
   </td>
   <td>Grant
   </td>
   <td>Entry has the note ‘heirs’ and no original text, Margaret is missing the second t
   </td>
  </tr>
  <tr>
   <td>57471
   </td>
   <td>Hre Rest & Ch & St Pr Chumess
   </td>
   <td>Hre (name 1)
<p>
St Pr (name 2)
   </td>
   <td>Rest (name 1)
<p>
Chumess (name 2)
<p>
Ch (name 3)
   </td>
   <td>Could be referring to a Church of St. Peter
   </td>
  </tr>
  <tr>
   <td>5364-5365
   </td>
   <td>Ebenezer Storer Treasurer H College
   </td>
   <td>H College (name 1)
<p>
Ebenezer (name 2)
   </td>
   <td>Storer (name 2)
   </td>
   <td>Name 1 has the title ‘organization’, name 2 has the title ‘treasurer’
   </td>
  </tr>
  <tr>
   <td>7541
   </td>
   <td>Job Cushing Treasurer for Shrewsbury
   </td>
   <td>Shrewsbury (name 1)
<p>
Job (name 2)
   </td>
   <td>Cushing (name 2)
   </td>
   <td>Name 1 has the title ‘organization’, name 2 has the title ‘treasurer’
   </td>
  </tr>
  <tr>
   <td>9178
   </td>
   <td>Jos Richards Treas 2nd Precinct Roxbury
   </td>
   <td>2nd Precinct Roxbury (name 1)
<p>
Jos (name 2)
   </td>
   <td>Richards (name 2)
   </td>
   <td>Name 1 has the title ‘organization’, name 2 has the title ‘treasurer’
   </td>
  </tr>
  <tr>
   <td>14250
   </td>
   <td>Dan Thurston Treasurer Church in Franklin
   </td>
   <td>Church in Franklin (name 1)
<p>
Dan (name 2)
   </td>
   <td>Thurston (name 2)
   </td>
   <td>Name 1 has the title ‘organization’, name 2 has the title ‘treasurer’
   </td>
  </tr>
  <tr>
   <td>14298, 16298-16299
   </td>
   <td>Simeon Howard Treasurer Convention of Ministers
   </td>
   <td>Convention of Ministers (name 1)
<p>
Simeon (name 2)
   </td>
   <td>Howard (name 2)
   </td>
   <td>Name 1 has the title ‘organization’, name 2 has the title ‘treasurer’
   </td>
  </tr>
  <tr>
   <td>14314
   </td>
   <td>Eli Root Treasurer of Pittsfield
   </td>
   <td>Pittsfield (name 1)
<p>
Eli (name 2)
   </td>
   <td>Root (name 2)
   </td>
   <td>Name 1 has the title ‘organization’, name 2 has the title ‘treasurer’
   </td>
  </tr>
  <tr>
   <td>20172-20173
   </td>
   <td>Society's Treasurer Lyme
   </td>
   <td>Society (name 1)
   </td>
   <td>Lyme (name 2)
   </td>
   <td>Name 1 has the title ‘organization’, name 2 has the title ‘treasurer’
   </td>
  </tr>
  <tr>
   <td>26940
   </td>
   <td>Peter & Anna Maricha
   </td>
   <td>Peter (name 1)
<p>
Anna (name 2)
   </td>
   <td>Maricha (name 1)
<p>
Maricha (name 2)
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>27215
   </td>
   <td>Myndert & Mary Van Schaick
   </td>
   <td>Myndert (name 1)
<p>
Mary (name 2)
   </td>
   <td>Van Schaick (name 1)
<p>
Van Schaick (name 2)
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>3751
   </td>
   <td>Sam Austin exec to Sam Hasting
   </td>
   <td>Sam (name 1)
   </td>
   <td>Hasting (name 1)
<p>
Austin (name 2)**
   </td>
   <td>Austin has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>3987
   </td>
   <td>William Gordon Treasurer to the Convention of Ministers
   </td>
   <td>William
   </td>
   <td>Gordon Treasurer to the Convention of Ministers
   </td>
   <td>Entry not properly cleaned
   </td>
  </tr>
  <tr>
   <td>4638-4639
   </td>
   <td>Daniel Thurston Treas Church Wrentham
   </td>
   <td>Daniel 
   </td>
   <td>Thurston Treas Church Wrentham
   </td>
   <td>Entry not properly cleaned
   </td>
  </tr>
  <tr>
   <td>5375
   </td>
   <td>Anna Biglow Guardian to her Children
   </td>
   <td>Anna
   </td>
   <td>Biglow Guardian to her Children
   </td>
   <td>Entry not properly cleaned
   </td>
  </tr>
  <tr>
   <td>5660
   </td>
   <td>Joseph Miller Treas Westminster
   </td>
   <td>Joseph
   </td>
   <td>Miller Treas Westminster
   </td>
   <td>Entry not properly cleaned
   </td>
  </tr>
  <tr>
   <td>4991
   </td>
   <td>Joseph Allen Executor to B Winchester
   </td>
   <td>B (name 1)
   </td>
   <td>Winchester (name 2)
<p>
Allen (name 2)**
   </td>
   <td>Name 2 has the title ‘executor’
   </td>
  </tr>
  <tr>
   <td>79151-79212, 79215-79217
   </td>
   <td>SD George and Comp.
   </td>
   <td>SD George (name 1)
   </td>
   <td>Comp. (name 1)
<p>
Comp. (name 2)
   </td>
   <td>Entry not properly cleaned, original text accidentally populated in cleaning notes
   </td>
  </tr>
  <tr>
   <td>67545
   </td>
   <td>Simon Dreisbach For Estates and John fox
   </td>
   <td>Simon Dreisbach (name 1)
<p>
John (name 2)
   </td>
   <td>Estates (name 1)
<p>
fox (name 2)
   </td>
   <td>Simon Dresibach improperly populated
   </td>
  </tr>
</table>




* Marine office certificates - removes entries with ‘deceased’ and ‘estate’, adding notes to a cleaning notes column
    * Special cases: see chart, Hoov and Harrison were split into two last name columns

<table>
  <tr>
   <td>
Row number 
   </td>
   <td>Original First name
   </td>
   <td>Original Last name
   </td>
   <td>New First name
   </td>
   <td>New Last name(s)
   </td>
   <td>Notes
   </td>
  </tr>
  <tr>
   <td>84-87
   </td>
   <td>The Estate of John Young dee The Estate of John Young Deceased
   </td>
   <td>Young
   </td>
   <td>John
   </td>
   <td>Young
   </td>
   <td>estate, deceased
   </td>
  </tr>
  <tr>
   <td>129
   </td>
   <td>Weaver deed
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>Weaver
   </td>
   <td>deed
   </td>
  </tr>
  <tr>
   <td>188
   </td>
   <td>Moses Bush & Sons
   </td>
   <td>Bush
   </td>
   <td>Moses
   </td>
   <td>Bush
   </td>
   <td>sons
   </td>
  </tr>
  <tr>
   <td>741
   </td>
   <td>J Mc Nesbitt & Co
   </td>
   <td>Nesbitt
   </td>
   <td>J Mc
   </td>
   <td>Nesbitt
   </td>
   <td>Co
   </td>
  </tr>
  <tr>
   <td>777
   </td>
   <td>Hoov and Harrison
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>Hoov (name 1)
<p>
Harrison (name 2)
   </td>
   <td>
   </td>
  </tr>
</table>




* Pierce certificates - strips entries and removes entries with no last name, added a second set of name columns
    * Special cases - see chart; some split into two names

<table>
  <tr>
   <td>
Row number (in raw data)
   </td>
   <td>Original First name
   </td>
   <td>Original Last name
   </td>
   <td>New First name(s)
   </td>
   <td>New Last name(s)
   </td>
  </tr>
  <tr>
   <td>850
   </td>
   <td>Thomas G Jr
   </td>
   <td>Alford
   </td>
   <td>Thomas G
   </td>
   <td>Alford Jr
   </td>
  </tr>
  <tr>
   <td>851
   </td>
   <td>Thomas G Sr
   </td>
   <td>Alford
   </td>
   <td>Thomas G
   </td>
   <td>Alford Sr
   </td>
  </tr>
  <tr>
   <td>1258-1259
   </td>
   <td>Tho G Jr
   </td>
   <td>Alford
   </td>
   <td>Tho G
   </td>
   <td>Alford Jr
   </td>
  </tr>
  <tr>
   <td>1260
   </td>
   <td>Tho G Sr
   </td>
   <td>Alford
   </td>
   <td>Tho G
   </td>
   <td>Alford Sr
   </td>
  </tr>
  <tr>
   <td>5627
   </td>
   <td>P. & J. Bemant &. Porter
   </td>
   <td>
   </td>
   <td>P. (name 1)
<p>
J. (name 2)
   </td>
   <td>Bemant (name 1)
<p>
Porter (name 2)
   </td>
  </tr>
  <tr>
   <td>5957
   </td>
   <td>John (see Berrick)
   </td>
   <td>Benrick
   </td>
   <td>John
   </td>
   <td>Berrick
   </td>
  </tr>
  <tr>
   <td>7169
   </td>
   <td>Blanchard & Russell
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>Blanchard (name 1)
<p>
Russell (name 2)
   </td>
  </tr>
  <tr>
   <td>15062
   </td>
   <td>James (alias Cady)
   </td>
   <td>Church
   </td>
   <td>James
   </td>
   <td>Church
   </td>
  </tr>
  <tr>
   <td>16505
   </td>
   <td>William
   </td>
   <td>Code (or Coad)
   </td>
   <td>William
   </td>
   <td>Code (name 1)
<p>
Coad (name 2)
   </td>
  </tr>
  <tr>
   <td>17745
   </td>
   <td>John F (?)
   </td>
   <td>Conrad
   </td>
   <td>John F
   </td>
   <td>Conrad
   </td>
  </tr>
  <tr>
   <td>20901
   </td>
   <td>S & Delano Darting
   </td>
   <td>
   </td>
   <td>S. (name 1)
<p>
Delano (name 2)
   </td>
   <td>Darting (name 1)
<p>
Darting (name 2)
   </td>
  </tr>
  <tr>
   <td>45413
   </td>
   <td>M for J. Jones
   </td>
   <td>Jones
   </td>
   <td>J.
   </td>
   <td>Jones
   </td>
  </tr>
  <tr>
   <td>64460
   </td>
   <td>Ge
   </td>
   <td>Peffer (or Pepper)
   </td>
   <td>Ge (name 1)
<p>
Ge (name 2)
   </td>
   <td>Peffer (name 1)
<p>
Pepper (name 2)
   </td>
  </tr>
  <tr>
   <td>64656
   </td>
   <td>Ge
   </td>
   <td>Pepper (or Peffer)
   </td>
   <td>Dropped since same CN as row 64460
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>69741
   </td>
   <td>William And Lewis
   </td>
   <td>Rice
   </td>
   <td>William (name 1)
<p>
Lewis (name 1)
   </td>
   <td>Rice (name 1)
<p>
Rice (name 2)
   </td>
  </tr>
  <tr>
   <td>71384
   </td>
   <td>alias Hodge S
   </td>
   <td>Rollins
   </td>
   <td>Hodge S
   </td>
   <td>Rollins
   </td>
  </tr>
  <tr>
   <td>72701
   </td>
   <td>John P Jr.
   </td>
   <td>Salter
   </td>
   <td>John P
   </td>
   <td>Salter Jr.
   </td>
  </tr>
  <tr>
   <td>72702
   </td>
   <td>John P Sr.
   </td>
   <td>Salter
   </td>
   <td>John P
   </td>
   <td>Salter Sr.
   </td>
  </tr>
  <tr>
   <td>93305-93309
   </td>
   <td>Various different names
   </td>
   <td>TRUE
   </td>
   <td>Same as original
   </td>
   <td>True
   </td>
  </tr>
  <tr>
   <td>93310
   </td>
   <td>Benjamin & Donnelly
   </td>
   <td>X
   </td>
   <td>
   </td>
   <td>Benjamin (name 1)
<p>
Donnelly (name 2)
   </td>
  </tr>
</table>




* State liquidated debt - removes empty rows; splits entries with ‘&’ or ‘and’ into two names; removes phrases like ‘and co’, ‘& son’ , ‘& others’ and adds them to a Cleaning notes column; removes ‘estates’, ‘heir of’, and ‘deceased’, adding those to the notes 
    * Special cases - see chart; some entries in PA had ‘esastate’ and those were treated the same as ‘estate’

<table>
  <tr>
   <td>
State
   </td>
   <td>Row
   </td>
   <td>Original First name
   </td>
   <td>New First name
   </td>
   <td>New Last name
   </td>
   <td>New title
   </td>
  </tr>
  <tr>
   <td>DE
   </td>
   <td>445-446
   </td>
   <td>Trusts of Wilmington Academy
   </td>
   <td>Same as original
   </td>
   <td>
   </td>
   <td>organization
   </td>
  </tr>
  <tr>
   <td>MA
   </td>
   <td>2093
   </td>
   <td>The Estate of Capt John Williams
   </td>
   <td>John
   </td>
   <td>Williams
   </td>
   <td>capt
   </td>
  </tr>
  <tr>
   <td>NY
   </td>
   <td>7310
   </td>
   <td>Trustees Of & Davids Church
   </td>
   <td>Trustees of Davids Church
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>PA
   </td>
   <td>4425-4426
   </td>
   <td>John Maxwell Nesbitt & Coy
   </td>
   <td>John Maxwell
   </td>
   <td>Nesbitt
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>PA
   </td>
   <td>8800
   </td>
   <td>Joseph Ball & Coy
   </td>
   <td>Joseph
   </td>
   <td>Ball
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>PA
   </td>
   <td>7340 and 7478
   </td>
   <td>John Finney McClenaghan
   </td>
   <td>John Finney
   </td>
   <td>McClenaghan
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>RI
   </td>
   <td>655-656
   </td>
   <td>Estate of Col.Chris .Greene
   </td>
   <td>Chris
   </td>
   <td>Greene
   </td>
   <td>Col
   </td>
  </tr>
</table>


fuzzy_matching.ipynb - runs cleaned delegates and debt certificates through a fuzzy matching algorithm, yielding`final_matching.csv_



* First, uses process.extract with a threshold of 85 to form a list of possible matches
    * Note: process.extract uses a weighted ratio of all four fuzz ratios
* Next, let m = min(# of words in name 1, # of words in name 2). This is the minimum threshold of word-pairs between the two names that must have a threshold score of 90 (a word pair is a pair of words consisting of one word from each of the two names that were considered to be a match)
* If the match passes both steps, it is added to the csv file
* See the Methods section of the report for a better explanation of step 2

fuzzy_matching_post1790.ipynb - uses the same algorithm as`fuzzy_matching.ipynb`to generate`final_matching_post1790_._csv_

debt_aggregation.ipynb - merges state and constitutional convention delegates’ on the matched names from`final_matching.csv_, then uses full names to merge with the cleaned pre-1790 loan certificate data to compile the total sum value and certificate count of each certificate type for each delegate



* Produces`Delegate_Pre1790_Assets.csv_

debt_aggregation_post1790.ipynb - uses the same process to merge matched names with the post-1790 stocks and compile the total sum value and count of each type of stock for each delegate



* Produces`Delegates_Post1790_Assets.csv_

Results.ipynb - code which utilizes fuzzy matching and aggregated debt csv files to generate the tables and charts found in the Results section of our technical report

_Csv Files_

**Raw data:**



* Delegates
    *`Data/Delegates/constitutional_convention_1787.xlsx_
    *`Data/Delegates/State Delegates.xlsx_
* Pre1790 Debt Files
    *`Data/Pre1790/`contains the raw Pre-1790 debt certificates that were copied over dropbox
* Post1790 Debt Files
    *`Data/Post1790/`contains the raw Post-1790 debt certificates that were copied over dropbox, organized by state in the folders

**Cleaned Data** - products of`clean_debt_files.ipynb_



* Delegates - located in`Data/Delegates/cleaned_
    *`State_Delegates_cleaned.csv_
    *`constitutional_convention_delegates_cleaned.csv_
* Pre-1790 Debt Files - located in`Data/Pre1790/cleaned_
    *`Marine_Liquidated_Debt_Certificates_cleaned.csv_
    *`Pierce_Certs_cleaned_2021.csv_
    *`liquidated_debt_certificates_CT_cleaned.csv_
    *`liquidated_debt_certificates_DE_cleaned.csv_
    *`liquidated_debt_certificates_MA_cleaned.csv_
    *`liquidated_debt_certificates_NH_cleaned.csv_
    *`liquidated_debt_certificates_NJ_cleaned.csv_
    *`liquidated_debt_certificates_NY_cleaned.csv_
    *`liquidated_debt_certificates_PA_stelle_cleaned.csv_
    *`liquidated_debt_certificates_PA_story_cleaned.csv_
    *`liquidated_debt_certificates_RI_cleaned.csv_
    *`Loan_office_certificates_9_states_cleaned.csv_

**Intermediary Data ** 



*`final_matching.csv`- Lists all the fuzzy matches matches generated by`fuzzy_matching.ipynb_, with the initial process.extract score in the Scores column
    * Used in`debt_aggregation.ipynb`to generate totals of delegate assets
*`final_matching_post1790.csv`- Lists all the fuzzy matches matches generated by`fuzzy_matching_post1790.ipynb_, with the initial process.extract score in the Scores column
    * Used in`debt_aggregation_post1790.ipynb`to generate totals of delegate assets
*`state_companies.csv`- Lists all the entries from`Loan_office_certificates_9_states.xlsx`which contained ‘&’ or ‘and’ with two last names
    * Ex. Clark & Nightingale

**Final Data**



*`Delegates_Pre1790_Assets.csv`- final compiled table of pre-1790 assets of delegates, formatted as requested
    * Product of`debt_aggregation.ipynb_
*`Delegates_Post1790_Assets.csv`- final compiled table of post-1790 assets of delegates, formatted requested
    * Product of`debt_aggregation_post1790.ipynb_
* Separate - aggregated debt for each type of asset
    *`ASD_debt_Matched.csv_
    *`CD_debt_Matched.csv_
    *`Loan_Office_Certificates_Matched.csv_
    *`Marine_Certificates_Matched.csv_
    *`Pierce_Certificates_Matched.csv_
    *`State_Certificates_Matched.csv_

**Something I wish we did:**

Identify company owners - see our incomplete list at`state_companies.csv_



* This would give us a more complete way to calculate a person’s holdings

Change abbreviated names (Thm - Thomas, J/Jn to John/Jonathan)
