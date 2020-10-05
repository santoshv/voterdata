import csv
import precinct_mapping

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










