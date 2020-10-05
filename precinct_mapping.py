import fiona
import csv

def normP(precinct):
	return "".join(precinct.split()).lstrip("0").lower()

def normC(county):
	return "".join(county.split()).lower()

def normPID(precinct_id):
	return precinct_id.lower().strip("0")

def getCountyName(feat):
	return county_id_to_county_name[int(feat['properties']['CTYNUMBER'])]

def getPrecinctID(feat):
	return feat['properties']['PRECINCT_I']

def getPrecinctName(feat):
	return feat['properties']['PRECINCT_N']

county_id_to_county_name = dict()
with open("data/county_ids.csv") as ctyids:
	for line in ctyids:
		county_id, county_name = tuple(line.split(","))
		county_id_to_county_name[int(county_id)] = county_name

precinct_id_to_name = dict()
precinct_list = list()

for feat in fiona.open("data/vtd2018/VTD2018-Shapefile.shp"):
	if feat['properties']['CTYNUMBER'] == None:
		continue
	county = normC(getCountyName(feat))
	precinct_id = normPID(getPrecinctID(feat))

	if normP(getPrecinctName(feat)) == 'eliwhitneycomplex':
		precinct_id_to_name[(county, precinct_id)] = getPrecinctID(feat) + normP(getPrecinctName(feat))
		precinct_list.append((county, getPrecinctID(feat) + normP(getPrecinctName(feat))))
		continue
	if county == 'ware':
		precinct_id_to_name[(county, precinct_id)] = 'ware'
		precinct_list.append((county, 'ware'))
		continue
	precinct_id_to_name[(county, precinct_id)] = normP(getPrecinctName(feat))
	precinct_list.append((county, normP(getPrecinctName(feat))))

geocoded_precinct_ids = dict()

with open("data/geocoding_2018.csv", "r") as geocoding:
	csvreader = csv.reader(geocoding)
	for row in csvreader:
		reg_number, _, _, county, _, precinct_id = row
		geocoded_precinct_ids[reg_number] = (county, precinct_id)

with open("data/geocoding_new.csv", "r") as geocoding:
	csvreader = csv.reader(geocoding)
	for row in csvreader:
		reg_number, _, _, county, _, precinct_id = row
		geocoded_precinct_ids[reg_number] = (county, precinct_id)
		
general_precinct_map = dict()

import glob
files = list(glob.glob("data/general_precinct_map/*.csv"))
for path in files:
	with open(path) as file:
		county_name = path[26:-4]
		csvreader = csv.reader(file)
		for row in csvreader:
			general_precinct_name, shapefile_precinct_name = row
			general_precinct_map[(county_name, general_precinct_name)] = shapefile_precinct_name

def mapVoter(registered_id, county, precinct_id):
	if (normC(county), normPID(precinct_id)) not in precinct_id_to_name.keys():
		if registered_id in geocoded_precinct_ids.keys():
			county, precinct_id = geocoded_precinct_ids[registered_id]
		else:
			return None
	return (normC(county), precinct_id_to_name[(normC(county), normPID(precinct_id))])

def mapGeneralPrecinct(county, precinct_name):
	return (normC(county), general_precinct_map[(normC(county), normP(precinct_name))])