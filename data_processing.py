import csv
import precinct_mapping
import statistics
import math
import numpy as np

precinct_data = dict()

for precinct in precinct_mapping.precinct_list:
	precinct_data[precinct] = {"Voters" : 0, "Dropped" : 0, "Dropped No Contact" : 0, "Dropped Returned Mail" : 0, "Dropped NCOA" : 0, "New" : 0, "Democrat" : 0, "Republican" : 0, "Independent" : 0, "Total" : 0}

num_failed_registered = 0
num_failed_dropped = 0
num_failed_new = 0

with open("data/Registered_Voter_Precincts.csv", "r") as voter_data:
	csvreader = csv.reader(voter_data)
	first = True
	for row in csvreader:
		if first:
			first = False
			continue
		reg_num, county, precinct = row
		precinct = precinct_mapping.mapVoter(reg_num, county, precinct)
		if precinct == None:
			num_failed_registered += 1
			continue
		precinct_data[precinct]["Voters"] += 1

print("Failed: {}".format(num_failed_registered))

with open("data/actually_dropped.csv", "r") as actually_dropped:
	csvreader = csv.reader(actually_dropped)
	first = True
	for row in csvreader:
		if first:
			first = False
			continue
		reg_num, _, _, _, _, inactive_reason, county, _, precinct = row
		precinct = precinct_mapping.mapVoter(reg_num, county, precinct)
		if precinct == None:
			num_failed_dropped += 1
			continue
		precinct_data[precinct]["Dropped"] += 1
		inactive_reason = inactive_reason.strip()
		if inactive_reason == "No Contact":
			precinct_data[precinct]["Dropped No Contact"] += 1
		elif inactive_reason == "Returned Mail":
			precinct_data[precinct]["Dropped Returned Mail"] += 1
		elif inactive_reason == "NCOA":
			precinct_data[precinct]["Dropped NCOA"] += 1

print("Failed Dropped: {}".format(num_failed_dropped))

with open("data/newly_added.csv", "r") as newly_added:
	csvreader = csv.reader(newly_added)
	first = True
	for row in csvreader:
		if first:
			first = False
			continue
		reg_num, _, _, _, _, _, county, _, precinct = row
		precinct = precinct_mapping.mapVoter(reg_num, county, precinct)
		if precinct == None:
			num_failed_new += 1
			continue
		precinct_data[precinct]["New"] += 1

print("Failed New: {}".format(num_failed_new))

num_failed_general = 0

with open("data/precinct_votes_2018.csv", "r") as precinct_votes_2018:
	csvreader = csv.reader(precinct_votes_2018)
	first = True
	for row in csvreader:
		if first:
			first = False
			continue
		county, precinct_id, rep, dem, ind, total = row
		precinct = precinct_mapping.mapGeneralPrecinct(county, precinct_id)
		if precinct == None:
			num_failed_general += 1
			continue
		precinct_data[precinct]["Republican"] += int(rep)
		precinct_data[precinct]["Democrat"] += int(dem)
		precinct_data[precinct]["Independent"] += int(ind)
		precinct_data[precinct]["Total"] += int(total)

print("Failed General Maps: {}".format(num_failed_general))

with open("data/precinct_aggregate_data.csv", "w") as aggregate_data:
	csvwriter = csv.writer(aggregate_data)
	csvwriter.writerow(["County", "Precinct", "Registered", "Dropped", "Dropped No Contact", "Dropped Returned Mail", "Dropped NCOA", "New", "Democrat", "Republican", "Independent", "Total"])
	for precinct, data in sorted(precinct_data.items()):
		csvwriter.writerow([precinct[0], precinct[1], data["Voters"], data["Dropped"], data["Dropped No Contact"], data["Dropped Returned Mail"], data["Dropped NCOA"], data["New"], data["Democrat"], data["Republican"], data["Independent"], data["Total"]])

dropped_reasons = ["Dropped", "Dropped No Contact", "Dropped Returned Mail", "Dropped NCOA", "New"]
for dropped_reason in dropped_reasons:
	democrat_percent_bins = [[]]
	dropped_percent_bins = [[]]
	voters_per_bin = [0]
	IDEAL_VOTERS_PER_BIN = 151720
	current_total = 0
	for data in sorted(precinct_data.values(), key = lambda x: x["Democrat"] / x["Total"]):
		if data["Voters"] == 0:
			continue
		if abs(current_total - IDEAL_VOTERS_PER_BIN) < abs(current_total + data["Voters"] - IDEAL_VOTERS_PER_BIN):
			current_total = 0
			democrat_percent_bins.append([])
			dropped_percent_bins.append([])
			voters_per_bin.append(0)
		democrat_percent_bins[-1].append(data["Democrat"] / data["Total"])
		dropped_percent_bins[-1].append(data[dropped_reason] / data["Voters"])
		voters_per_bin[-1] += data["Voters"]
		current_total += data["Voters"]


	democrat_percent_bins[-2] += democrat_percent_bins[-1]
	democrat_percent_bins.pop()
	dropped_percent_bins[-2] += dropped_percent_bins[-1]
	dropped_percent_bins.pop()
	voters_per_bin[-2] += voters_per_bin[-1]
	voters_per_bin.pop()

	with open('data/binned{}.csv'.format(dropped_reason), 'w', newline = '') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['bin', 'median dropped percent', 'overall median', 'num voters in bin'])
		overall_median = statistics.median([x[dropped_reason] / x["Voters"] for x in precinct_data.values()if x["Voters"] != 0])
		for democrat_percents, dropped_percents, voters_in_bin in zip(democrat_percent_bins, dropped_percent_bins, voters_per_bin):
			median_dropped = 0
			if len(dropped_percents) != 0:
				median_dropped = statistics.median(dropped_percents)
			writer.writerow(["{} - {}".format(round(democrat_percents[0]*100, 2), round(democrat_percents[-1]*100, 2)), median_dropped * 100, overall_median * 100, voters_in_bin])


# def mean(x, w):
# 	return sum([xi * wi for xi, wi in zip(x, w)]) / sum([wi for wi in w])

# def cov(x, y, w):
# 	mxw = mean(x, w)
# 	myw = mean(y, w)
# 	sw = sum([wi for wi in w])
# 	return sum([wi * (xi - mxw) * (yi - myw) for xi, yi, wi in zip(x, y, w)]) / sum([wi for wi in w])

def weighted_correlation(x, y, w):
	covmat = np.cov(x, y, aweights = w)
	return covmat[0][1] / math.sqrt(covmat[0][0] * covmat[1][1])
	#return cov(x, y, w) / math.sqrt(cov(x, x, w) * cov(y, y, w))

print("Correlations: ")

data = [(x["Dropped"] / x["Voters"], \
x["Democrat"] / x["Total"], \
x["Republican"] / x["Total"], \
x["Voters"]) for x in precinct_data.values() if x["Voters"] != 0]
percent_dropped, percent_democrat, percent_republican, num_voters = zip(*data)
print(weighted_correlation(percent_dropped, percent_democrat, num_voters))
print(weighted_correlation(percent_dropped, percent_republican, num_voters))

