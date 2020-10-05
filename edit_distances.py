import Levenshtein
import fiona
import csv

county_id_to_county_name = dict()
with open("data/county_ids.csv") as ctyids:
	for line in ctyids:
		county_id, county_name = tuple(line.split(","))
		county_id_to_county_name[int(county_id)] = county_name


def normP(precinct):
	return "".join(precinct.split()).lstrip("0").lower()

def normC(county):
	return "".join(county.split()).lower()


def getCountyName(feat):
	return county_id_to_county_name[int(feat['properties']['CTYNUMBER'])]

def getPrecinctID(feat):
	return feat['properties']['PRECINCT_I']

def getPrecinctName(feat):
	return feat['properties']['PRECINCT_N']

general_precincts = dict()
shape_precincts = dict()

with open("data/precinct_votes_2018.csv") as general:
	csvreader = csv.reader(general)
	first = True
	for row in csvreader:
		if first:
			first = False
			continue
		county = normC(row[0])
		precinct = normP(row[1])
		if county not in general_precincts:
			general_precincts[county] = []
		general_precincts[county].append(precinct)


for feat in fiona.open("data/vtd2018/VTD2018-Shapefile.shp"):
	if feat['properties']['CTYNUMBER'] == None:
		continue
	county = normC(getCountyName(feat))

	if county not in shape_precincts:
		shape_precincts[county] = []
	if normP(getPrecinctName(feat)) == 'eliwhitneycomplex':
		shape_precincts[county].append(getPrecinctID(feat) + normP(getPrecinctName(feat)))
		print(getPrecinctID(feat))
		continue
	shape_precincts[county].append(normP(getPrecinctName(feat)))

print(general_precincts['appling'])
print(shape_precincts['appling'])

import numpy as np
import scipy.optimize

for county, precincts in general_precincts.items():
	with open("data/counties_all/{}.csv".format(county), "w") as out_file:
		csvwriter = csv.writer(out_file)
		graph = np.zeros((len(precincts), max(len(precincts), len(shape_precincts[county]))))
		precincts = sorted(precincts)
		for i, precinct in enumerate(precincts):
			info = [precinct, "", "", "", "", ""]
			distances = []
			longest_general = 0
			for general_precinct in shape_precincts[county]:
				longest_general = max(longest_general, len(general_precinct))
			for general_precinct in shape_precincts[county]:
				padded = general_precinct.ljust(longest_general)
				distances.append((Levenshtein.distance(precinct, padded), general_precinct))
			for j in range(len(distances)):
				graph[i][j] = distances[j][0]
			distances = sorted(distances)
			for i in range(0, min(5, len(distances))):
				info[i+1] = distances[i]
			csvwriter.writerow(info)

		if len(precincts) > len(shape_precincts[county]):
			for i in range(0, len(precincts)):
				for j in range(len(precincts), len(shape_precincts[county])):
					graph[i][j] = 999999

		row_ind, col_ind = scipy.optimize.linear_sum_assignment(graph)
		unused_precincts = set(shape_precincts[county])
		res = [[x, None] for x in precincts]
		is_empty = True

		for i in range(0, len(row_ind)):
			if col_ind[i] >= len(shape_precincts[county]):
				is_empty = False
				continue
			unused_precincts.remove(shape_precincts[county][col_ind[i]])
			res[i][1] = shape_precincts[county][col_ind[i]]
			is_empty = False

		with open("data/counties_hungarian/{}.csv".format(county), 'w') as matching_file:
			csvwriter = csv.writer(matching_file)
			for match in res:
				if match == [None, None]:
					continue
				csvwriter.writerow(match)
			for unused in unused_precincts:
				csvwriter.writerow(['', unused])












