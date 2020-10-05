# Code used to analyse dropped and new voter data between 2018 to 2020.

Files needed to run the code:

### data/actually_dropped.csv file format:

Format: ',' delimited file with '"' escape characters, and a single header row.
Description: Data for a list of voters which were registered in late 2018 but not in early 2020.
Columns: REGISTRATION_NUMBER,LAST_NAME,FIRST_NAME,GENDER,BIRTHDATE,INACTIVE_REASON,COUNTY_NAME,PARTY_LAST_VOTED,COUNTY_PRECINCT_ID

### data/Registered_Voter_Precincts.csv

Format: ',' delimited file with '"' escape characters, and a single header row.
Description: Precinct data for a list of voters registered in late 2018.
Columns: REGISTRATION_NUMBER,COUNTY_NAME,COUNTY_PRECINCT_ID

### data/newly_added.csv

Format: ',' delimited file with '"' escape characters, and a single header row.
Description: Data for a list of voters which were not registered in late 2018 but are registered as of early 2020
Columns: REGISTRATION_NUMBER,LAST_NAME,FIRST_NAME,GENDER,BIRTHDATE,- Filler Column -,COUNTY_NAME,PARTY_LAST_VOTED,COUNTY_PRECINCT_ID

### data/precinct_votes_2018.csv

Format: ',' delimited file with '"' escape characters, and a single header row.
Description: Aggregate voting data for all precincts from the 2018 general election from https://github.com/openelections/openelections-data-ga.
Columns: County,Precinct ID,Rep,Dem,Ind,Total

### data/geocoding_dropped.csv

Format: ',' delimited file with '"' escape characters, and a single header row.
Description: Geocoded locations for all 2018 proposed dropped voters.
Columns: Registration Number, Registered County, Registered Precinct Id, Geocoded County, Geocoded Precinct Name, Geocoded Precinct Id

### data/geocoding_new.csv

Format: ',' delimited file with '"' escape characters, and a single header row.
Description: Geocoded locations for all 2018 proposed dropped voters.
Columns: Registration Number, - Filler Column -, - Filler Column -, Geocoded County, Geocoded Precinct Name, Geocoded Precinct Id

### data/vtd2018/*
Shapefile data of the Georgia precincts from http://www.legis.ga.gov/Joint/reapportionment/en-US/default.aspx